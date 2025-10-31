import streamlit as st
import os
import pickle
import joblib
import numpy as np
import time
from sklearn.metrics import r2_score, mean_squared_error, accuracy_score
from sklearn.preprocessing import OneHotEncoder
from src.utils.dataloader import generate_file_selector

MODELS_DIR = "./MLmodels/"

# helpers
def load_model(path):
    return joblib.load(path)

def save_model(obj, path):
    joblib.dump(obj, path)

def rmse_score(y_true, y_pred):
    """Compute RMSE safely (compatible with older sklearn versions)."""
    try:
        return mean_squared_error(y_true, y_pred, squared=False)
    except TypeError:
        return np.sqrt(mean_squared_error(y_true, y_pred))

def diff_icon(new, old, higher_is_better=True):
    """Display an icon depending on metric improvement."""
    if old is None:
        return ""
    if new == old:
        return "➖"
    if (new > old and higher_is_better) or (new < old and not higher_is_better):
        return "✅🔼"
    else:
        return "⚠️🔽"

def make_pipeline_tolerant_inplace(pipeline):
    """
    Modify the pipeline *in place* so that all OneHotEncoders
    have handle_unknown='ignore', even inside sub-pipelines.
    """
    def update_encoder(transformer):
        if isinstance(transformer, OneHotEncoder):
            transformer.handle_unknown = "ignore"
        elif hasattr(transformer, "steps"):
            for _, step_obj in transformer.steps:
                update_encoder(step_obj)

    preprocessor = pipeline.named_steps.get("preprocessor", None)
    if preprocessor is not None:
        for _, transformer, _ in preprocessor.transformers:
            update_encoder(transformer)

    return pipeline

def filter_dataset_for_original(df, pipeline, features):
    """
    Filter dataset to remove rows with unknown categories for original models
    (useful only for evaluation of non-tolerant models).
    """
    df_filtered = df.copy()
    unknowns = {}

    while True:
        try:
            pipeline.named_steps["preprocessor"].transform(df_filtered[features])
            break
        except ValueError as e:
            msg = str(e)
            if "Found unknown categories" in msg:
                bad_cat = msg.split("['")[1].split("']")[0]
                if "in column" in msg:
                    col_part = msg.split("in column")[1].strip().split()[0]
                    bad_col = features[int(col_part)] if col_part.isdigit() else col_part
                else:
                    bad_col = features[0]
                unknowns.setdefault(bad_col, []).append(bad_cat)
                df_filtered = df_filtered[df_filtered[bad_col] != bad_cat]
            else:
                raise e
    return df_filtered, unknowns

# Interface
st.title("🔄 Retrain regression and classification models")
st.caption("Training may take several minutes depending on dataset size ⏳")
st.write("Select a dataset in the **sidebar**, then click the button to retrain both models on the new data.")

# Sidebar dataset selector
with st.sidebar:
    st.header("📂 Dataset selection")
    generate_file_selector(sidebar=True)

df = st.session_state.get("df", None)
if df is None:
    st.info("⬅️ Please select a dataset in the sidebar.")
    st.stop()

st.success(f"Dataset loaded: {st.session_state.get('last_file', '')}")
st.write(f"Rows: {len(df)}")
st.dataframe(df.head())

