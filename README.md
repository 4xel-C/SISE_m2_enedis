# ml-enedis
Application permettant l'évaluation du DPE et de la consommation énergétique d'un logement.

## Démo

<u>TODO</u>

## Installation

Pour installer ce projet, suivez les étapes ci-dessous :

1. **Cloner le dépôt** :
```sh
git clone https://github.com/cyrizon/ml-enedis.git
```

2. **Installer les dépendances** :

**Pré-requis :** Python 3.13 installé.

- *Avec le gestionnaire de package UV :*
```sh
uv sync
```

- *Sans UV :*
```sh
pip install -r requirements.txt
```

3. **Lancer l'application**:

<u>TODO</u>
pour l'instant il faut écrire cette commande dans un terminal python

- *Avec le gestionnaire de package UV :*
```sh
uv run streamlit run home.py
```

- *Sans UV :*
```sh
streamlit run home.py
```

## Project structure
```
mon_projet/
│
├── home.py                                          # Main streamlit app launcher.
├── requirements.txt
├── README.md
├── pyproject.toml
├── uv.lock
├── .python-version
│
├── .streamlit       # À créer
│   └── secrets.toml # Fichier contenant votre clé API publique MapBox : MAPBOX_API_KEY= "..."
│                    # Utilisé pour des arrières plan de carte
│
├── pages/                                          # Pages from streamlit.
│   ├── data.py
│   ├── prediction.py
│   └── api_requests.py
│
├── src/                                            # Main code.
│   ├── data_requesters                             # Requesters for data on external APIs.
│   │   ├── ademe.py                                
│   │   ├── elevation.py                            
│   │   ├── enedis.py
│   │   ├── geo_features.py
│   │   └── helper.py
│   └── api.py/                                     # FastAPI routes for the application.
│       └── main.py                                 # main FastAPI file to run the back-end API routes.
│
├── MLmodels/                                       # trained ml models.
│   ├── pipeline_xgboost_classification.pkl         # Classification model.
│   ├── label_encoder_target.pkl                    # Label encoder for target.
|   └── features_target_columns.pkl                 # Features infos.
|
├── assets/                                         # assets for streamlit app.
├── data/                                           # data storage (will contains a sample for test).
└── notebooks/                                      # ipython noteboks for exploration.                     
```

## Links
- [📊 Data exploration and models building](https://github.com/4xel-C/SISE_Enedis_ML_Study): Data exploration have been separated in another repository to avoid overloading main application from model preparations and explorations.
