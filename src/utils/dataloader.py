from pathlib import Path

import pandas as pd
import streamlit as st

# ============================================================ #
# Loader for csv files in stream lit application with caching  #
# ============================================================ #


# === Path to CSV Files ===
DATASETS_DIR = Path(__file__).parent.parent.parent / "data" / "datasets"


# === Side bar files selection ===
csv_files = [f.name for f in DATASETS_DIR.glob("*.csv")]
print(csv_files)


@st.cache_data
def load_csv(path: Path) -> pd.DataFrame:
    """Function to cache loaded dataset.

    Args:
        path (Path): Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded DataFrame.
    """
    return pd.read_csv(path)


def generate_file_selector():
    """Generate a file selector in the sidebar and load the selected file into session state."""

    # Get the default index of the menu.
    default_index = (
        csv_files.index(st.session_state.last_file)
        if st.session_state.get("last_file", None)
        else 0
    )

    # Call back function.
    def load_selected_file():
        file_path = DATASETS_DIR / st.session_state.selected_file
        st.session_state.df = load_csv(file_path)
        st.session_state.last_file = st.session_state.selected_file
        st.sidebar.success(
            f"✅ Dataset `{st.session_state.selected_file}` successfully loaded"
        )

    # Selectbox avec on_change
    st.sidebar.selectbox(
        "**Select your dataset:**",
        ["Select a dataset"] + csv_files,
        index=default_index,
        key="selected_file",
        on_change=load_selected_file,
    )
