"""
# Context Page - Présentation et Visualisation des Données
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys

# Ajouter le chemin parent pour importer les modules
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.data_requesters.enedis import Enedis_API_requester
from src.data_requesters.ademe import Ademe_API_requester

# ⚙️ Configuration générale
st.set_page_config(
    page_title="DPE - Contexte des Données", page_icon="📋", layout="wide"
)

# 📋 Titre
st.title("📋 Contexte - Présentation des Données Disponibles")

st.markdown("""
Cette page présente l'ensemble des **données disponibles** dans le projet, leur structure, 
leurs sources et des visualisations pour mieux comprendre le contexte d'utilisation.
""")

st.divider()

# === Vue d'ensemble des sources de données ===
st.header("📊 Sources de Données")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="🏛️ ADEME - DPE",
        value="Source principale",
        help="Base de données des diagnostics de performance énergétique"
    )
    st.caption("Données énergétiques des logements français")

with col2:
    st.metric(
        label="⚡ Enedis",
        value="Données complémentaires",
        help="Consommations électriques par territoire"
    )
    st.caption("Consommations d'électricité réelles")

with col3:
    st.metric(
        label="🗺️ Géographiques",
        value="Enrichissement",
        help="Communes, zones climatiques, altitudes"
    )
    st.caption("Contexte géographique et climatique")

with col4:
    st.metric(
        label="⛰️ Altitude",
        value="API Elevation",
        help="Données d'altitude précises par coordonnées GPS"
    )
    st.caption("Enrichissement altimétrique")

st.divider()

# === Données ADEME - DPE ===
st.header("🏛️ Données ADEME - Diagnostic de Performance Énergétique")

st.markdown("""
Les données **ADEME** constituent la source principale du projet. Le DPE évalue la performance 
énergétique des logements et les classe de **A (très performant)** à **G (peu performant)**.
""")

# Récupération dynamique des variables depuis l'API ADEME
with st.expander("📋 Voir les variables DPE disponibles (récupérées en temps réel depuis l'API)"):
    
    # Choix entre existant et neuf
    col1, col2 = st.columns(2)
    with col1:
        dataset_type = st.radio(
            "Type de logement",
            ["Logements existants", "Logements neufs"],
            index=0,
            horizontal=True
        )
    
    neuf = dataset_type == "Logements neufs"
    
    try:
        with st.spinner(f"Récupération des métadonnées de l'API ADEME ({dataset_type})..."):
            requester = Ademe_API_requester()
            fields_by_group = requester.get_fields_by_group(neuf=neuf)
        
        if fields_by_group:
            total_fields = sum(len(fields) for fields in fields_by_group.values())
            st.success(f"✅ {total_fields} variables récupérées avec succès depuis l'API ADEME")
            
            # Afficher les statistiques
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📊 Nombre total de champs", total_fields)
            with col2:
                st.metric("📁 Groupes de variables", len(fields_by_group))
            with col3:
                # Compter les types uniques
                all_fields = []
                for fields in fields_by_group.values():
                    all_fields.extend(fields)
                types_count = len(set(f['type'] for f in all_fields))
                st.metric("🔢 Types de données", types_count)
            
            # Afficher par groupe
            st.markdown("#### 📋 Variables par groupe")
            
            for group_name in sorted(fields_by_group.keys()):
                group_fields = fields_by_group[group_name]
                
                with st.container():
                    st.markdown(f"**📁 {group_name}** ({len(group_fields)} champs)")
                    
                    # Créer un DataFrame pour affichage
                    df_group = pd.DataFrame(group_fields)
                    display_df = df_group[['key', 'label', 'type', 'description']].copy()
                    display_df.columns = ['Nom du champ', 'Label', 'Type', 'Description']
                    
                    st.dataframe(
                        display_df,
                        use_container_width=True,
                        hide_index=True,
                        height=min(len(group_fields) * 35 + 38, 400)
                    )
            
            # Option pour télécharger les métadonnées
            st.divider()
            st.markdown("#### 💾 Export des métadonnées")
            
            # Créer un DataFrame avec tous les champs
            all_fields_list = []
            for group, fields in fields_by_group.items():
                for field in fields:
                    all_fields_list.append(field)
            
            df_all_fields = pd.DataFrame(all_fields_list)
            csv = df_all_fields.to_csv(index=False)
            
            filename = f"ademe_api_fields_{'neuf' if neuf else 'existant'}.csv"
            st.download_button(
                label="📥 Télécharger la liste complète des variables (CSV)",
                data=csv,
                file_name=filename,
                mime="text/csv",
            )
            
    except Exception as e:
        st.error(f"❌ Erreur lors de la récupération des variables : {e}")
        
        # Afficher un fallback avec les informations de base
        st.markdown("**Variables principales (informations de base)** :")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Identifiants et localisation**
            - `N°DPE` : Identifiant unique du diagnostic
            - `Code_postal_(BAN)` : Code postal
            - `Commune_(BAN)` : Nom de la commune
            - `Département` : Code département
            - `Longitude` / `Latitude` : Coordonnées GPS
            - `Altitude` : Altitude du logement
            
            **Caractéristiques du bâtiment**
            - `Type_bâtiment` : Maison, appartement, etc.
            - `Année_construction` : Année de construction
            - `Surface_habitable_logement` : Surface en m²
            - `Type_installation_chauffage` : Type de chauffage
            - `Type_énergie_principale_chauffage` : Gaz, électricité, etc.
            - `Isolation_toiture`, `Isolation_murs`, `Isolation_plancher_bas`
            """)
        
        with col2:
            st.markdown("""
            **Performance énergétique**
            - `Classe_consommation_énergie` : A, B, C, D, E, F, G
            - `Conso_5_usages_é_finale` : Consommation finale (kWh/m²/an)
            - `Conso_5_usages_é_primaire` : Consommation primaire
            - `Classe_estimation_ges` : Classe émissions GES
            - `Estimation_ges` : Émissions CO2 (kg/m²/an)
            
            **Équipements**
            - `Type_installation_ECS` : Eau chaude sanitaire
            - `Type_énergie_n°1_ECS` : Énergie pour ECS
            - `Qualité_isolation_enveloppe` : Qualité globale
            - `Qualité_isolation_menuiseries` : Qualité des fenêtres
            - `Type_ventilation` : Système de ventilation
            """)

