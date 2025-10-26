import streamlit as st
import pandas as pd

st.set_page_config(page_title="Stats Dataset DPE", page_icon="📊", layout="wide")
st.title("Statistiques du Dataset DPE")

st.sidebar.header("Chargement des Données")
data_files = st.sidebar.file_uploader(
    "Téléchargez un ou plusieurs fichiers CSV",
    type=["csv"],
    accept_multiple_files=True,
    key="stats_data_files"
)

@st.cache_data
def load_data(files):
    dfs = []
    for f in files:
        df = pd.read_csv(f)
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

MAX_DISPLAY_ROWS = 10000   # max lignes affichées
SAMPLE_HIST = 50000        # échantillon pour histogrammes
NB_BINS = 50               # nombre d'intervalles pour pd.cut

if data_files:
    data = load_data(data_files)

    # Vérification des colonnes nécessaires
    required_cols = {"lat", "lon", "etiquette_dpe", "cout_total_5_usages"}
    missing = required_cols - set(data.columns)
    if missing:
        st.error(f"❌ Colonnes manquantes : {missing}")
        st.stop()

    # Aperçu des données (limité)
    st.subheader("Aperçu des données")
    if len(data) > MAX_DISPLAY_ROWS:
        st.warning(f"⚠️ Affichage limité à {MAX_DISPLAY_ROWS:,} lignes sur {len(data):,}")
        df_display = data.sample(MAX_DISPLAY_ROWS, random_state=42)
    else:
        df_display = data
    st.dataframe(df_display)

    # Colonnes numériques
    numeric_cols = data.select_dtypes(include="number").columns.tolist()

    # Statistiques rapides
    st.subheader("Statistiques rapides")
    st.write(data[numeric_cols].describe())

    st.subheader("Rajouter des schémas pour la suite")

else:
    st.info("⬆️ Veuillez charger un ou plusieurs fichiers CSV pour commencer.")
