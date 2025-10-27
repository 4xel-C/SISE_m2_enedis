import pandas as pd
import streamlit as st

from src.data_requesters import api_ademe

# Configuration de la page
st.set_page_config(page_title="Requête ADEME", page_icon="🌐", layout="wide")

st.title("🌐 Requêtes vers l’API ADEME")
st.markdown("""
Cette page permet de récupérer des données depuis **l’API ADEME (DPE)** en affichant **la progression en temps réel**.  
Les données sont téléchargées par paquets, pour éviter les longs temps d’attente bloquants.
""")

# Paramètres de la requête
st.header("🔧 Paramètres de la requête")

type_bat = st.radio("Type de bâtiments :", ["Existants", "Neufs"], horizontal=True)
neuf = type_bat == "Neufs"

departement = st.text_input("Code du département (ex: 75, 13, 59, etc.)", "33")
limit = st.number_input("Nombre maximal à récupérer", 100, 10_000, 1000, step=500)
size = st.slider("Taille des paquets API (size)", 100, 2500, 500, step=100)

launch = st.button("🚀 Lancer la requête", use_container_width=True)

# Lancement de la requête
if launch:
    st.info(
        f"⏳ Requête en cours vers l’API ADEME pour le département {departement}..."
    )
    requester = api_ademe

    progress_bar = st.progress(0)
    status_text = st.empty()
    data_preview = st.empty()

    all_data = []
    try:
        # --- Étape 1 : connaître le nombre total à récupérer
        url = (
            requester._Ademe_API_requester__base_url_existant
            if not neuf
            else requester._Ademe_API_requester__base_url_neuf
        )
        url += "/lines"
        params = {"qs": f"code_departement_ban:{departement}", "size": size}

        total_length = requester._Ademe_API_requester__get_length(url, params=params)
        if limit:
            total_length = min(limit, total_length)

        if total_length == 0:
            st.warning("Aucune donnée trouvée pour ce département.")
            st.stop()

        status_text.text(f"Total à récupérer : {total_length:,} lignes")
        next_url = url
        fetched = 0
        params = params.copy()

        # --- Étape 2 : récupération progressive
        while next_url and fetched < total_length:
            data_chunk = requester._Ademe_API_requester__get_data(
                next_url, params=params
            )
            if not data_chunk:
                break

            results = data_chunk.get("results", [])
            all_data.extend(results)
            fetched += len(results)

            # Mettre à jour le progrès
            progress = min(fetched / total_length, 1.0)
            progress_bar.progress(progress)
            status_text.text(
                f"Récupéré {fetched:,}/{total_length:,} ({progress * 100:.1f}%)"
            )

            # Aperçu live toutes les 2 secondes
            if fetched % (2 * size) < size and len(all_data) > 0:
                df_preview = pd.DataFrame(all_data[-min(len(all_data), 50) :])
                data_preview.dataframe(df_preview, use_container_width=True, height=250)

            next_url = data_chunk.get("next")
            params = None

            if fetched >= total_length:
                break

        # --- Étape 3 : affichage final
        df = pd.DataFrame(all_data)
        st.success(
            f"✅ Téléchargement terminé — {len(df):,} enregistrements récupérés."
        )
        st.dataframe(df.head(50), use_container_width=True)

        # Statistiques rapides
        if "etiquette_dpe" in df.columns:
            st.markdown("### 🏠 Répartition des classes DPE")
            st.bar_chart(df["etiquette_dpe"].value_counts().sort_index())

        st.download_button(
            "💾 Télécharger le résultat (CSV)",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name=f"dpe_ademe_{departement}_{'neuf' if neuf else 'existant'}.csv",
            mime="text/csv",
        )

    except Exception as e:
        st.error(f"❌ Erreur lors de la requête : {e}")
        st.stop()

else:
    st.info(
        "🪄 Configurez les paramètres et cliquez sur **🚀 Lancer la requête** pour démarrer."
    )
