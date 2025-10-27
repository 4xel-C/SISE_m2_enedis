import os

import matplotlib.pyplot as plt
import pandas as pd
import pydeck as pdk
import seaborn as sns
import streamlit as st

# Configuration générale
st.set_page_config(page_title="Carte & Statistiques DPE", page_icon="🗺️", layout="wide")

st.title("🗺️ Carte et 📊 Statistiques du Dataset DPE")

# === Upload de données ===
st.header("📂 Chargement des Données")
data_files = st.file_uploader(
    "Téléchargez un ou plusieurs fichiers CSV",
    type=["csv"],
    accept_multiple_files=True,
    key="data_files",
)


@st.cache_data
def load_data(files):
    dfs = []
    for f in files:
        df = pd.read_csv(f)
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)


# === Paramètres globaux ===
DEFAULT_POINTS_MAP = 100_000
DEFAULT_ROWS_DISPLAY = 10_000
NB_BINS = 50

# === Si des fichiers sont importés ===
if data_files:
    data = load_data(data_files)

    # Vérification colonnes requises
    required_cols = {"lat", "lon", "etiquette_dpe", "cout_total_5_usages"}
    if not required_cols.issubset(data.columns):
        st.error(f"❌ Colonnes manquantes : {required_cols - set(data.columns)}")
        st.stop()

    # Onglets principaux
    tab1, tab2 = st.tabs(["🗺️ Carte DPE", "📊 Statistiques du Dataset"])

    # --- Onglet 1 : Carte ---
    with tab1:
        st.subheader("Visualisation géographique des logements")

        # Slider pour choisir le nombre de points sur la carte
        max_points_possible = len(data)
        nb_points_map = st.slider(
            "Nombre de logements affichés sur la carte 🗺️",
            min_value=1_000,
            max_value=max_points_possible,
            value=min(DEFAULT_POINTS_MAP, max_points_possible),
            step=1_000,
            help="Ajustez pour limiter le nombre de points et améliorer la fluidité.",
        )

        # Échantillonnage aléatoire
        if len(data) > nb_points_map:
            data_map = data.sample(nb_points_map, random_state=42)
            st.caption(
                f"🧮 {nb_points_map:,} logements affichés sur {max_points_possible:,}."
            )
        else:
            data_map = data
            st.caption(f"🧮 Tous les {len(data):,} logements sont affichés.")

        # Carte Pydeck
        os.environ["MAPBOX_API_KEY"] = st.secrets["MAPBOX_API_KEY"]

        view_state = pdk.ViewState(
            latitude=data_map["lat"].mean(),
            longitude=data_map["lon"].mean(),
            zoom=6,
            pitch=0,
        )

        layer = pdk.Layer(
            "ScatterplotLayer",
            data=data_map,
            get_position="[lon, lat]",
            get_color="[200, 30, 0, 160]",
            get_radius=40,
            pickable=True,
        )

        tooltip = {
            "html": "<b>Étiquette DPE:</b> {etiquette_dpe}<br/>"
            "<b>Coût Total 5 Usages:</b> {cout_total_5_usages}<br/>"
            "<b>Lat:</b> {lat}<br/><b>Lon:</b> {lon}",
            "style": {"backgroundColor": "white", "color": "black"},
        }

        deck = pdk.Deck(
            map_style="mapbox://styles/mapbox/satellite-streets-v12",
            initial_view_state=view_state,
            layers=[layer],
            tooltip=tooltip,
        )

        st.pydeck_chart(deck, use_container_width=True)

    # --- Onglet 2 : Statistiques ---
    with tab2:
        st.subheader("Analyse statistique du dataset")

        # Slider pour choisir le nombre de lignes affichées
        max_rows_possible = len(data)
        nb_rows_display = st.slider(
            "Nombre de lignes affichées dans l’aperçu du dataset 📄",
            min_value=1_000,
            max_value=max_rows_possible,
            value=min(DEFAULT_ROWS_DISPLAY, max_rows_possible),
            step=1_000,
            help="Affiche un échantillon aléatoire du dataset pour éviter les ralentissements.",
        )

        # Échantillonnage pour l’affichage
        if len(data) > nb_rows_display:
            df_display = data.sample(nb_rows_display, random_state=42)
            st.caption(f"🧮 {nb_rows_display:,} lignes affichées sur {len(data):,}.")
        else:
            df_display = data
            st.caption(f"🧮 Toutes les {len(data):,} lignes sont affichées.")

        st.dataframe(df_display)

        # Colonnes numériques
        numeric_cols = data.select_dtypes(include="number").columns.tolist()

        st.markdown("### Statistiques descriptives")
        st.write(data[numeric_cols].describe())

        # Histogramme des classes DPE
        if "etiquette_dpe" in data.columns:
            st.markdown("### Répartition des classes DPE")
            dpe_counts = data["etiquette_dpe"].value_counts().sort_index()
            st.bar_chart(dpe_counts, use_container_width=True)
        else:
            st.info("Aucune colonne 'etiquette_dpe' trouvée dans le dataset.")

        st.markdown("### Distribution du coût total (5 usages)")

        # Catégorisation des coûts
        bins = [0, 500, 1000, 1500, float("inf")]
        labels = ["< 500 €", "500 – 1000 €", "1000 – 1500 €", "> 1500 €"]

        data["cat_cout"] = pd.cut(
            data["cout_total_5_usages"],
            bins=bins,
            labels=labels,
            right=False,
            ordered=True,
        )
        cout_counts = data["cat_cout"].value_counts(sort=False).reindex(labels)

        st.bar_chart(cout_counts, use_container_width=True)
        st.dataframe(cout_counts.rename("Nombre de logements"))

        if "etiquette_dpe" in data.columns and "cout_total_5_usages" in data.columns:
            st.markdown("### Distribution du coût total selon la classe DPE")

            subset = data[["etiquette_dpe", "cout_total_5_usages"]].dropna()

            fig, ax = plt.subplots(figsize=(8, 4))
            sns.boxplot(
                data=subset,
                x="etiquette_dpe",
                y="cout_total_5_usages",
                showfliers=False,
                ax=ax,
            )
            sns.pointplot(
                data=subset,
                x="etiquette_dpe",
                y="cout_total_5_usages",
                estimator="mean",
                color="red",
                markers="D",
                linestyles="",
                ax=ax,
            )
            ax.set_title("Coût total (5 usages) selon la classe DPE (avec moyenne)")
            ax.set_xlabel("Classe DPE")
            ax.set_ylabel("Coût total (€)")
            st.pyplot(fig)

        st.markdown("### Classe DPE dominante par commune")
        region_dpe = data.groupby("nom_commune_ban")["etiquette_dpe"].agg(
            lambda x: x.mode()[0] if not x.mode().empty else None
        )
        st.dataframe(region_dpe)


else:
    st.info("⬆️ Veuillez charger un ou plusieurs fichiers CSV pour commencer.")
