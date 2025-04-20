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

##  Partie 2 : Dashboard Interactif

- Statistiques sur les annonces à l’aide de **Pandas**
- Visualisation via **Plotly** (graphique circulaire, barres, histogrammes…)
- Tableau interactif avec recherche
- Filtres dynamiques (type de bien, région)
  
****Auteur**:
  Arwa Kthiri &
  Aziz Seblaoui**