st.info("💡 **Source** : [data.ademe.fr](https://data.ademe.fr) - Base nationale des DPE")

st.divider()

# === Données Enedis ===
st.header("⚡ Données Enedis - Consommations Électriques")

st.markdown("""
Les données **Enedis** fournissent les consommations électriques réelles par territoire, 
permettant d'enrichir l'analyse avec des données de consommation effectives.
""")

# Récupération dynamique des variables depuis l'API
with st.expander("📋 Voir les variables Enedis disponibles (récupérées en temps réel depuis l'API)"):
    try:
        with st.spinner("Récupération des métadonnées de l'API Enedis..."):
            requester = Enedis_API_requester()
            fields = requester.get_dataset_fields()
        
        if fields:
            st.success(f"✅ {len(fields)} variables récupérées avec succès depuis l'API Enedis")
            
            # Créer un DataFrame pour affichage
            df_fields = pd.DataFrame(fields)
            
            # Afficher les statistiques
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📊 Nombre total de champs", len(fields))
            with col2:
                types_count = df_fields['type'].nunique()
                st.metric("🔢 Types de données", types_count)
            with col3:
                with_desc = df_fields['description'].apply(lambda x: bool(x)).sum()
                st.metric("📝 Champs documentés", with_desc)
            
            # Grouper par type de données
            st.markdown("#### 📋 Variables par type")
            
            # Créer des onglets par catégorie
            types = df_fields['type'].unique()
            
            for data_type in sorted(types):
                fields_of_type = df_fields[df_fields['type'] == data_type]
                
                with st.container():
                    st.markdown(f"**Type: `{data_type}`** ({len(fields_of_type)} champs)")
                    
                    # Afficher sous forme de tableau compact
                    display_df = fields_of_type[['name', 'label', 'description']].copy()
                    display_df.columns = ['Nom du champ', 'Label', 'Description']
                    
                    st.dataframe(
                        display_df,
                        use_container_width=True,
                        hide_index=True,
                        height=min(len(fields_of_type) * 35 + 38, 300)
                    )
            
            # Option pour télécharger les métadonnées
            st.divider()
            st.markdown("#### 💾 Export des métadonnées")
            
            csv = df_fields.to_csv(index=False)
            st.download_button(
                label="📥 Télécharger la liste complète des variables (CSV)",
                data=csv,
                file_name="enedis_api_fields.csv",
                mime="text/csv",
            )
            
    except Exception as e:
        st.error(f"❌ Erreur lors de la récupération des variables : {e}")
        
        # Afficher un fallback avec les informations de base
        st.markdown("**Variables principales (informations de base)** :")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Localisation**
            - Code commune INSEE
            - Nom de la commune
            - Code département
            - Région
            
            **Consommations**
            - Consommation annuelle (MWh)
            - Nombre de sites
            - Consommation moyenne par site
            """)
        
        with col2:
            st.markdown("""
            **Typologie**
            - Secteur résidentiel
            - Profil de consommation
            - Puissance souscrite
            
            **Temporalité**
            - Année de référence
            - Évolution temporelle
            """)

st.info("💡 **Source** : [data.enedis.fr](https://data.enedis.fr) - Open Data Enedis")

st.divider()

# === Données d'Altitude (Elevation API) ===
st.header("⛰️ Données d'Altitude - Elevation API")

st.markdown("""
L'**API Elevation** permet d'enrichir les données avec l'altitude précise des logements 
à partir de leurs coordonnées GPS (latitude/longitude).
""")

with st.expander("📋 Voir les informations sur l'API Elevation"):
    st.markdown("""
    ### 🎯 Fonctionnement
    
    L'API Elevation est utilisée pour obtenir l'**altitude en mètres** d'un point géographique.
    
    **Paramètres d'entrée** :
    - `lat` : Latitude (format décimal)
    - `lon` : Longitude (format décimal)
    
    **Exemple de requête** :
    ```
    https://api.elevationapi.com/api/Elevation?lat=48.8566&lon=2.3522
    ```
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📊 Données retournées
        
        **Point géographique** :
        - `elevation` : Altitude en mètres
        - `latitude` : Latitude du point
        - `longitude` : Longitude du point
        - `distanceFromOriginMeters` : Distance depuis l'origine
        
        **Métriques** :
        - `minElevation` : Altitude minimale
        - `maxElevation` : Altitude maximale
        - `distance` : Distance totale
        - `numPoints` : Nombre de points
        """)
    
    with col2:
        st.markdown("""
        ### 📁 Dataset source
        
        **Caractéristiques** :
        - `name` : Nom du dataset
        - `description` : Description
        - `resolutionMeters` : Résolution en mètres
        - `resolutionArcSeconds` : Résolution en secondes d'arc
        - `fileFormat` : Format des fichiers sources
        - `attribution` : Attribution des données
        
        **Qualité** :
        - Couverture mondiale
        - Précision variable selon la zone
        - Sources multiples (SRTM, ASTER, etc.)
        """)
    
    st.info("""
    💡 **Utilisation dans le projet** : L'altitude est un facteur important pour le calcul 
    du DPE car elle influence les besoins en chauffage (températures plus basses en altitude).
    """)

st.info("💡 **Source** : [elevationapi.com](https://elevationapi.com) - API d'altitude mondiale")

st.divider()

# === Données Géographiques ===
st.header("🗺️ Données Géographiques et Climatiques")

st.markdown("""
Les données géographiques permettent d'enrichir les analyses avec le **contexte territorial** 
et **climatique** des logements.
""")

tab1, tab2 = st.tabs(["🌍 Communes de France", "🌡️ Zones Climatiques"])

with tab1:
    st.markdown("### Référentiel des Communes Françaises (2025)")
    
    st.info("💡 **Source** : [data.gouv.fr - Communes et villes de France](https://www.data.gouv.fr/datasets/communes-et-villes-de-france-en-csv-excel-json-parquet-et-feather/) - Données ouvertes gouvernementales")
    
    # Chargement et affichage des données des communes
    data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "communes-france-2025.csv")
    
    if os.path.exists(data_path):
        try:
            df_communes = pd.read_csv(data_path, nrows=5)
            
            st.markdown(f"""
            📊 **Aperçu du fichier** : `communes-france-2025.csv`
            
            Ce fichier provient du **portail Open Data du gouvernement français** et contient 
            des informations exhaustives sur toutes les communes de France métropolitaine et d'outre-mer.
            
            **Caractéristiques** :
            - **Nombre total de communes** : ~35 000 communes
            - **Formats disponibles** : CSV, Excel, JSON, Parquet, Feather
            - **Mise à jour** : Régulière (données 2025)
            - **Licence** : Licence Ouverte / Open Licence
            """)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📍 Variables géographiques", "~40")
            with col2:
                st.metric("🏘️ Données démographiques", "Oui")
            with col3:
                st.metric("🔗 Codes d'identification", "Multiples")
            
            with st.expander("Voir les principales variables disponibles"):
                st.markdown("""
                **Identifiants et noms**
                - `code_insee` : Code commune assigné par l'INSEE
                - `nom_standard` : Nom normalisé avec article (ex: Le Havre)
                - `nom_sans_pronom` : Nom sans article (ex: Havre)
                - `nom_a` : Avec préposition à/au/aux (ex: au Havre)
                - `nom_de` : Avec préposition d'/de/du/des (ex: du Havre)
                - `nom_sans_accent` : Sans accents ni caractères spéciaux
                - `nom_standard_majuscule` : En majuscules (ex: LE HAVRE)
                
                **Type de commune**
                - `typecom` : Type abrégé (COM, COMA, COMD, ARM)
                - `typecom_texte` : Type en version textuelle
                
                **Localisation administrative**
                - `reg_code` / `reg_nom` : Code et nom de la région
                - `dep_code` / `dep_nom` : Code et nom du département
                - `canton_code` / `canton_nom` : Code et nom du canton
                - `epci_code` / `epci_nom` : Code et nom de l'EPCI (établissement public de coopération intercommunale)
                - `academie_code` / `academie_nom` : Code et nom de l'académie de rattachement
                
                **Codes postaux**
                - `code_postal` : Code postal principal
                - `codes_postaux` : Liste de tous les codes postaux rattachés
                
                **Géographie**
                - `latitude_mairie` / `longitude_mairie` : Coordonnées de la mairie
                - `latitude_centre` / `longitude_centre` : Coordonnées du centroïde du territoire
                - `altitude_moyenne` / `altitude_minimale` / `altitude_maximale` : Altitudes en mètres
                - `superficie_hectare` / `superficie_km2` : Superficie en ha et km²
                
                **Démographie**
                - `population` : Population municipale
                - `densite` : Densité en habitants/km²
                
                **Urbanisation**
                - `grille_densite` : Grille communale de densité à 7 niveaux (INSEE)
                - `grille_densite_texte` : Version textuelle de la grille de densité
                - `code_unite_urbaine` : Code INSEE de l'unité urbaine (agglomération)
                - `nom_unite_urbaine` : Nom de l'agglomération
                - `taille_unite_urbaine` : Taille de l'unité urbaine
                - `type_commune_unite_urbaine` : Type (Hors unité urbaine ou Unité urbaine)
                - `statut_commune_unite_urbaine` : Statut (H: Hors unité urbaine, C: Ville-centre, B: Banlieue, I: Ville isolée)
                
                **Économie et services**
                - `zone_emploi` : Code de la zone d'emploi (INSEE)
                - `code_insee_centre_zone_emploi` : Code INSEE de la commune centre de la zone d'emploi
                - `niveau_equipements_services` : Niveau d'équipements (0 à 4)
                - `niveau_equipements_services_texte` : Version textuelle du niveau d'équipements
                
                **Informations complémentaires**
                - `gentile` : Nom des habitants
                - `url_wikipedia` : Lien vers la page Wikipédia
                - `url_villedereve` : Lien vers la page Ville de rêve
                """)
            
            st.dataframe(df_communes.head(), use_container_width=True)
            
        except Exception as e:
            st.warning(f"Impossible de charger l'aperçu : {e}")
    else:
        st.warning("⚠️ Fichier `communes-france-2025.csv` non trouvé dans le dossier `data/`")

with tab2:
    st.markdown("### Zones Climatiques par Département")
    
    # Chargement et visualisation des zones climatiques
    climate_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "climate_zones.csv")
    
    if os.path.exists(climate_path):
        try:
            df_climate = pd.read_csv(climate_path)
            
            st.markdown("""
            La France est divisée en **3 zones climatiques** réglementaires pour le calcul 
            des performances énergétiques des bâtiments :
            """)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                h1_count = len(df_climate[df_climate['Zone climatique'] == 'H1'])
                st.metric("🥶 Zone H1 (Froide)", f"{h1_count} dép.", 
                         help="Nord et Est de la France - Climat le plus rigoureux")
            
            with col2:
                h2_count = len(df_climate[df_climate['Zone climatique'] == 'H2'])
                st.metric("🌤️ Zone H2 (Tempérée)", f"{h2_count} dép.",
                         help="Centre et Ouest de la France - Climat intermédiaire")
            
            with col3:
                h3_count = len(df_climate[df_climate['Zone climatique'] == 'H3'])
                st.metric("☀️ Zone H3 (Chaude)", f"{h3_count} dép.",
                         help="Sud de la France et littoral méditerranéen - Climat doux")
            
            # Graphique de répartition
            fig = px.pie(
                df_climate.groupby('Zone climatique').size().reset_index(name='count'),
                values='count',
                names='Zone climatique',
                title='Répartition des départements par zone climatique',
                color='Zone climatique',
                color_discrete_map={'H1': '#4A90E2', 'H2': '#F5A623', 'H3': '#E94B3C'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            with st.expander("📋 Voir la liste complète des départements"):
                st.dataframe(df_climate, use_container_width=True, height=400)
            
        except Exception as e:
            st.warning(f"Impossible de charger les données climatiques : {e}")
    else:
        st.warning("⚠️ Fichier `climate_zones.csv` non trouvé dans le dossier `data/`")

st.divider()

# === Structure des données d'entrée pour la prédiction ===
st.header("🔮 Variables utilisées pour la Prédiction")

st.markdown("""
Le modèle de prédiction du DPE utilise un ensemble de **variables précises** pour estimer 
la classe énergétique d'un logement (A → G). Voici les données d'entrée du modèle :
""")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 📝 Variables du modèle
    
    **Caractéristiques quantitatives** :
    - `surface_habitable_logement` : Surface habitable en m²
    - `nombre_niveau_logement` : Nombre de niveaux/étages
    - `age_batiment` : Âge du bâtiment en années
    - `altitude_moyenne` : Altitude moyenne en mètres
    - `cout_total_5_usages` : Coût total annuel (€/an) - optionnel
    
    **Caractéristiques qualitatives** :
    - `type_energie_principale_chauffage` : Type d'énergie de chauffage
      - Gaz naturel
      - Électricité  
      - Autre
    - `type_batiment` : Type de construction
      - Appartement
      - Maison
      - Immeuble
    - `zone_climatique` : Zone climatique réglementaire (H1, H2, H3)
    """)

