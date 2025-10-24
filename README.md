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


## Project structure
```
mon_projet/
│
├── app.py                     # Main streamlit app launcher.
├── requirements.txt
├── README.md
├── pyproject.toml
├── uv.lock
├── .python-version
│
├── pages/                     # Pages from streamlit.
│   ├── 1_Visualisation.py
│   ├── 2_Modele_ML.py
│   └── 3_Analyse_API.py
│
├── src/                       # Main code.
│   ├── data_requesters        # Requesters for data on external APIs.
│   │   ├── api_requesters.py
│   │   └── helper.py
│   └── api.py/                # FastAPI routes for the application.
│       └── main.py            # main FastAPI file to run the back-end API routes.
│
├── MLmodels/                  # trained ml models.
│   ├── model1.pkl
│   └── ...
├── assets/                    # assets for streamlit app.
├── data/                      # data storage (will contains a sample for test).
└── notebooks/                 # ipython noteboks for exploration.                     
```

## Links
- [📊 Data exploration and models building](https://github.com/4xel-C/SISE_Enedis_ML_Study): Data exploration have been separated in another repository to avoid overloading main application from model preparations and explorations.
