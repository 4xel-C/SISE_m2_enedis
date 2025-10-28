"""
# Accueil
"""

import streamlit as st

# ⚙️ Configuration générale
st.set_page_config(
    page_title="DPE Ademe & Enedis - Accueil", page_icon="🏠", layout="centered"
)

# 🏠 Titre et description
st.title("🏠 Tableau de Bord DPE - Ademe & Enedis")
st.markdown("""
Bienvenue sur l’application **DPE Ademe**, un outil interactif pour :
- Explorer les **données énergétiques des logements** (ADEME, Enedis),
- Visualiser les **cartes dynamiques** par zone géographique,
- **Prédire la classe DPE** d’un logement grâce à vos modèles de Machine Learning.
- Requêter des données depuis l’**API ADEME** pour enrichir votre analyse.

Sélectionnez une page ci-dessous pour commencer :
""")

st.divider()

# 🔗 Liens vers les pages
col1, col2, col3 = st.columns(3)


with col1:
    st.page_link(
        "pages/data.py",
        label="Explorer la carte et les stats DPE",
        icon="📊",
    )
    st.markdown("""
    Visualisez jusqu’à plusieurs centaines de milliers de logements sur une **carte interactive**.
    Filtrez par région, département ou classe énergétique.\n
    Et explorez rapidement les caractéristiques principales de votre dataset : distributions, valeurs manquantes et statistiques descriptives pour mieux comprendre vos données.
    """)

with col2:
    st.page_link("pages/prediction.py", label="Prédire la classe DPE", icon="🔮")
    st.markdown("""
    Utilisez vos **modèles de prédiction (.pkl)** pour estimer la **classe DPE (A → G)** 
    à partir des caractéristiques du logement.
    """)

with col3:
    st.page_link("pages/api_requests.py", label="Requêtes vers l’API ADEME", icon="🌐")
    st.markdown("""
    Récupérez des données depuis **l’API ADEME (DPE)**.
    """)

st.divider()

# 🧩 Section d’informations complémentaires
with st.expander("ℹ️ À propos de l’application"):
    st.markdown("""
    - **Auteur :** Thibaud  
    - **Sources de données :** [ADEME - DPE](https://data.ademe.fr) & [Enedis Open Data](https://data.enedis.fr)  
    - **Technologies :** Streamlit, Pydeck, Scikit-Learn  
    - **Dernière mise à jour :** Octobre 2025  
    """)

st.caption(
    "💡 Astuce : utilisez la barre latérale gauche pour naviguer entre les pages."
)