with col2:
    st.markdown("""
    ### 🔄 Processus de prédiction
    
    **Étape 1 : Saisie utilisateur**
    - Nom de la ville → récupération automatique des coordonnées GPS
    
    **Étape 2 : Enrichissement automatique**
    - Latitude/Longitude → via base de données des communes
    - Zone climatique → déterminée par le département
    - Altitude → récupérée via l'API Elevation
    
    **Étape 3 : Prédiction du coût (si non fourni)**
    - Modèle de régression pour estimer `cout_total_5_usages`
    - Basé sur les autres caractéristiques du logement
    
    **Étape 4 : Prédiction de la classe DPE**
    - Modèle de classification XGBoost
    - Sortie : Classe énergétique de A (meilleur) à G (moins bon)
    """)

st.info("""
💡 **Utilisation pratique** : Sur la page **Prédiction**, l'utilisateur n'a qu'à saisir :
- Le nom de la ville (enrichissement automatique)
- Surface habitable, nombre de niveaux, âge du bâtiment
- Type d'énergie et type de bâtiment
- Optionnellement : le coût total annuel

Le modèle s'occupe automatiquement de récupérer la zone climatique et l'altitude !
""")

st.divider()

# === Workflow des données ===
st.header("🔄 Flux de Traitement des Données")

