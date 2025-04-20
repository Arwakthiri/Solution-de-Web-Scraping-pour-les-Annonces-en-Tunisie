# Solution-de-Web-Scraping-pour-les-Annonces-en-Tunisie

** Description**

Ce projet est une application complète de scraping qui extrait des annonces depuis le web, les enregistre dans une base de données SQLite, et expose une API via FastAPI pour interagir facilement avec les données (récupération, ajout, etc.).

L'objectif est d'automatiser le scraping, de stocker les résultats de manière structurée, et de fournir une API REST pour accéder aux données.

** Prérequis**

Python 3.10+

FastAPI (pour l'API)
Uvicorn (pour lancer le serveur)
SQLite3 (base de données intégrée)
Requests / selenium (pour le scraping)

** Installation**
Créer un environnement virtuel 
 python -m venv venv
 source venv/bin/activate
 
 Installation des dépendances
 pip install fastapi uvicorn selenium webdriver-manager pandas sqlite3
 creation du fichier main.py et requirements.txt
 pip freeze > requirements.txt  pour  sauvegarder les dépendances :

  **Lancer le projet**

Lancer le serveur API :  uvicorn main:app --reload
Accéder à l'API dans le navigateur :
      Accueil : http://127.0.0.1:8000/
      Docs interactives (Swagger) : http://127.0.0.1:8000/docs
ou bien avec postman

**BDD(sql lite)**
pour mieux visualisation installer DB Browser for SQLite


 ** Endpoints API disponibles**

GET / : Page d'accueil simple

POST /scrape : Lance le scraping et stocke les annonces dans la base de données _annonces.db_.

GET /annonces : Récupère toutes les annonces stockées.

## Partie 2 : Dashboard Interactif

Le tableau de bord interactif est construit en utilisant **Dash**, **Plotly**, et **Pandas** pour afficher des statistiques et des visualisations sur les annonces immobilières.

### Fonctionnalités du Dashboard :
- **Statistiques sur les annonces** : Traitement des données avec **Pandas** pour extraire des informations pertinentes.
- **Visualisation via Plotly** : Création de différents graphiques (graphique circulaire, barres, histogrammes, etc.).
- **Tableau interactif** avec recherche : Permet de rechercher et filtrer les annonces directement dans le tableau.
- **Filtres dynamiques** : Les utilisateurs peuvent filtrer les annonces par type de bien (Appartement, Maison, Terrain, etc.) et par région.

### Lancer le Dashboard

1. **Installer les dépendances nécessaires** :
   Dans votre terminal, assurez-vous d'abord d'avoir installé **Dash** et **Plotly** :

   pip install dash plotly pandas
**2. Lancer l'application Dashboard**
   python app.py

3. **Structure des fichiers**
app.py : Contient le tableau de bord interactif construit avec Dash. C'est là que l'interface utilisateur (UI) et les graphiques sont définis.

utils.py : Contient des fonctions utiles pour le traitement des données et le calcul des statistiques (moyenne des prix, superficie moyenne, etc.).


****Auteur**:
  Arwa Kthiri &
  Aziz Seblaoui**

