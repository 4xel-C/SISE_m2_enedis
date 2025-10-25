import streamlit as st
import pandas as pd
import os
import pydeck as pdk

st.set_page_config(page_title="DPE Ademe, Enedis", page_icon="🗺️", layout="wide")

st.title("DPE Ademe")

st.sidebar.header("Chargement des Données")
data_files = st.sidebar.file_uploader("Téléchargez un ou plusieurs fichiers CSV", type=["csv"], accept_multiple_files=True, key="data_files")

@st.cache_data
def load_data(files):
    dfs = []
    for f in files:
        df = pd.read_csv(f)
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

if data_files:
    data = load_data(data_files)
    

    # Vérification des colonnes
    required_cols = {"lat", "lon", "etiquette_dpe", "cout_total_5_usages"}
    if not required_cols.issubset(data.columns):
        st.error(f"❌ Les colonnes requises sont manquantes : {required_cols - set(data.columns)}")
        st.stop()
    
    # Limitation visuelle (optionnelle)
    MAX_POINTS = 100000  # Pydeck peut monter à 1M+, mais les fichiers sont limités à 200 MB et on est à 412.9 avec tout le clean_dataset.csv
    if len(data) > MAX_POINTS:
        st.warning(f"⚠️ Seulement {MAX_POINTS:,} points affichés sur {len(data):,}")
        data = data.sample(MAX_POINTS, random_state=42)
    
    os.environ["MAPBOX_API_KEY"] = st.secrets["MAPBOX_API_KEY"]

    # Vue initiale centrée sur les données
    view_state = pdk.ViewState(
        latitude=data["lat"].mean(),
        longitude=data["lon"].mean(),
        zoom=6,
        pitch=0,
    )

    # Paramétrage de la carte
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=data,
        get_position='[lon, lat]',
        get_color='[200, 30, 0, 160]',  # rouge semi-transparent
        get_radius=40,
        pickable=True,
    )

    # Tooltip (infobulle)
    tooltip = {
        "html": "<b>Étiquette DPE:</b> {etiquette_dpe}<br/>"
                "<b>Coût Total 5 Usages:</b> {cout_total_5_usages}<br/>"
                "<b>Lat:</b> {lat}<br/><b>Lon:</b> {lon}",
        "style": {"backgroundColor": "white", "color": "black"}
    }
    
    ''' Différents styles de cartes
        {
        "Rues": "mapbox://styles/mapbox/streets-v12",
        "Clair": "mapbox://styles/mapbox/light-v11",
        "Sombre": "mapbox://styles/mapbox/dark-v11",
        "Satellite": "mapbox://styles/mapbox/satellite-v9",
        "Hybride": "mapbox://styles/mapbox/satellite-streets-v12",
        }
    '''
    # Carte Pydeck
    deck = pdk.Deck(
    map_style="mapbox://styles/mapbox/satellite-streets-v12",
    initial_view_state=view_state,
    layers=[layer],
    tooltip=tooltip,
    )

    st.pydeck_chart(deck)

else:
    st.info("⬆️ Veuillez charger un ou plusieurs fichiers CSV pour commencer.")

