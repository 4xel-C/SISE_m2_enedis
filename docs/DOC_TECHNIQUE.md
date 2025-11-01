# Technical Documentation

## Application Architecture 
The application uses a modular, __Python-based architecture__ that separates the frontend interface, backend, machine learning models, and data processing scripts. This makes the system easy to maintain, scale, and extend. The entire stack runs in __Docker__ containers, which ensures consistent deployment and environment reproducibility across different systems.

![architecture](https://github.com/user-attachments/assets/62239f77-1c6e-4a45-94ad-25d5c8df27eb)

The system is composed of several main components:
### 1. Frontend (Streamlit)
The __Streamlit interface__ serves as the main entry point where users interact with the system. It's a simple web interface that brings together data visualization, analysis, model training, and predictions all in one place. Users can navigate between different pages like Home, Context, Data, Datasets, Map, Retrain Models, and Prediction. When users make selections or requests, the interface sends those to the backend to fetch data or generate predictions.

### 2. Backend (FastAPI)
The __FastAPI backend__ provides the API layer connecting the frontend to ML models and data services. It exposes REST endpoints like `/predict` to handle requests from Streamlit, coordinates communication between components, and returns predictions and processed data.

### 3. Machine Learning Models 
This module contains the trained machine learning components used for energy prediction and DPE classification. It includes:
- 🧠 __XGBoost__ – classification model
- ⚡ __K-Nearest Neighbors (KNN)__ – regression model
- ⚙️ __Preprocessing components__ `feature engineering` and `label encoding` for input data.

### 4. Scripts 
The Scripts module contains utility and data management scripts that help with collecting, cleaning, and preparing data:
- __Data Requesters (API)__: Collects data from external APIs (Ademe, Elevation, Geo, Enedis)
- __Processing__: Prepares, cleans, and structures data for analysis and model training.
- __Utils__: Contains helper functions for common tasks

### 5. Datasets 
Data sources used throughout the application, including climate zones, French communes, and the Ademe Lyon dataset. These datasets feed both the analysis dashboards and ML models.

### 6. Environment 
The application runs on __Python 3.13__ with __UV__ as the package manager. Docker manages all dependencies and configurations to ensure consistent deployments.


## Technologies used 
The application uses the following technologies:

| Technology | Description  |
|:--|:--|
| <img src="https://logos-world.net/wp-content/uploads/2021/10/Python-Logo-700x394.png" height="40"> | Core programming language for the application. |
| <img src="https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png" height="40"> | A Python framework for building interactive web applications. Streamlit simplifies the creation of user interfaces with visual and control components, making it ideal for data science applications. |
| <img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" height="40"> | A high-performance Python web framework for building APIs. It enables fast, reliable, and type-safe request handling, making it ideal for serving machine learning models and backend services. |
| <img src="https://www.sequoiacap.com/wp-content/uploads/sites/6/2023/08/name-and-logo-path.svg" height="20"> | A Python library for data validation and schema definition, ensuring that API inputs are correctly structured, type-safe, and ready for processing in the application. |
| <img src="https://upload.wikimedia.org/wikipedia/commons/e/ed/Pandas_logo.svg" height="40"> | A popular library for data manipulation, offering powerful tools for cleaning, transforming, and analyzing structured data in DataFrames. |
| <img src="https://upload.wikimedia.org/wikipedia/commons/0/05/Scikit_learn_logo_small.svg" height="40"> | A powerful machine learning library offering algorithms for classification, regression, and clustering. In this application, it is used to train models that predict building energy consumption and DPE class. |
| <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Plotly-logo.png/330px-Plotly-logo.png" height="40"> | A visualization library used to create interactive charts in the application, allowing users to explore and analyze DPE and energy consumption data with clear and dynamic visualizations. |
| <img src="https://static-assets.mapbox.com/logos/mapbox-logo-black.png" height="20"/> | A web mapping service and API for creating interactive, high-quality maps. Integrated into the application to visualize building locations and spatial distribution of energy performance. |
| <img src="https://upload.wikimedia.org/wikipedia/commons/1/1e/Docker_Logo.png" height="20"> | A platform for containerizing applications, ensuring consistent environments, simplified deployment, and easy scalability across different systems. |
