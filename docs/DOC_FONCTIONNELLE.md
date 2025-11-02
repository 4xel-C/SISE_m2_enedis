# Functional Documentation

## Introduction
The application was developed to analyze and predict the __*Diagnostic de Performance Énergétique* (DPE)__ and the __Energy Consumption__ of residential and commercial buildings in France. It uses __Machine Learning models__ to estimat DPE class and energy consumption based on various property characteristics. 

The application is organized into __three main sections__, each containing dedicated pages that help __explore, visualize, and understand__ energy performance across different buildings and their attributes. 

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

<br/>

## 1. Project Section 
### 🏠Home Page 
The home page introduces the application and its main objectives. It outlines the key features—data exploration, visualization, and DPE/energy consumption prediction- and guides users to the different sections.
### 📋Context Page
The Context Page gives an overview of all available data sources and their structure, helping users understand the information behind the analyses and predictions. It features:

* __Data sources__ - overview of all the datasets used in the project, including ADEME DPE, Enedis electricity consumption, and geographic, climatic, and altitude data
* __Prediction variables__ - detailed information on the quantitative and qualitative features used by the ML models.
* __Data processing workflow__ - how data is collected, enriched, cleaned, and prepared
* __Data quality indicators__ - highlights dataset strengths, limitations, and considerations for interpreting results
  
<br/>

## 2. Data Section
### 📊Statistics & Visualization Page
The Statistics & Visualization page lets users explore and analyze the DPE dataset through interactive filters and visualizations. It contains __two subpages__:
* __🧮Datasets Print__: Browse the dataset, view the first rows, and check the total number of records. Users can sort data in ascending or descending order and export samples as CSV files.
* __📊Dataset Statistics__: Provides detailed insights into energy performance metrics and patterns. Features include:
    * __Dynamic filters__: Filter the dataset by commune, building type, and DPE class to examine specific subsets
    * __Key metrics__: View averages, most frequent DPE labels, and summary statistics at a glance.
    * __Statistics__: Access detailed statistics for energy consumption, costs, and GES emissions, including mean, standard deviation, min, and max values.
    * __Distributions and comparisons__: Visualize DPE and GES class distributions, energy consumption, and costs by category.
    * __Consumption by usage type__: Break down total energy consumption, costs, and GES emissions by each energy usage category (heating, cooling, ECS, lighting, and auxiliaries).
    * __Variable impact analysis__: Explore correlations and relationships between energy consumption and other numeric variables.

<p align="center">
  <img src="https://github.com/user-attachments/assets/5d1289d5-f910-4b1e-8633-172b09724a04" alt="statistics" width="900">
</p>

### 🗺️DPE Map Page  
The Map Page visualizes the geographic distribution of DPE classes across buildings. Users can interactively filter and analyze homes by DPE class and location:
* __Interactive map__ - displays homes color-coded by DPE class for easy interpretation
* __Dynamic filtering__ - select specific DPE classes and adjust the number of homes displayed
* __Tooltips__ - hover over points to view DPE label, energy cost, and coordinates

<p align="center"> 
   <img width="900" height="850" alt="Map" src="https://github.com/user-attachments/assets/bcf1b0b2-99ce-4722-adf4-bab4320baca4" />
</p>

### 📂Datasets and Download 
The Datasets & Download page manages local datasets and allows the retrieval of new data directly from the ADEME API. Users can upload, refresh, clean, and download datasets. The page has two main sections:
* __🧮 Your Datasets__: Browse, load, and preview locally stored datasets. Existing datasets can be refreshed with new data from the ADEME API, downloaded, or deleted.
* __🛜 Fetch new data__: Import new data by department and building type (existing or new) directly from the ADEME API. The acquired data is automatically cleaned, formatted, and ready to be added to the existing datasets.

<br/>

## 3. Prediction Section 
### 🔮Predict DPE Class
This page allows users to predict the energy consumption and the DPE class of a building based on its characteristics. It includes: 
* __Input Form__: Enter building details like living area, type, energy source, and city. If energy consumption is unknown, the model predicts both consumption and DPE class. If provided, only the DPE class is predicted.
* __Model selection__: Choose between the original and retrained versions of the regression and classification models directly from the sidebar.
* __Automatic enrichment__: The app automatically retrieves the climate zone, latitude, longitude, and altitude based on the entered city.
* __Prediction results__: Display the predicted DPE class and, when applicable, the estimated annual energy cost.

<table>
<tr>
  <td><img src="https://github.com/user-attachments/assets/19af13ea-ccb5-4543-99c2-4912a87f2f43" alt="Predic1"></td>
  <td><img src="https://github.com/user-attachments/assets/5d549aac-b245-4d5a-832c-c746fadbc9d6" alt="Predic2"></td>
</tr>
</table>

### 🔄Model Retraining 
This page allows users to retrain the regression and classification models using a new dataset, ensuring that the models remain up to date and adapted to recent data.
* __Data selection & retraining__ - Select a dataset from the sidebar and launch the retraining of both regression and classification pipelines directly within the app.
* __Performance comparison__ - compare metrics (R², RMSE, accuracy) between original and retrained models, with indicators showing improvements or declines.
* __Automatic saving__ - newly retrained models are automatically saved to the model directory for future use.
