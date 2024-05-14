import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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

# Dossier pour enregistrer les abbréviations
output_dir = "data/abbreviations-raw"

try:
    os.makedirs(output_dir, exist_ok=True)

    # Configuration des options pour Firefox
    options = Options()
    options.headless = True
    options.add_argument(f"-profile {profile_path}")

    # Initialisation du Webdriver (Firefox)
    driver = webdriver.Firefox(service=service, options=options)

    # Itérer sur chaque catégorie et son URL
    for category, main_url in main_urls.items():
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

        # List pour collecter les textes d'abbréviations
        abbreviation_texts = []

        # Pour chaque élément <dt>, on cherche et on clique sur la balise <a> qui contient le lien de l'article
        for index, dt_element in enumerate(dt_elements, start=1):
            link_element = dt_element.find_element(By.XPATH, './a')
            link_url = link_element.get_attribute('href')

            # Ouverture du lien dans un nouvel onglet
            driver.execute_script("window.open();")
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(link_url)

            # Attendre que la page ait chargée avant de passer à la suite
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'articleinfo')))

            # Extraction de la section Abbreviation contenue dans la dernière balise <p> de articleInfo
            article_info = driver.find_element(By.CLASS_NAME, 'articleinfo')
            p_tags = article_info.find_elements(By.TAG_NAME, 'p')

            # Chercher la dernière balise <p>
            if p_tags:
                last_p_tag_text = p_tags[-1].text.strip()
                abbreviation_texts.append(last_p_tag_text)
                print(abbreviation_texts)

            # Fermeture de la page de l'article pour retourner sur la page principale
            # On recommence pour chaque article de la page principale puis pour chaque page principale de main_urls
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        # Ecrire le texte de la section Abbreviation dans le fichier correspondant
        if abbreviation_texts:
            output_file_path = os.path.join(output_dir, f"abbreviations_{category}.txt")
            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write("\n".join(abbreviation_texts))

except Exception as e:
    print(f"Error: {e}")

finally:
    # Fermeture du webdriver et Geckodriver
    driver.quit()
    service.stop()
