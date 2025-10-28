import os
import pickle

from services import BASE_DIR

MODEL_PATH = BASE_DIR / "MLmodels" / "pipeline_xgboost_classification.pkl"

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)


def predict(features: list[float]) -> float:
    prediction = model.predict([features])
    return float(prediction[0])
