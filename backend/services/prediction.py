import joblib
from fastapi import HTTPException

from backend.models.input_model import InputData
from backend.services import BASE_DIR
from backend.services.data_prepartion import prepare_data

MODEL_PATH = BASE_DIR / "MLmodels" / "pipeline_xgboost_classification.pkl"
ENCODER_PATH = BASE_DIR / "MLmodels" / "label_encoder_target.pkl"


def load_pipeline():
    return joblib.load(MODEL_PATH)


def load_label_encoder():
    return joblib.load(ENCODER_PATH)


def predict_classification(features: InputData) -> dict:
    # ---- Prepare data
    X_input = prepare_data(features)

    # If we couldn't retrive geographical features, return an error.
    if X_input is None:
        raise HTTPException(
            status_code=400,
            detail="❌ Unable to retrieve geographical features for the provided city/INSEE code.",
        )

    # load the pipeline and the model
    pipeline_model = load_pipeline()
    label_encoder = load_label_encoder()

    # ---- Prediction
    try:
        y_pred_int = pipeline_model.predict(X_input)
        y_pred_label = label_encoder.inverse_transform(y_pred_int)

        return {"prediction": y_pred_label[0]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
