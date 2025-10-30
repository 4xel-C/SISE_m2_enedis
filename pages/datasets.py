from pathlib import Path

import pandas as pd
import streamlit as st

from src.data_requesters import Ademe_API_requester
from src.processing.data_cleaner import DataCleaner

# General configuration
st.set_page_config(page_title="DPE Map & Statistics", page_icon="🗺️", layout="wide")

# === Path to CSV Files ===
DATASETS_DIR = Path(__file__).parent.parent / "data" / "datasets"


st.title("📂 Manage your Datasets")

# Main tabs
(
    tab1,
    tab2,
) = st.tabs(["🧮 Your Datasets", "🛜 Download new data"])

# === File uploader ===

# === Dataset manager ===

with tab1:
    pass


# === ADEME API Import ===
with tab2:
    st.header("🌐 Import new department Data from ADEME API")
    type_bat = st.radio("Building type:", ["Existing", "New"], horizontal=True)
    neuf = type_bat == "New"

    departement = st.text_input("Department code (e.g.: 75, 13, 59...)", "33")
    limit = st.number_input("Maximum number to retrieve", 100, 10_000, 1000, step=500)
    size = st.slider("API batch size (size)", 100, 2500, 500, step=100)

    fetch_api = st.button("🚀 Fetch from ADEME API")

    # Define progress elements
    if st.session_state.get("data_api", None) is None:
        progress_bar = st.progress(0.0)
        status_text = st.empty()
    else:
        progress_bar = st.progress(1.0)
        status_text = st.text("Data already loaded in session.")

    @st.cache_data
    def load_csv(files):
        dfs = []
        for f in files:
            df = pd.read_csv(f)
            dfs.append(df)
        return pd.concat(dfs, ignore_index=True)

    # === Load Data ===
    def progress_cb(current: int, total: int) -> None:
        frac = (current / total) if total else 0.0
        progress_bar.progress(min(1.0, frac))
        status_text.text(f"Retrieved {current:,} / {total:,}")

    def load_api(neuf: bool, limit: int, departement: str, size: int):
        requester = Ademe_API_requester(size=size)
        data_api = requester.custom_lines_request(
            neuf=neuf,
            limit=limit,
            progress_callback=progress_cb,
            qs=f"code_departement_ban:{departement}",
        )
        return pd.DataFrame(data_api)

    data_api = st.session_state.get("data_api", None)

    if fetch_api:
        data_api = load_api(neuf, limit, departement, size)
        if not data_api.empty:
            # have to add construction year if new building because API does not provide it
            # if neuf and "annee_construction" not in data_api.columns:
            #     current_year = datetime.datetime.now().year
            #     data_api["annee_construction"] = current_year

            cleaner_api = DataCleaner(data_api)
            data_api = cleaner_api.clean_all()
            st.session_state.data_api = data_api
        else:
            st.warning("⚠️ No data returned from ADEME API.")
            st.session_state.data_api = None

        data_api = st.session_state.data_api

    if data_api is not None:
        new = data_api["age_batiment"].sum() == 0

        dep = data_api["code_departement_ban"].iloc[0]

        st.success(
            f"✅ Data for {"new" if new else "existing"} housing for department {dep} loaded and processed successfully: {len(data_api)} rows."
        )

        st.write(data_api.head(5))

        col1, col2 = st.columns(2)

        with col1:
            st.download_button(
                "💾 Download result API (CSV)",
                data=data_api.to_csv(index=False).encode("utf-8"),
                file_name=f"dpe_ademe_{dep}_{'new' if neuf else 'existing'}.csv",
                mime="text/csv",
            )
        with col2:
            file_path = DATASETS_DIR / f"data_{dep}.csv"

            action = st.session_state.get("action", "Replace")

            if st.button("➕ Add to your datasets"):
                if file_path.exists():
                    if action == "Replace":
                        data_api.to_csv(file_path, index=False)
                        st.success(f"✅ File `{file_path.name}` replaced.")

                    elif action == "Concat & Overwrite":
                        existing_df = pd.read_csv(file_path, low_memory=False)

                        combined_df = pd.concat(
                            [existing_df, data_api], ignore_index=True
                        ).drop_duplicates()

                        combined_df.to_csv(file_path, index=False)

                        st.success(
                            f"✅ File `{file_path.name}` updated by concatenation."
                        )

                else:
                    data_api.to_csv(
                        file_path,
                        index=False,
                    )

            if file_path.exists():
                st.warning(f"⚠️ Data for department `{dep}` already exists.")
                # Display a radio button to choose action
                action = st.radio(
                    "File exists: choose action",
                    options=["Replace", "Concat & Overwrite"],
                    index=0,
                )
                st.session_state.action = action
