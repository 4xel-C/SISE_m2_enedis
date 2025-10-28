import pickle

import numpy as np
import pandas as pd
from models.input_model import InputData

from services import BASE_DIR

FEATURES_PATH = BASE_DIR / "MLmodels" / "pipeline_xgboost_classification.pkl"


def prepare_data(input_data: InputData) -> np.ndarray:
    # Import the features list.
    with open(FEATURES_PATH, "rb") as f:
        # Load the features list.
        features_list = pickle.load(f)

        # From the location, get the corresponding features.
        city = input_data.Location.upper()

        cities_df = pd.read_csv(BASE_DIR / "data" / "cities_features.csv")

        # Get the city from the datalist.

    # Convert the input data into a NumPy array for the model
    data = np.array(
        [
            input_data.Location,
            input_data.cost,
            input_data.area,
            input_data.n_floors,
            input_data.age,
            input_data.main_heating_energy,
            input_data.building,
        ]
    )
    return data
