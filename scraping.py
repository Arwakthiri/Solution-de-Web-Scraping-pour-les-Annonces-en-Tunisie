import csv
import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.expected_conditions import text_to_be_present_in_element
from selenium.common.exceptions import NoSuchElementException, TimeoutException


# . Options pour éviter la détection Selenium
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-usb"])
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
options.add_argument("--headless")  # Mode sans affichage (optionnel)
options.add_argument("--disable-gpu")  # Utile pour éviter certains bugs graphiques
options.add_argument("--no-sandbox")  # Utile sur certains systèmes
options.add_argument("--no-sandbox")  # Mode sans sandbox (utile pour certains environnements)
options.add_argument("--disable-software-rasterizer")  # Évite le fallback WebGL
options.add_argument("--enable-unsafe-swiftshader")  # Active SwiftShader si nécessaire

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.maximize_window()

# URL de base pour la pagination
base_url = "http://www.tunisie-annonce.com/AnnoncesImmobilier.asp?rech_page_num={}"

# Liste pour stocker les données
annonces = []

# Boucle sur chaque page (1 à 1002)
for page in range(1, 1003):  
    url = base_url.format(page)
    print(f"Scraping page {page}...")

    # Charger la page
    driver.get(url)
    time.sleep(2)  # Pause pour laisser la page se charger

    # Récupérer les annonces (tableau principal)
    rows = driver.find_elements(By.XPATH, "(//tr[@bgcolor='#294a73']/following-sibling::tr)")
    for row in rows:

        try:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) > 10 and cols[1].text.strip()!="":
            # Extraire les données
                region = cols[1].text.strip()
                print(region)
                nature = cols[3].text.strip()
                type_ = cols[5].text.strip()
                texte = cols[7].text.strip()
                prix = cols[9].text.strip()
                modifie = cols[11].text.strip()

                try:
                    link_element = cols[7].find_element(By.CSS_SELECTOR, "a")
                    details_link = link_element.get_attribute("href")
                    print(details_link)
                    driver.execute_script(f"window.open('{details_link}', '_blank');")

    # **Changer vers le nouvel onglet (dernier ouvert)**
                    driver.switch_to.window(driver.window_handles[-1])
                    driver.get(details_link)
            
                    # Extraire la ligne qui contient "Surface"
                    try:
                        surface = driver.find_element(By.XPATH, ".//tr[td[contains(text(),'Surface')]]/td[2]").text
                    except:
                        surface="non disponible"
                    # Extraire la ligne qui contient "Texte"
                    try:
                        desc = driver.find_element(By.XPATH, ".//tr[td[contains(text(),'Texte')]]/td[2]").text
                    except:
                        desc="Non disponible"

                    try:
                        loc = driver.find_element(By.XPATH, ".//tr[td[contains(text(),'Localisation')]]/td[2]").text
                    except:
                        loc="Non disponible"
                    
                    # Exemple : Si tu veux garder uniquement les lignes paires
                    try:
                        cellphone_data = driver.find_element(By.XPATH, "//li[@class='cellphone']/span").text
                    except:
                        cellphone_data="Non disponible"

                except:
                    continue  # Passer à l'hôtel suivant
                        # Tester l'ouverture d'un nouvel onglet
              # **Ouvrir un nouvel onglet et basculer dessus**


                driver.close()
                driver.switch_to.window(driver.window_handles[0])
    
            # Ajouter aux résultats
                annonces.append([region, nature, type_, texte, prix, modifie,surface,desc,cellphone_data,loc,details_link])
        except Exception as e:
                print(f"Erreur lors du traitement d'une ligne: {e}")


    print(f"Page {page} récupérée avec succès!")

# Fermer le navigateur
driver.quit()

# Sauvegarde dans un fichier Excel
df = pd.DataFrame(annonces, columns=["Région", "Nature", "Type", "Texte annonce", "Prix", "Modifiée","Superficie","Description","Numero","Localisation","details_link"])
df.to_excel("annonces_tunisie.xlsx", index=False)

print("Scraping terminé. Données enregistrées dans 'annonces_tunisie.xlsx'.")