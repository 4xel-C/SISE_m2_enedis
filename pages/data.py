import matplotlib.pyplot as plt
import pandas as pd
import pydeck as pdk
import seaborn as sns
import streamlit as st

# General configuration
st.set_page_config(page_title="DPE Map & Statistics", page_icon="🗺️", layout="wide")

st.title("🗺️ Map and 📊 Statistics of the DPE Dataset")

# === Data upload ===
st.header("📂 Data Upload")
data_files = st.file_uploader(
    "Upload one or more CSV files",
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


# === Global parameters ===
DEFAULT_POINTS_MAP = 100_000
DEFAULT_ROWS_DISPLAY = 10_000
NB_BINS = 50

# === If files are imported ===
if data_files:
    data = load_data(data_files)

    # Check required columns
    required_cols = {"lat", "lon", "etiquette_dpe", "cout_total_5_usages"}
    if not required_cols.issubset(data.columns):
        st.error(f"❌ Missing columns: {required_cols - set(data.columns)}")
        st.stop()

    # Main tabs
    tab1, tab2 = st.tabs(["🗺️ DPE Map", "📊 Dataset Statistics"])

    # --- Tab 1: Map ---
    with tab1:
        st.subheader("Geographical visualization of housing")

        # Slider to choose the number of points on the map
        max_points_possible = len(data)
        nb_points_map = st.slider(
            "Number of homes displayed on the map 🗺️",
            min_value=0,
            max_value=max_points_possible,
            value=min(DEFAULT_POINTS_MAP, max_points_possible),
            step=1_000,
            help="Adjust to limit the number of points and improve smoothness.",
        )

        # Random sampling
        if len(data) > nb_points_map:
            data_map = data.sample(nb_points_map, random_state=42)
            st.caption(
                f"🧮 {nb_points_map:,} homes displayed out of {max_points_possible:,}."
            )
        else:
            data_map = data
            st.caption(f"🧮 All {len(data):,} homes are displayed.")

        # Pydeck map
        # os.environ["MAPBOX_API_KEY"] = st.secrets["MAPBOX_API_KEY"]

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
            "html": "<b>DPE Label:</b> {etiquette_dpe}<br/>"
            "<b>Total Cost (5 Uses):</b> {cout_total_5_usages}<br/>"
            "<b>Lat:</b> {lat}<br/><b>Lon:</b> {lon}",
            "style": {"backgroundColor": "white", "color": "black"},
        }

        deck = pdk.Deck(
            map_style="mapbox://styles/mapbox/satellite-streets-v12",
            initial_view_state=view_state,
            layers=[layer],
            tooltip=tooltip,
        )

        st.pydeck_chart(deck, width="stretch")

    # --- Tab 2: Statistics ---
    with tab2:
        st.subheader("Statistical analysis of the dataset")

        # Slider to choose the number of displayed rows
        max_rows_possible = len(data)
        nb_rows_display = st.slider(
            "Number of rows displayed in the dataset preview 📄",
            min_value=0,
            max_value=max_rows_possible,
            value=min(DEFAULT_ROWS_DISPLAY, max_rows_possible),
            step=1_000,
            help="Displays a random sample of the dataset to avoid slowdowns.",
        )

        # Sampling for display
        if len(data) > nb_rows_display:
            df_display = data.sample(nb_rows_display, random_state=42)
            st.caption(f"🧮 {nb_rows_display:,} rows displayed out of {len(data):,}.")
        else:
            df_display = data
            st.caption(f"🧮 All {len(data):,} rows are displayed.")

        st.dataframe(df_display)

        # Numeric columns
        numeric_cols = data.select_dtypes(include="number").columns.tolist()

        st.markdown("### Descriptive statistics")
        st.write(data[numeric_cols].describe())

        # Histogram of DPE classes
        if "etiquette_dpe" in data.columns:
            st.markdown("### Distribution of DPE classes")
            dpe_counts = data["etiquette_dpe"].value_counts().sort_index()
            st.bar_chart(dpe_counts, width="stretch")
        else:
            st.info("No 'etiquette_dpe' column found in the dataset.")

        st.markdown("### Distribution of total cost (5 uses)")

        # Cost categorization
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

        st.bar_chart(cout_counts, width="stretch")
        st.dataframe(cout_counts.rename("Number of homes"))

        if "etiquette_dpe" in data.columns and "cout_total_5_usages" in data.columns:
            st.markdown("### Distribution of total cost by DPE class")

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
            ax.set_title("Total cost (5 uses) by DPE class (with mean)")
            ax.set_xlabel("DPE class")
            ax.set_ylabel("Total cost (€)")
            st.pyplot(fig)

        st.markdown("### Dominant DPE class by municipality")
        region_dpe = data.groupby("nom_commune_ban")["etiquette_dpe"].agg(
            lambda x: x.mode()[0] if not x.mode().empty else None
        )
        st.dataframe(region_dpe)


else:
    st.info("⬆️ Please upload one or more CSV files to get started.")
