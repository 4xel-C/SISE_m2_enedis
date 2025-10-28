"""
# Home
"""

import streamlit as st

# ⚙️ General configuration
st.set_page_config(
    page_title="DPE Ademe & Enedis - Home", page_icon="🏠", layout="centered"
)

# 🏠 Title and description
st.title("🏠 DPE Dashboard - Ademe & Enedis")
st.markdown("""
Welcome to the **DPE Ademe** app, an interactive tool to:
- Explore **housing energy data** (ADEME, Enedis),
- Visualize **dynamic maps** by geographic area,
- **Predict the DPE class** of a home using your Machine Learning models,
- Request data from the **ADEME API** to enrich your analysis.

Select a page below to get started:
""")

st.divider()

# 🔗 Links to pages
col1, col2, col3 = st.columns(3)

with col1:
    st.page_link("pages/data.py", label="Explore the DPE map and statistics", icon="📊")
    st.markdown("""
    Visualize up to hundreds of thousands of homes on an **interactive map**.  
    Filter by region, department, or energy class.  
    Quickly explore the main characteristics of your dataset: distributions, missing values, and descriptive statistics to better understand your data.
    """)

with col2:
    st.page_link("pages/prediction.py", label="Predict DPE class", icon="🔮")
    st.markdown("""
    Use your **prediction models (.pkl)** to estimate the **DPE class (A → G)**  
    based on the home's characteristics.
    """)

with col3:
    st.page_link("pages/api_requests.py", label="Requests to the ADEME API", icon="🌐")
    st.markdown("""
    Retrieve data from the **ADEME (DPE) API**.
    """)

st.divider()

# 🧩 Additional information section
with st.expander("ℹ️ About the application"):
    st.markdown("""
    - **Author:** Thibaud  
    - **Data sources:** [ADEME - DPE](https://data.ademe.fr) & [Enedis Open Data](https://data.enedis.fr)  
    - **Technologies:** Streamlit, Pydeck, Scikit-Learn  
    - **Last update:** October 2025  
    """)

st.caption("💡 Tip: use the left sidebar to navigate between pages.")
