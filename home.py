"""
# Home
"""

from pathlib import Path

import streamlit as st

# === Pages path definition and Menu ===
PAGES_PATH = Path(__file__).parent / "pages"
ASSETS_PATH = Path(__file__).parent / "assets"

# === Menu Definition ===
pages = {
    "Project": [
        st.Page(PAGES_PATH / "intro.py", title="🏠 Home"),
        st.Page(PAGES_PATH / "context.py", title="📋 Context"),
    ],
    "Data": [
        st.Page(PAGES_PATH / "data.py", title="📊 Statistics & Visualizations"),
        st.Page(PAGES_PATH / "map.py", title="🗺️ DPE Map"),
        st.Page(PAGES_PATH / "datasets.py", title="🗃️ Dataset and Download"),
    ],
    "Prediction": [
        st.Page(PAGES_PATH / "prediction.py", title="🔮 Predict DPE Class"),
        st.Page(PAGES_PATH / "retrain_models.py", title="⚙️ Model Retraining"),
    ],
}

# === CSS For menu style ===
st.markdown(
    """
    <style>
    /* Categories style */
     [data-testid="stNavSectionHeader"] {
        font-size: 1.5rem !important;
        font-weight: 2300 !important;
        margin-top: 1.5rem !important;
        margin-bottom: 0.8rem !important;
        padding-left: 0.5rem !important;
    }
    
    /* Link style */
    [data-testid="stSidebarNav"] a {
        font-size: 1.05rem !important;
        font-weight: 500 !important;
    }
    
    /* Active page */
    [data-testid="stSidebarNav"] a[aria-current="page"] {
        background-color: rgba(255, 190, 0, 0.20) !important;
        border-left: 4px solid #FF4B4B !important;
        font-weight: 600 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


pg = st.navigation(pages)


pg.run()
