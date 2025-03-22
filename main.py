import time
import sqlite3
import pandas as pd
from fastapi import FastAPI
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

# Initialisation de l'API
app = FastAPI()

# Nom de la base de données
DB_NAME = "annonces.db"

# Fonction pour initialiser la base de données SQLite
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS annonces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            region TEXT,
            nature TEXT,
            type TEXT,
            texte TEXT,
            prix TEXT,
            modifie TEXT,
            superficie TEXT,
            description TEXT,
            numero_tel TEXT,
            localisation TEXT,
            details_link TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Route d'accueil
@app.get("/")
def home():
    return {"message": "API de scraping des annonces"}

# Route pour récupérer les annonces stockées
@app.get("/annonces")
def get_annonces():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM annonces", conn)
    conn.close()
    return df.to_dict(orient="records")

# Route pour lancer le scraping
@app.post("/scrape")
def scrape_annonces():
    # Configuration du WebDriver Selenium
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("user-agent=Mozilla/5.0")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    base_url = "http://www.tunisie-annonce.com/AnnoncesImmobilier.asp?rech_order_by=11&rech_page_num={}"
    annonces = []
    page=1
    #for page in range(1, 1003):  # Réduire le nombre de pages pour le test
    while True:

        url = base_url.format(page)
        print(f"Scraping page {page}...")

        driver.get(url)
        time.sleep(2)

        rows = driver.find_elements(By.XPATH, "(//tr[@bgcolor='#294a73']/following-sibling::tr)")
        if not rows:
            break
            
        for row in rows:
            try:
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) > 10 and cols[1].text.strip() != "":
                    modifie = cols[11].text.strip()
                    try:
                        date_modifie = datetime.strptime(modifie, "%d/%m/%Y")
                        date_min = datetime(2025, 1, 1)
                        date_max = datetime(2025, 2, 28)

                        if date_min <= date_modifie <= date_max:
                            region = cols[1].text.strip()
                            nature = cols[3].text.strip()
                            type_ = cols[5].text.strip()
                            texte = cols[7].text.strip()
                            prix = cols[9].text.strip()
                            details_link = cols[7].find_element(By.CSS_SELECTOR, "a").get_attribute("href")

                            # Ouvrir le lien pour récupérer plus d'infos
                            driver.execute_script(f"window.open('{details_link}', '_blank');")
                            driver.switch_to.window(driver.window_handles[-1])
                            driver.get(details_link)

                            try:
                                superficie = driver.find_element(By.XPATH, ".//tr[td[contains(text(),'Surface')]]/td[2]").text
                            except:
                                superficie = "non disponible"

                            try:
                                description = driver.find_element(By.XPATH, ".//tr[td[contains(text(),'Texte')]]/td[2]").text
                            except:
                                description = "non disponible"

                            try:
                                localisation = driver.find_element(By.XPATH, ".//tr[td[contains(text(),'Localisation')]]/td[2]").text
                            except:
                                localisation = "non disponible"

                            try:
                                numero_tel = driver.find_element(By.XPATH, "//li[@class='cellphone']/span").text
                            except:
                                numero_tel = "non disponible"

                            driver.close()
                            driver.switch_to.window(driver.window_handles[0])

                            # Ajouter aux résultats
                            annonces.append((region, nature, type_, texte, prix, modifie, superficie, description, numero_tel, localisation, details_link))

                    except Exception as e:
                        print(f"Erreur parsing date: {e}")

            except Exception as e:
                print(f"Erreur ligne: {e}")

        print(f"Page {page} récupérée avec succès!")
        page += 1

    driver.quit()

    # Enregistrer dans la base de données SQLite
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.executemany("""
        INSERT INTO annonces (region, nature, type, texte, prix, date de pub, superficie, description, numero_tel, localisation, details_link)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, annonces)
    conn.commit()
    conn.close()

    return {"message": f"{len(annonces)} annonces enregistrées avec succès!"}
