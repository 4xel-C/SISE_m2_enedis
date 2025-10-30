from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pydeck as pdk
import streamlit as st
from streamlit_dynamic_filters import DynamicFilters

from src.utils.dataloader import generate_file_selector

# General configuration
st.set_page_config(page_title="DPE Map & Statistics", page_icon="🗺️", layout="wide")

# === Path to CSV Files ===
DATASETS_DIR = Path(__file__).parent.parent / "data" / "datasets"


st.title("📊 Statistics of the DPE Dataset")

# === Side bar files selection ===
generate_file_selector()

# Load the data in memory.
data = st.session_state.get("df", None)

# === Display Data ===
if data is not None:
    # Check required columns
    required_cols = {"lat", "lon", "etiquette_dpe", "cout_total_5_usages"}
    if not required_cols.issubset(data.columns):
        st.error(f"❌ Missing columns: {required_cols - set(data.columns)}")
        st.stop()

    # Main tabs
    (
        tab1,
        tab2,
    ) = st.tabs(["🧮 Datasets Print", "📊 Dataset Statistics"])

    # --- Tab 1: Datasets ---
    with tab1:
        st.subheader("Your data preview")
        if data is not None:
            st.write(f"Number of rows: {len(data)}")
            st.dataframe(data.head(50), width="stretch")
        else:
            st.info("No CSV files uploaded.")

    # --- Tab 3: Statistics ---
    with tab2:
        # ------------------------------------------------------------------------------------------

        # Filter Section
        cols = ["nom_commune_ban", "type_batiment", "etiquette_dpe"]
        for c in cols:
            data[c] = data[c].fillna("Unknown").astype(str)

        dynamic_filters = DynamicFilters(data, filters=cols)
        st.markdown("<br>", unsafe_allow_html=True)
        st.write("Filters")
        dynamic_filters.display_filters(location="columns", num_columns=3, gap="large")

        filtered_df = dynamic_filters.filter_df()

        # Get the number of filtered rows
        n = filtered_df.shape[0]

        st.divider()

        # ------------------------------------------------------------------------------------------
        # Metrics Section
        col1, col2, col3, col4 = st.columns(4)

        # Mean surface habitable
        surface_moyenne = filtered_df["surface_habitable_logement"].mean()
        col1.metric(
            label="Moyenne Surface Habitable",
            value=f"{round(surface_moyenne, 2)}m²",
            border=True,
        )
        # Mean consommation énergie
        consommation_moyenne = filtered_df["cout_total_5_usages"].mean()
        col2.metric(
            label="Consommation Moyenne (kWh/an)",
            value=f"{round(consommation_moyenne, 2)} kWh",
            border=True,
        )
        # Mean cout
        cout_moyen = filtered_df["cout_total_5_usages"].mean()
        col3.metric(
            label="Coût moyen (€/an)", value=f"{round(cout_moyen, 2)}€", border=True
        )
        # Most frequent DPE class
        most_common_dpe = filtered_df["etiquette_dpe"].mode()[0]
        col4.metric(
            label="Etiquette DPE plus fréquente (replace with icon)",
            value=most_common_dpe,
            border=True,
        )

        # ------------------------------------------------------------------------------------------
        # General Info
        col1, col2, col3 = st.columns([0.4, 0.3, 0.3])

        # Statistics Table
        with col1:
            st.write("")
            st.write("")
            conso_stats = filtered_df["conso_5_usages_ef"].describe()
            cout_stats = filtered_df["cout_total_5_usages"].describe()
            ges_stat = filtered_df["emission_ges_5_usages"].describe()
            with st.container():
                summary_df = pd.DataFrame(
                    {
                        "Conso Énergétique (kWep)": conso_stats,
                        "Emission Ges (kgCO₂/an)": ges_stat,
                        "Coût (€)": cout_stats,
                    }
                ).round(2)
                st.markdown("**Statistiques**")
                st.dataframe(
                    summary_df.style.set_table_styles(
                        [{"selector": "td, th", "props": [("font-size", "12px")]}]
                    )
                )
        # DPE class Distribution
        with col2:
            dpe_counts = (
                filtered_df["etiquette_dpe"]
                .value_counts()
                .reindex(["A", "B", "C", "D", "E", "F", "G"], fill_value=0)
            )
            labels = dpe_counts.index.tolist()
            counts = dpe_counts.values
            percentages = counts / counts.sum() * 100

            # DPE colors
            dpe_colors = {
                "A": "#006400",  # Dark Green
                "B": "#008000",  # Green
                "C": "#9ACD32",  # Yellow-Green
                "D": "#FFFF00",  # Yellow
                "E": "#FFA500",  # Orange
                "F": "#FF4500",  # Red-Orange
                "G": "#FF0000",  # Red
            }
            colors = [dpe_colors[label] for label in labels]

            # horizontal bar chart
            fig_col = go.Figure(
                data=[
                    go.Bar(
                        y=labels,
                        x=percentages,
                        marker_color=colors,
                        text=[f"{p:.2f}%" for p in percentages],
                        textposition="auto",
                        orientation="h",
                    )
                ]
            )

            fig_col.update_layout(
                title="Répartition des classes DPE",
                xaxis_title="",
                yaxis_title="Classe DPE",
            )
            fig_col.update_yaxes(autorange="reversed")

            st.plotly_chart(fig_col, width="stretch")

        # GES class Distribution
        with col3:
            ges_colors = {
                "A": "#E3D1F4",  # very light violet
                "B": "#C7A8E4",
                "C": "#AB7ED4",
                "D": "#8F55C4",
                "E": "#733BB4",
                "F": "#5722A4",
                "G": "#3B0A94",  # dark violet
            }

            # Count and order
            ges_counts = (
                filtered_df["etiquette_ges"]
                .value_counts()
                .reindex(["A", "B", "C", "D", "E", "F", "G"], fill_value=0)
            )
            labels = ges_counts.index.tolist()
            counts = ges_counts.values
            percentages = counts / counts.sum() * 100

            colors = [ges_colors[label] for label in labels]

            # horizontal bar chart
            fig_ges = go.Figure(
                data=[
                    go.Bar(
                        y=labels,
                        x=percentages,
                        marker_color=colors,
                        text=[f"{p:.2f}%" for p in percentages],
                        textposition="auto",
                        orientation="h",
                    )
                ]
            )

            fig_ges.update_layout(
                title="Répartition des classes GES",
                xaxis_title="",
                yaxis_title="Classe GES",
            )
            fig_ges.update_yaxes(autorange="reversed")

            st.plotly_chart(fig_ges, width="stretch")

        # Energy consumption and cost per class DPE
        col1, col2 = st.columns(2)

        # Consommation énergie par classe DPE
        with col1:
            fig_box = px.box(
                filtered_df,
                x="etiquette_dpe",
                y="conso_5_usages_ef",
                category_orders={"etiquette_dpe": ["A", "B", "C", "D", "E", "F", "G"]},
                points=False,
                title="Consommation énergie par classe DPE",
            )
            st.plotly_chart(fig_box, width="stretch")

        # Coût moyen par classe DPE
        with col2:
            fig = px.histogram(
                filtered_df,
                x="etiquette_dpe",
                y="cout_total_5_usages",
                category_orders={"etiquette_dpe": ["A", "B", "C", "D", "E", "F", "G"]},
                histfunc="avg",
                title="Coût moyen par classe DPE",
                labels={
                    "etiquette_dpe": "Classe DPE",
                    "cout_total_5_usages": "Coût(€)",
                },
                text_auto=True,
            )

            fig.update_layout(template="plotly_white", showlegend=False)
            st.plotly_chart(fig, width="stretch")

        st.divider()
        # ------------------------------------------------------------------------------------------
        # Consommation d'énergie par Type d'Usage
        st.subheader("Consommation d'énergie par Type d'Usage")
        usage_map = {
            "Chauffage": {
                "conso": "conso_chauffage_ef",
                "cout": "cout_chauffage",
                "ges": "emission_ges_chauffage",
            },
            "ECS": {
                "conso": "conso_ecs_ef",
                "cout": "cout_ecs",
                "ges": "emission_ges_ecs",
            },
            "Refroidissement": {
                "conso": "conso_refroidissement_ef",
                "cout": "cout_refroidissement",
                "ges": "emission_ges_refroidissement",
            },
            "Eclairage": {
                "conso": "conso_eclairage_ef",
                "cout": "cout_eclairage",
                "ges": "emission_ges_eclairage",
            },
            "Auxiliaires": {
                "conso": "conso_auxiliaires_ef",
                "cout": "cout_auxiliaires",
                "ges": "emission_ges_auxiliaires",
            },
        }

        # Radio button filter
        usages = ["Chauffage", "ECS", "Refroidissement", "Eclairage", "Auxiliaires"]
        selected_usage = st.radio("Choisir le type de consommation", usages)

        # Get the correct columns
        conso_col = usage_map[selected_usage]["conso"]
        cout_col = usage_map[selected_usage]["cout"]
        ges_col = usage_map[selected_usage]["ges"]

        col1, col2, col3 = st.columns([0.5, 0.25, 0.25])
        # satistics table
        with col1:
            summary_df = pd.DataFrame(
                {
                    "Consommation (kWep/an)": [
                        filtered_df[conso_col].mean(),
                        filtered_df[conso_col].std(),
                        filtered_df[conso_col].min(),
                        filtered_df[conso_col].max(),
                    ],
                    "Émission GES (kgCO₂/an)": [
                        filtered_df[ges_col].mean(),
                        filtered_df[ges_col].std(),
                        filtered_df[ges_col].min(),
                        filtered_df[ges_col].max(),
                    ],
                    "Coût (€)": [
                        filtered_df[cout_col].mean(),
                        filtered_df[cout_col].std(),
                        filtered_df[cout_col].min(),
                        filtered_df[cout_col].max(),
                    ],
                },
                index=["Moyenne", "Écart-type", "Min", "Max"],
            ).round(2)

            st.write(f"Consommation d'énergie : {selected_usage}")
            st.dataframe(summary_df)

        # Gauge Conso
        with col2:
            total_conso_sum = filtered_df["conso_5_usages_ef"].sum()
            usage_sum = filtered_df[conso_col].sum()
            prop = usage_sum / total_conso_sum * 100

            # Simple gauge
            fig = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=prop,
                    number={"suffix": "%"},
                    title={
                        "text": f"Contribution de {selected_usage} <br> à la consommation énergétique",
                        "font": {"size": 14},
                    },
                    gauge={
                        "axis": {"range": [0, 100], "showticklabels": False},
                        "bar": {"color": "#B22222"},
                    },
                )
            )

            # Adjust size
            fig.update_layout(
                height=250,  # smaller height
                width=250,  # optional: smaller width
                margin={"t": 60, "b": 20, "l": 20, "r": 20},  # reduce extra space
            )

            st.plotly_chart(fig, width="stretch")

        # Gauge émission GES
        with col3:
            total_ges_sum = filtered_df["emission_ges_5_usages"].sum()

            # Somme de l'usage sélectionné (chauffage, ecs, etc.)
            usage_ges_sum = filtered_df[ges_col].sum()

            # Calcul du pourcentage
            prop_ges = usage_ges_sum / total_ges_sum * 100

            # Simple gauge pour les émissions GES
            fig_ges = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=prop_ges,
                    number={"suffix": "%"},
                    title={
                        "text": f"Contribution de {selected_usage} <br> aux émissions GES",
                        "font": {"size": 14},
                    },
                    gauge={
                        "axis": {"range": [0, 100], "showticklabels": False},
                        "bar": {"color": "#AB63FA"},
                    },
                )
            )

            # Adjust size
            fig_ges.update_layout(
                height=250,  # smaller height
                width=250,  # optional: smaller width
                margin={"t": 60, "b": 20, "l": 20, "r": 20},  # reduce extra space
            )

            st.plotly_chart(fig_ges, width="stretch")

        st.divider()

        # ------------------------------------------------------------------------------------------
        # SCATTER PLOT
        st.subheader("Impact des variables sur la consommation énergétique")
        col1, col2 = st.columns([0.3, 0.7])
        with col1:
            numeric_cols = filtered_df.select_dtypes(include="number").columns.tolist()
            option = st.selectbox(
                "Choix du variable Y",
                numeric_cols,
            )
            st.write("Y = ", option)
        with col2:
            corr_value = filtered_df["conso_5_usages_ef"].corr(filtered_df[option])
            fig = px.scatter(
                filtered_df.sample(n=1000 if n > 1000 else n, random_state=42),
                x="conso_5_usages_ef",  # X is fixed as total consumption
                y=option,
                labels={
                    "conso_5_usages_ef": "Consommation Totale (kWep/m²/an)",
                    option: option,
                },
                title=f"Relation entre Consommation énergétique et {option} (Corrélation = {corr_value:.2f})",
            )

            st.plotly_chart(fig, width="stretch")

else:
    st.info("⬆️ Please upload a dataset to get started.")
