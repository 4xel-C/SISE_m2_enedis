import pandas as pd
import streamlit as st

from src.data_requesters import Ademe_API_requester

# ⚙️ Page configuration
st.set_page_config(page_title="ADEME Request", page_icon="🌐", layout="wide")

st.title("🌐 Requests to the ADEME API")
st.markdown("""
This page allows you to retrieve data from **the ADEME (DPE) API**  
with progress tracking and a preview of the retrieved data.
""")

# 🧭 User parameters
st.header("🔧 Request parameters")

type_bat = st.radio("Building type:", ["Existing", "New"], horizontal=True)
neuf = type_bat == "New"

departement = st.text_input("Department code (e.g.: 75, 13, 59...)", "33")
limit = st.number_input("Maximum number to retrieve", 100, 10_000, 1000, step=500)
size = st.slider("API batch size (size)", 100, 2500, 500, step=100)

launch = st.button("🚀 Launch request", width="stretch")

# 🚀 Request execution
if launch:
    st.info(f"⏳ Request in progress to the ADEME API for department {departement}...")

    requester = Ademe_API_requester(size=size)
    progress_bar = st.progress(0.0)
    status_text = st.empty()
    data_preview = st.empty()

    try:
        # Step 1: Retrieve data using the public method
        all_data = []
        status_text.text("Retrieving data...")

        # Progress callback used by the requester
        def progress_cb(current: int, total: int) -> None:
            frac = (current / total) if total else 0.0
            progress_bar.progress(min(1.0, frac))
            status_text.text(f"Retrieved {current:,} / {total:,}")

        # The custom_lines_request method allows setting a "limit" and a progress callback
        all_data = requester.custom_lines_request(
            neuf=neuf,
            limit=limit,
            progress_callback=progress_cb,
            qs=f"code_departement_ban:{departement}",
        )

        progress_bar.progress(1.0)
        status_text.text("Retrieval complete.")

        # Step 2: Convert to DataFrame
        if not all_data:
            st.warning("No data found for this department.")
            st.stop()

        df = pd.DataFrame(all_data)

        st.success(f"✅ Download complete — {len(df):,} records retrieved.")
        st.dataframe(df.head(50), width='stretch')

        # Step 3: Quick statistics
        if "etiquette_dpe" in df.columns:
            st.markdown("### 🏠 Distribution of DPE classes")
            st.bar_chart(df["etiquette_dpe"].value_counts().sort_index())

        # Step 4: CSV download
        st.download_button(
            "💾 Download result (CSV)",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name=f"dpe_ademe_{departement}_{'new' if neuf else 'existing'}.csv",
            mime="text/csv",
        )

    except Exception as e:
        st.error(f"❌ Error during request: {e}")
        st.stop()

else:
    st.info("🪄 Configure the parameters and click **🚀 Launch request** to start.")
