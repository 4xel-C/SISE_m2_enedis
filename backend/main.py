from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.input_model import InputData
from services.prediction import predict

app = FastAPI(title="ML Prediction API")

# Autoriser les appels depuis Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou spécifie ton domaine Streamlit
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/predict")
def predict_route(data: InputData):
    result = predict([data.feature1, data.feature2, data.feature3])
    return {"prediction": result}
