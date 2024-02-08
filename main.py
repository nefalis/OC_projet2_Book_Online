import requests
from bs4 import BeautifulSoup

from fonctions.one_category import one_category

print("debut")
# Récupération de la page d'acceuil. page number permet d'initialisé la page actuelle a 1.
base_url = "https://books.toscrape.com/"
page_number = 1

# obtenir le contenu HTML de la page actuelle et beautiful pour analyser l'HTML
response = requests.get(base_url)
soup = BeautifulSoup(response.content, 'lxml')
link_category = []

# Trouver le menu de navigation contenant les catégories
nav_menu = soup.select('.nav-list >li > ul')
# Trouver toutes les catégories
categories = nav_menu[0].find_all('a')

# Afficher les catégories
#  la méthode .strip() est utilisée pour supprimer les espaces et les sauts de ligne éventuels autour du texte
for category in categories:
    category_name = category.text.strip()
    category_url = base_url + category['href']
    category_url = category_url.replace('index.html', '')

    name_csv = "{category_name}.csv"
    one_category(category_url, name_csv)

print("fin")
print("fichier data fait !! ")