st.markdown("""
Voici le **workflow complet** de traitement des données dans l'application :
""")

# Diagramme de flux avec des colonnes
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    ### 1️⃣ Collecte
    📥 **Sources**
    - API ADEME
    - Open Data Enedis
    - Fichiers CSV
    """)

with col2:
    st.markdown("""
    ### 2️⃣ Enrichissement
    🔧 **Ajout**
    - Zones climatiques
    - Données géographiques
    - Altitudes
    - Densités
    """)

with col3:
    st.markdown("""
    ### 3️⃣ Traitement
    ⚙️ **Nettoyage**
    - Valeurs manquantes
    - Doublons
    - Normalisation
    - Feature engineering
    """)

with col4:
    st.markdown("""
    ### 4️⃣ Utilisation
    🎯 **Applications**
    - Visualisations
    - Statistiques
    - Prédictions ML
    - Export
    """)

st.divider()

# === Qualité des données ===
st.header("✅ Qualité et Fiabilité des Données")

st.markdown("""
La **qualité des données** est essentielle pour obtenir des analyses et prédictions fiables.
""")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### Points forts ✅
    - Données officielles certifiées
    - Mise à jour régulière
    - Couverture nationale complète
    - Variables standardisées
    - Géolocalisation précise
    """)

with col2:
    st.markdown("""
    ### Points d'attention ⚠️
    - Valeurs manquantes possibles
    - Hétérogénéité des données anciennes
    - Évolution des normes DPE
    - Qualité variable selon départements
    - Données Enedis agrégées par commune
    """)

st.divider()

# === Footer ===
st.caption("💡 Utilisez la barre latérale pour naviguer vers les autres pages et exploiter ces données.")
st.caption("📊 Page **Data** : Visualisez les données sur carte interactive")
st.caption("🔮 Page **Prédiction** : Utilisez le modèle ML pour prédire la classe DPE")
st.caption("🌐 Page **API** : Requêtez l'API ADEME en temps réel")
st.caption("📈 Page **Stats** : Analysez les statistiques détaillées du dataset")
