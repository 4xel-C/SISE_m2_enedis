# ⚡ ml-enedis: Master SISE Project

![Python version](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
![Streamlit version](https://img.shields.io/badge/Streamlit-1.50-orange?logo=streamlit&logoColor=white)
![Scikit-learn version](https://img.shields.io/badge/scikit--learn-1.7.2-orange?logo=scikit-learn&logoColor=white)

## 🧠 Introduction

This repository hosts a complete **web application** that provides an interface for **data analysis**, **dataset management**, and **prediction** using **pretrained machine learning models**. The application predicts:

- **Total annual energy cost** of a house or apartment
- ⚡ **DPE classification** (Energy Performance Diagnosis)

The **DPE classification** is a 7-level label ranging from **A** (most energy efficient) to **G** (least efficient). It is a crucial criterion when selling or renting properties, with regulatory restrictions for low-performing buildings. Our goal is to predict this classification using easily accessible input data through a simple web form, avoiding the need for detailed technical measurements.

Since the DPE label is closely linked to total energy costs, the project also includes a **regression model** to predict the annual energy expenditure. Together, these form a **two-model prediction pipeline**.

This project was developed by **four Master SISE students** and concludes the Python and Machine Learning lessons of the program.

> [!NOTE]
> All the preliminary data explorations, models testing and devlopment are findable in the following repository: [📊 Data exploration and models building](https://github.com/4xel-C/SISE_Enedis_ML_Study)

---

## ⚙️ Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/cyrizon/ml-enedis.git
cd ml-enedis
```

### 2️⃣ Install dependencies

#### Option A: Run with Docker Compose (Recommended)

**Prerequisites:** Docker and Docker Compose installed.

1. Create a `.env` file in the project root:

```bash
MAPBOX_API_KEY=your_mapbox_api_key_here
```

2. Build and run the application:

```bash
docker-compose up -d
```

3. Access the application:

   - 🌐 Streamlit UI: http://localhost:8501
   - 🔌 FastAPI Backend: http://localhost:8000

4. Stop the application:

```bash
docker-compose down
```

#### Option B: Run locally

**Prerequisite:** Python 3.13 installed.

- **Using UV package manager**

```bash
uv sync
```

- **Without UV**

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

### With Docker Compose

The application starts automatically when you run `docker-compose up -d`. Access it at http://localhost:8501.

### Running locally

1. Run the web app:

```bash
streamlit run home.py
```

2. (Optional) Run the FastAPI backend in a separate terminal:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

3. Open your browser to interact with the app.
4. Go to the prediction menu, fill in the form with your property's details to get predictions for:
   - 🏠 Total annual energy cost
   - ⚡ DPE classification

---

````

### 2️⃣ Install dependencies
**Prerequisite:** Python 3.13 installed.

- **Using UV package manager**
```bash
uv sync
````

- **Without UV**

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

1. Run the web app locally:

```bash
streamlit run Home.py
```

2. Open your browser to interact with the app.
3. Go to the prediction menu, fill in the form with your property’s details to get predictions for:
   - 🏠 Total annual energy cost
   - ⚡ DPE classification

---

## 📊 Features

- 🏠 Predict DPE labels (A–G)
- 💰 Predict total annual energy cost
- 📈 Interactive web interface with dashboard and map
- 🔍 Data exploration and visualization built-in
- 🛜 Download and update datasets

---

## 🛠 Tech Stack

This project leverages the following technologies and libraries:

- **Python** – Core programming language for the application.
- **Streamlit** – Web application framework for interactive UI.
- **FastAPI** – Backend API framework for handling requests and predictions.
- **Pydantic** – Data validation and schema definition for API inputs.
- **Pandas** – Data manipulation and preprocessing.
- **Scikit-learn** – Machine learning models, pipelines, and preprocessing.
- **Plotly** – Interactive visualizations and dynamic plots.

---

## 🗂 Project Structure

```
ml-enedis/
├─ home.py                   # Streamlit app launcher
├─ pages/                    # Streamlit multi-page interface
│  ├─ data.py
│  ├─ context.py
│  ├─ datasets.py
│  ├─ map.py
│  └─ prediction.py
├─ assets/                   # Images and icons for app
├─ MLModels/                 # Pretrained machine learning models and encoders
│  ├─ features_target_columns_classification.pkl
│  ├─ features_target_columns_regression.pkl
│  ├─ label_encoder_target.pkl
│  ├─ pipeline_best_regression.pkl
│  └─ pipeline_sgboost_classification.pkl
├─ data/                     # Raw and processed data
│  ├─ climate_zones.csv
│  ├─ communes-france-2025.csv
│  └─ datasets/              # Specific datasets
│     └─ data_69.csv
├─ doc/                      # Documentation
│  ├─ DOC_FONCTIONNELLE.md
│  ├─ DOC_TECHNIQUE.md
│  └─ RAPPORT.md
├─ backend/                  # FastAPI backend
│  ├─ main.py                # API launcher
│  ├─ models/                # Pydantic input validation models
│  │  └─ input_model.py
│  └─ services/              # Backend services for data prep and predictions
│     ├─ data_preparation.py
│     └─ prediction.py
└─ src/                      # Supporting Python modules
   ├─ data_requesters/      # Data fetching modules
   │  ├─ ademe.py
   │  ├─ base_api.py        # ABC class for API requests
   │  ├─ elevation.py
   │  ├─ enedis.py
   │  ├─ geo_features.py
   │  └─ helper.py
   ├─ processing/           # Data processing modules
   │  └─ data_cleaner.py
   └─ utils/                # Utilities for loading and selecting files
      ├─ dataloader.py
      └─ file_selector.py    # Streamlit file selector
```

## 📈 Datasources

- **ADEME API opendata:**
  - **[`Existing housing`](https:\data.ademe.fr\datasets\dpe03existant)**: Exhaustive data on housing specificities.
  - **[`Recent housing`](https://data.ademe.fr/datasets/dpe03existant)**: Exhaustive on recent housing specificities.
- **datagouv opendata:**
  - **[`French cities dabase`](https://www.data.gouv.fr/datasets/communes-et-villes-de-france-en-csv-excel-json-parquet-et-feather)**: Coordinates and information concerning all cities in France.
  - **[`Elevation API`](https://www.data.gouv.fr/reuses/elevation-api/)**: Used to provide the altitude of specific coordinates.
  - **[`Climate Zones`](https://www.ecologie.gouv.fr/sites/default/files/documents/La%20r%C3%A9partition%20des%20d%C3%A9partements%20par%20zone%20climatique.pdf)**: Provide climate zone for each department in France.
  - **[`Cities Geolocalisation`](https://data.geopf.fr/geocodage/search)**: Geocoding cities by their INSEE code.
  - **[`Cities informations`](https://geo.api.gouv.fr/communes)**: Open API providing complementary information about cities, mainly used to search by name and get the INSEE code for geolocalisation and altitude.

---

<img width="2181" height="1126" alt="image" src="https://github.com/user-attachments/assets/43cc255b-d267-498b-854c-35477353ea1c" />

<img width="2120" height="850" alt="image" src="https://github.com/user-attachments/assets/f91c6bac-559b-427a-a844-3f6baf92a687" />

---
