import streamlit as st
import pandas as pd
import joblib
import os


# Configuration page
st.set_page_config(page_title="Prédiction DPE", page_icon="🔮", layout="centered")
st.title("🔮 Prédiction de la Classe DPE d’un logement")

# Chargement des modèles
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
    st.error(f"❌ Une librairie manque pour charger le modèle : {e}")
    st.stop()
except FileNotFoundError as e:
    st.error(f"❌ Fichier manquant : {e}")
    st.stop()
except Exception as e:
    st.error(f"❌ Erreur lors du chargement des modèles : {e}")
    st.stop()

st.sidebar.success("✅ Modèles ML chargés")


# Formulaire utilisateur
st.markdown("### 🧾 Saisir les caractéristiques du logement")

with st.form("form_pred"):
    st.subheader("🔹 Caractéristiques quantitatives")
    cout_total_5_usages = st.number_input(
        "Coût total sur 5 usages (€/mois)", 0.0, 5000.0, 500.0
    )
    surface_habitable_logement = st.number_input(
        "Surface habitable logement (m²)", 10.0, 400.0, 75.0
    )
    nombre_niveau_logement = st.number_input("Nombre de niveaux", 1, 10, 2)
    age_batiment = st.number_input("Âge du bâtiment (années)", 0, 150, 33)
    altitude_moyenne = st.number_input("Altitude moyenne (m)", 0, 2000, 100)

    st.subheader("🔹 Caractéristiques qualitatives")
    type_energie_principale_chauffage = st.selectbox(
        "Énergie principale chauffage", ["Autre", "Gaz naturel", "Électricité"]
    )
    type_batiment = st.selectbox(
        "Type de bâtiment", ["appartement", "maison", "immeuble"]
    )
    zone_climatique = st.selectbox("Zone climatique", ["H1", "H2", "H3"])

    submitted = st.form_submit_button("🔮 Prédire la classe DPE")


# Préparer le DataFrame pour la prédiction
if submitted:
    # Dictionnaire utilisateur
    user_input = {
        "cout_total_5_usages": cout_total_5_usages,
        "surface_habitable_logement": surface_habitable_logement,
        "nombre_niveau_logement": nombre_niveau_logement,
        "age_batiment": age_batiment,
        "altitude_moyenne": altitude_moyenne,
        "type_energie_principale_chauffage": type_energie_principale_chauffage,
        "type_batiment": type_batiment,
        "zone_climatique": zone_climatique,
    }

    # Créer DataFrame avec toutes les colonnes nécessaires
    features_columns = user_input.keys()
    X_input = pd.DataFrame(columns=features_columns)
    for col in features_columns:
        X_input.at[0, col] = user_input[col]

    # Prédiction
    try:
        y_pred_int = pipeline_model.predict(X_input)
        y_pred_label = label_encoder.inverse_transform(y_pred_int)
    except Exception as e:
        st.error(f"❌ Erreur pendant la prédiction : {e}")
        st.stop()

    # Affichage résultat
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

    st.success(f"✅ Classe DPE prédite : **{y_pred_label[0]}**")
    st.markdown(
        f"<div style='text-align:center; padding:1rem; font-size:2rem; "
        f"background-color:{couleur}; color:white; border-radius:0.5rem;'>"
        f"Classe {y_pred_label[0]}</div>",
        unsafe_allow_html=True,
    )
