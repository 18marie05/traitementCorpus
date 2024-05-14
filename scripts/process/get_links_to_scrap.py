import requests
from lxml import html
from urllib.parse import urljoin


"""
Ce script effectue le scraping de différents liens à partir d'une url de base contenue dans la variable url.
Les liens récupérés dans ce script pourront être réutilisés par la suite

L'environnement Python utilisé pour run ce script a besoin de différentes bibiothèques : 
    - requests, 
    - lxml, 
    - urllib.parse 
    pour effectuer le scraping et la navigation web. 
    
Ce script définit également une fonction `get_link_from_url()` qui prend une url et un chemin XPath comme arguments afin d'extraire différents lien de l'url principale.

Il est possible d'utiliser ce script pour une autre url et pour d'autres chemins XPath, il suffit de changer les valeurs de la variable `url` et de la liste `xpaths`

D'autres modifications pourraient être nécessaires en fonction de la structure du site web à scraper.

"""


# URL principale de la page à analyser
url = "https://plos.org/"

# Définition des chemins XPath pour récupérer les liens
xpaths = [
    '/html/body/div[2]/div/main/div/div/div/section[3]/div/div/div[1]/div/div/div[2]/div/div/p[2]/span[1]/a/@href',
    '/html/body/div[2]/div/main/div/div/div/section[3]/div/div/div[1]/div/div/div[2]/div/div/p[2]/span[2]/a[2]/@href',
    '/html/body/div[2]/div/main/div/div/div/section[3]/div/div/div[1]/div/div/div[2]/div/div/p[2]/span[4]/a/@href',
    '/html/body/div[2]/div/main/div/div/div/section[3]/div/div/div[1]/div/div/div[2]/div/div/p[2]/span[6]/a/@href'
]


# Liste pour stocker les liens à scraper
to_scrap = []

# Récupération du lien complet
def get_link_from_url(url, xpath):
    """
    Cette fonction récupère un lien à partir d'une url. Elle utilise XPath qui localise plusieurs éléments <a> spécifié par le chemin XPath donné.

    Args:
        url (str): url à partir de laquelle extraire les liens.
        xpath (str): chemin XPath spécifiant l'emplacement de l'élément <a> contenant le lien à récupérer.

    Returns:
        str: Lien absolu extrait à partir de l'élément <a> identifié par XPath, ou None si aucun lien n'a été extrait.
    """
    response = requests.get(url)
    if response.status_code == 200:
        tree = html.fromstring(response.content)
        # Utiliser XPath pour trouver l'élément <a> qui correspond au lien
        link_element = tree.xpath(xpath)
        if link_element:
            # Extraire l'attribut href de l'élément <a>
            full_link = link_element[0]
            if isinstance(full_link, html.HtmlElement):
                full_link = full_link.attrib.get('href')
            absolute_link = urljoin(url, full_link)
            return absolute_link
        else:
            print("Aucun élément <a> trouvé à l'emplacement spécifié pour :", url)
    else:
        print("Erreur lors de la récupération de la page :", response.status_code)

# Pour chaque lien extrait, accéder à la page et récupérer le lien complet avec XPath
for xpath in xpaths:
    # Récupérer le lien
    extracted_links = html.fromstring(requests.get(url).content).xpath(xpath)
    if extracted_links:
        link = extracted_links[0]
        # Accéder à la nouvelle page à partir du lien
        print("Accès à la page :", link)
        absolute_link = get_link_from_url(link, '//div[@class="more-link"]/a/@href')
        if absolute_link:
            # Ajouter le lien absolu à la liste 'to_scrap'
            to_scrap.append(absolute_link)
            print("Lien enregistré :", absolute_link)
            print("------------------------")
    else:
        print("Aucun lien trouvé à l'emplacement spécifié.")

print("Extraction des liens terminée. Les liens ont été stockés dans 'to_scrap'.")
print(to_scrap)