if st.button("🚀 Retrain models"):
    with st.spinner("Processing..."):
        # Load features and targets info
        with open(os.path.join(MODELS_DIR, "features_target_columns_regression.pkl"), "rb") as f:
            reg_info = pickle.load(f)
        with open(os.path.join(MODELS_DIR, "features_target_columns_classification.pkl"), "rb") as f:
            clf_info = pickle.load(f)

        reg_features = reg_info["quantitative_features"] + reg_info["qualitative_features"]
        reg_target = reg_info["target"]
        clf_features = clf_info["quantitative_features"] + clf_info["qualitative_features"]
        clf_target = clf_info["target"]

        # Regression
        with st.spinner("Training regression model..."):
            start = time.time()

            reg_pipeline_orig = load_model(os.path.join(MODELS_DIR, "pipeline_best_regression.pkl"))
            X_reg, y_reg = df[reg_features], df[reg_target]

            # Evaluate original model (with filtering to avoid errors)
            df_reg_filtered, unknowns_reg = filter_dataset_for_original(df, reg_pipeline_orig, reg_features)
            if unknowns_reg:
                st.warning(f"Regression: {len(df) - len(df_reg_filtered)} rows ignored for original model "
                           f"(unknown categories: {unknowns_reg})")

            if len(df_reg_filtered) > 0:
                X_reg_f, y_reg_f = df_reg_filtered[reg_features], df_reg_filtered[reg_target]
                y_pred_orig = reg_pipeline_orig.predict(X_reg_f)
                metrics_reg_orig = {"R2": r2_score(y_reg_f, y_pred_orig),
                                    "RMSE": rmse_score(y_reg_f, y_pred_orig)}
            else:
                metrics_reg_orig = {"R2": None, "RMSE": None}

            # Retrain model (tolerant to unknown categories)
            reg_pipeline_retrained = load_model(os.path.join(MODELS_DIR, "pipeline_best_regression.pkl"))
            make_pipeline_tolerant_inplace(reg_pipeline_retrained)
            reg_pipeline_retrained.fit(X_reg, y_reg)

            retrain_reg_path = os.path.join(MODELS_DIR, "pipeline_best_regression_retrained.pkl")
            save_model(reg_pipeline_retrained, retrain_reg_path)

            y_pred_new = reg_pipeline_retrained.predict(X_reg)
            metrics_reg_new = {"R2": r2_score(y_reg, y_pred_new),
                               "RMSE": rmse_score(y_reg, y_pred_new)}

            duration = time.time() - start
            st.success(f"✅ Regression retrained in {duration/60:.2f} min (tolerant to unseen categories)")

            st.subheader("📊 Regression comparison")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Original**")
                st.write(metrics_reg_orig)
            with col2:
                st.markdown("**Retrained**")
                st.write({
                    "R2": f"{metrics_reg_new['R2']:.4f} {diff_icon(metrics_reg_new['R2'], metrics_reg_orig['R2'], True)}",
                    "RMSE": f"{metrics_reg_new['RMSE']:.2f} {diff_icon(metrics_reg_new['RMSE'], metrics_reg_orig['RMSE'], False)}"
                })

        # Classification
        with st.spinner("Training classification model..."):
            start = time.time()

            clf_pipeline_orig = load_model(os.path.join(MODELS_DIR, "pipeline_xgboost_classification.pkl"))
            label_encoder = joblib.load(os.path.join(MODELS_DIR, "label_encoder_target.pkl"))
            X_clf, y_clf = df[clf_features], df[clf_target]
            y_clf_encoded = label_encoder.transform(y_clf)

            df_clf_filtered, unknowns_clf = filter_dataset_for_original(df, clf_pipeline_orig, clf_features)
            if unknowns_clf:
                st.warning(f"Classification: {len(df) - len(df_clf_filtered)} rows ignored for original model "
                           f"(unknown categories: {unknowns_clf})")

            if len(df_clf_filtered) > 0:
                X_clf_f, y_clf_f = df_clf_filtered[clf_features], df_clf_filtered[clf_target]
                y_pred_orig_encoded = clf_pipeline_orig.predict(X_clf_f)
                y_pred_orig = label_encoder.inverse_transform(y_pred_orig_encoded)
                metrics_clf_orig = {"Accuracy": accuracy_score(y_clf_f, y_pred_orig)}
            else:
                metrics_clf_orig = {"Accuracy": None}

            clf_pipeline_retrained = load_model(os.path.join(MODELS_DIR, "pipeline_xgboost_classification.pkl"))
            make_pipeline_tolerant_inplace(clf_pipeline_retrained)
            clf_pipeline_retrained.fit(X_clf, y_clf_encoded)

            retrain_clf_path = os.path.join(MODELS_DIR, "pipeline_xgboost_classification_retrained.pkl")
            save_model(clf_pipeline_retrained, retrain_clf_path)

            y_pred_new_encoded = clf_pipeline_retrained.predict(X_clf)
            y_pred_new = label_encoder.inverse_transform(y_pred_new_encoded)
            metrics_clf_new = {"Accuracy": accuracy_score(y_clf, y_pred_new)}

            duration = time.time() - start
            st.success(f"✅ Classification retrained in {duration/60:.2f} min (tolerant to unseen categories)")

            st.subheader("📊 Classification comparison")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Original**")
                st.write(metrics_clf_orig)
            with col2:
                st.markdown("**Retrained**")
                st.write({
                    "Accuracy": f"{metrics_clf_new['Accuracy']:.4f} "
                                f"{diff_icon(metrics_clf_new['Accuracy'], metrics_clf_orig['Accuracy'], True)}"
                })

    st.success("🎉 All models retrained successfully and are now tolerant to unseen categories.")
