import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



"""
Ce script permet de scraper différentes urls contenues dans le dictionnaire main_urls afin de récupérer leurs contenus textuels.

L'environnement Python utilisé pour run ce script a besoin de différents paquets : 
    - os
    - time
    - BeautifulSoup
    - selenium
    - un webdriver pour Firefox

Différentes variables sont à modifier si le script doit être réutilisé : 
    - profile_path qui est le chemin du profile Firefox à utiliser pour le scraping.
    - geckodriver_path qui est le chemin du Webdriver installé sur votre machine.


Chaque article scrapé est enregistré dans un dossier portant le nom de la clé du dictionnaire main_urls, puis dans un fichier .txt

"""


# Chemin du profile Firefox
profile_path = "/home/marie18/snap/firefox/common/.mozilla/firefox/93o6mgh5.default"

# Chemin du Geckodriver installé
geckodriver_path = '/usr/local/bin/geckodriver'

# Configuration du service Geckodriver
service = Service(executable_path=geckodriver_path)
service.start()

# Dictionnaire des urls pour chaque catégorie du PLOS journal à scraper
main_urls = {
    'Biology': "https://journals.plos.org/plosbiology/search?filterJournals=PLoSBiology&filterStartDate=2024-04-10&filterEndDate=2024-05-10&q=&sortOrder=DATE_NEWEST_FIRST",
    'ComputationalBiology': "https://journals.plos.org/ploscompbiol/search?sortOrder=DATE_NEWEST_FIRST&filterStartDate=2024-04-10&filterEndDate=2024-05-10&filterJournals=PLoSCompBiol&q=",
    'Genetics': "https://journals.plos.org/plosgenetics/search?sortOrder=DATE_NEWEST_FIRST&filterStartDate=2024-04-10&filterEndDate=2024-05-10&filterJournals=PLoSGenetics&q=",
    'Medicine': "https://journals.plos.org/plosmedicine/search?sortOrder=DATE_NEWEST_FIRST&filterStartDate=2024-04-10&filterEndDate=2024-05-10&filterJournals=PLoSMedicine&q="
}

try:
    # Configuration des options pour Firefox
    options = Options()
    options.headless = True
    options.add_argument(f"-profile {profile_path}")  # Utilisation du profile Firefox

    # Initialisation du Webdriver (Firefox)
    driver = webdriver.Firefox(service=service, options=options)

    # Itérer sur chaque catégorie et son URL pour enregistrer les artiles scrapés
    for category, main_url in main_urls.items():
        category_dir = f"data/raw/{category}"
        os.makedirs(category_dir, exist_ok=True)

        # Ouverture de la page principale
        driver.get(main_url)

        # Chercher l'emplacement des éléments StartDate et EndDate sur chaque page (on souhaite chercher des articles à une date spécifique)
        start_date_input = driver.find_element(By.XPATH, '//*[@id="dateFilterStartDate"]')
        end_date_input = driver.find_element(By.XPATH, '//*[@id="dateFilterEndDate"]')

        # Remplacer les valeurs de date de début et date de fin par des dates choisies
        start_date_input.clear()
        start_date_input.send_keys("2020-05-04")
        end_date_input.clear()
        end_date_input.send_keys("2021-05-04")

        # "Cliquer" sur le boutton Apply pour sauvegarder les modifications
        apply_button = driver.find_element(By.XPATH, '//*[@id="searchFilters"]/form/button')
        apply_button.click()

        # Ajouter un délai d'attente avant de passer à la suite (5 secondes)
        time.sleep(5)

        # Attente du chargement de la page
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'searchResultsList')))

        # Chercher tous les éléments <dt> de la page principale
        # Les éléments <dt> sont les liens des articles dont on veut récupérer le contenu textuel
        dt_elements = driver.find_elements(By.XPATH, '//*[@id="searchResultsList"]/dt')

        # Pour chaque élément <dt>, on cherche et on clique sur la balise <a> qui contient le lien de l'article
        for index, dt_element in enumerate(dt_elements, start=1):
            link_element = dt_element.find_element(By.XPATH, './a')
            link_url = link_element.get_attribute('href')

            # Ouverture du lien dans un nouvel onglet
            driver.execute_script("window.open();")
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(link_url)

            # Attendre que la page ait chargée avant de passer à la suite
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="artText"]')))

            # Extraction du contenu textuel de l'article
            article_content = driver.find_element(By.XPATH, '//*[@id="artText"]')

            # Utilisation de BeautifulSoup
            soup = BeautifulSoup(article_content.get_attribute('innerHTML'), 'html.parser')

            # Récupération du texte
            plain_text = soup.get_text(separator=' ', strip=True)

            # Sauvegarder le contenu textuel
            file_path = os.path.join(category_dir, f"article_{index}.txt")

            # Ecrire le contenu textuel dans le fichier .txt
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(plain_text)

            # Fermeture de la page de l'article pour retourner sur la page principale
            # On recommence pour chaque article de la page principale puis pour chaque page principale de main_urls
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

except Exception as e:
    print(f"Error: {e}")

finally:
    # Fermeture du webdriver et Geckodriver
    driver.quit()
    service.stop()
