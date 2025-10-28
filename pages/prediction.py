import os

import joblib
import pandas as pd
import streamlit as st

from src.data_requesters.elevation import Elevation_API_requester
from src.data_requesters.geo_features import get_zone_and_altitude

# Page configuration
st.set_page_config(page_title="DPE Prediction", page_icon="🔮", layout="centered")
st.title("🔮 Prediction of a Home's DPE Class")

# Model loading
ML_DIR = "MLmodels"


@st.cache_resource
def load_pipeline():
    return joblib.load(os.path.join(ML_DIR, "pipeline_xgboost_classification.pkl"))


@st.cache_resource
def load_label_encoder():
    return joblib.load(os.path.join(ML_DIR, "label_encoder_target.pkl"))


try:
    pipeline_model = load_pipeline()
    label_encoder = load_label_encoder()
except ModuleNotFoundError as e:
    st.error(f"❌ Missing library to load the model: {e}")
    st.stop()
except FileNotFoundError as e:
    st.error(f"❌ Missing file: {e}")
    st.stop()
except Exception as e:
    st.error(f"❌ Error while loading models: {e}")
    st.stop()

st.sidebar.success("✅ ML models successfully loaded")

# User form
st.markdown("### 🧾 Enter the home's characteristics")

with st.form("form_pred"):
    # ---- New section: City -> automatic zone & altitude ----
    st.subheader("🏙️ Location")
    city = st.text_input("City name", placeholder="e.g. Marseille, Lyon, Lille...")

    # ---- Main quantitative inputs ----
    st.subheader("🔹 Quantitative characteristics")
    cout_total_5_usages = st.number_input(
        "Total cost 5 uses (€/year)", 0.0, 5000.0, 500.0, 10.0
    )
    surface_habitable_logement = st.number_input(
        "Living area (m²)", 10.0, 400.0, 75.0, 1.0
    )
    nombre_niveau_logement = st.number_input("Number of floors", 1, 10, 2)
    age_batiment = st.number_input("Building age (years)", 0, 150, 33)

    # ---- Qualitative inputs ----
    st.subheader("🔹 Qualitative characteristics")

    energy_options = {
        "Other": "Autre",
        "Natural gas": "Gaz naturel",
        "Electricity": "Électricité",
    }
    building_options = {
        "Apartment": "appartement",
        "House": "maison",
        "Building": "immeuble",
    }

    type_energie_principale_chauffage_label = st.selectbox(
        "Main heating energy", list(energy_options.keys())
    )
    type_batiment_label = st.selectbox("Building type", list(building_options.keys()))

    submitted = st.form_submit_button("🔮 Predict DPE class")

# Prediction
if submitted:
    if not city.strip():
        st.error("❌ Please enter a city name before predicting.")
        st.stop()

    # ---- Step 1: Retrieve zone & coordinates
    with st.spinner(f"📡 Retrieving climate zone for {city}..."):
        geo_info = get_zone_and_altitude(ville=city)
        zone_clim = geo_info.get("zone_climatique")
        lat, lon = geo_info.get("lat"), geo_info.get("lon")

    if not lat or not lon:
        st.warning("⚠️ Could not retrieve coordinates for this city.")
        altitude_moyenne = 0
    else:
        # ---- Step 2: Retrieve elevation
        with st.spinner(f"⛰️ Fetching elevation data for {city}..."):
            elev_requester = Elevation_API_requester()
            altitude_moyenne = elev_requester.get_elevation(lat, lon) or 0

    # ---- Display fetched info
    st.markdown("### 🌦️ Automatically detected information")
    st.info(
        f"- **City:** {city}  \n"
        f"- **Latitude / Longitude:** {lat:.4f}, {lon:.4f}  \n"
        f"- **Climate zone:** {zone_clim or 'Unknown'}  \n"
        f"- **Average altitude:** {altitude_moyenne:.1f} m"
    )

    # ---- Prepare input dataframe
    user_input = {
        "cout_total_5_usages": cout_total_5_usages,
        "surface_habitable_logement": surface_habitable_logement,
        "nombre_niveau_logement": nombre_niveau_logement,
        "age_batiment": age_batiment,
        "altitude_moyenne": altitude_moyenne,
        "type_energie_principale_chauffage": energy_options[
            type_energie_principale_chauffage_label
        ],
        "type_batiment": building_options[type_batiment_label],
        "zone_climatique": zone_clim,
    }

    X_input = pd.DataFrame([user_input])

    # ---- Prediction
    try:
        y_pred_int = pipeline_model.predict(X_input)
        y_pred_label = label_encoder.inverse_transform(y_pred_int)
    except Exception as e:
        st.error(f"❌ Error during prediction: {e}")
        st.stop()

    # ---- Display result
    dpe_colors = {
        "A": "#00b050",
        "B": "#92d050",
        "C": "#ffff00",
        "D": "#ffc000",
        "E": "#ff0000",
        "F": "#a61c00",
        "G": "#7030a0",
    }
    couleur = dpe_colors.get(str(y_pred_label[0]).upper(), "#CCCCCC")

    st.success(f"✅ Predicted DPE class: **{y_pred_label[0]}**")
    st.markdown(
        f"<div style='text-align:center; padding:1rem; font-size:2rem; "
        f"background-color:{couleur}; color:white; border-radius:0.5rem;'>"
        f"Class {y_pred_label[0]}</div>",
        unsafe_allow_html=True,
    )
