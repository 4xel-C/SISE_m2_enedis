# Documentation fonctionnelle

## Introduction
The application was developed to analyze and predict the __*Diagnostic de Performance Énergétique* (DPE)__ and the __Energy Consumption__ of residential and commercial buildings in France. It incorporates __Machine Learning models__ to estimate both the DPE class and energy consumption based on various property characteristics. The application is organized into __three main sections__, each containing dedicated pages that help __explore, visualize, and understand__ energy performance across different buildings and their attributes:

* [Project Section](#project-section): Introduces the application’s objectives, data context, and overall structure.
    * [🏠Home Page](#home-page)
    * [📋Context Page](#context-page)
* [Data Section](#data-section): Focuses on data exploration, visualization, and management of datasets.
    * [📊Statistics & Visualization Page](#statistics--visualization-page)
    * [🗺️DPE Map Page](#️dpe-map-page)
    * [📂Datasets and Downloads Page](#datasets-and-download)
* [Prediction Section](#prediction-section): Covers DPE and energy consumption predictions, model retraining, and performance evaluation.
    * [🔮Predict DPE Class Page](#predict-dpe-class)
    * [🔄Model Retraining Page](#model-retraining)

## Project Section 
### 🏠Home Page 
The home page provides an overview of the application and its main objectives. It introduces the available features, such as data exploration, visualization, and DPE and energy consumption prediction, and guides users towards the different pages of the application.
### 📋Context Page
The Context Page gives an overview of all available data sources and their structure, helping users understand the information behind the analyses and predictions. It features:

* __Main data sources__: Overview of all the datasets used in the project, including ADEME DPE, Enedis electricity consumption, and geographic, climatic, and altitude data
* __Prediction variables__: Detailed information on the quantitative and qualitative features used by the prediction models.
* __Data processing workflow__: Explanation of how data is collected, enriched, cleaned, and prepared for analysis and prediction.
* __Data quality and reliability indicators__: Highlights the strengths of the datasets, potential limitations, and considerations for interpreting the results accurately.

## Data Section
### 📊Statistics & Visualization Page
The Statistics & Visualization page provides an interactive overview of the DPE dataset, allowing users to explore, filter, and analyze key metrics and distributions, and patterns of energy consumption, cost, and performance. It contains __two subpages__:
* __🧮Datasets Print__: Browse the dataset, view the first rows, and check the total number of records. The data can also be sorted in ascending or descending order, and a sample can be saved as a CSV file.
* __📊Dataset Statistics__: Provides detailed insights into the dataset, including distributions, key metrics, and relationships between variables. Features include:
    * __Dynamic filters__: Filter the dataset by commune, building type, and DPE class to examine specific subsets
    * __Key metrics__: View averages, most frequent DPE labels, and summary statistics at a glance.
    * __Statistics__: Access detailed statistics for energy consumption, costs, and GES emissions, including mean, standard deviation, min, and max values.
    * __Distributions and comparisons__: Visualize DPE and GES class distributions, energy consumption, and costs by category.
    * __Consumption by usage type__: Break down total energy consumption, costs, and GES emissions by each energy usage category (heating, cooling, ECS, lighting, and auxiliaries).
    * __Variable impact analysis__: Explore correlations and relationships between energy consumption and other numeric variables.

### 🗺️DPE Map Page  
The Map Page provides a geographical visualization of the DPE dataset, allowing exploration of the spatial distribution of energy performance across buildings. Users can interactively filter and analyze homes by DPE class and location. Key functionalities include:
* __Interactive map__: Explore the spatial distribution of homes, with DPE classes visually distinguished by color for quick interpretation.
* __Dynamic filtering__: Select DPE classes and adjust the number of homes displayed to focus on specific areas or subsets of data.
* __Tooltips__: Hover over each point to see detailed information, including DPE label, total energy cost, and geographical coordinates.

### 📂Datasets and Download 
The Datasets & Download page allows managing local datasets and retrieving new data directly from the ADEME API. It offers tools to upload, refresh, clean, and download datasets used throughout the application. The page is divided into two main sections:
* __🧮 Your Datasets__: Browse, load, and preview locally stored datasets. Existing datasets can be refreshed with new data from the ADEME API, downloaded, or deleted.
* __🛜 Fetch new data__: Import new data by department and building type (existing or new) directly from the ADEME API. The acquired data is automatically cleaned, formatted, and ready to be added to the existing datasets.

## Prediction Section 
### 🔮Predict DPE Class
This page allows users to predict both the energy consumption and the DPE class of a building based on its characteristics. It includes: 
* __Input Form__: Enter building information such as living area, type, energy source, and city. If the energy consumption value is unknown, the model predicts both energy use and DPE class. If provided, only the DPE class is predicted.
* __Model selection__: Choose between the original and retrained versions of the regression and classification models directly from the sidebar.
* __Automatic enrichment__: The app automatically retrieves the climate zone, latitude, longitude, and altitude based on the entered city.
* __Prediction results__: Display the predicted DPE class and, when applicable, the estimated annual energy cost. 

### 🔄Model Retraining 
This page allows users to retrain the regression and classification models using a new dataset, ensuring that the models remain up to date and adapted to recent data.
* __Data selection & retraining__: Select a dataset from the sidebar and launch the retraining of both regression and classification pipelines directly within the app.
* __Performance comparison__: View side-by-side metrics (R², RMSE, and Accuracy) comparing the original and retrained models, with clear indicators showing performance improvements or drops.
* __Automatic saving__: The newly retrained models are automatically stored in the application’s model directory for future predictions. 