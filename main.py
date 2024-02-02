import requests
from bs4 import BeautifulSoup

from fonctions.one_category2 import one_category

print("debut")
# Récupération de la page d'acceuil. page number permet d'initialisé la page actuelle a 1.
base_url = "http://books.toscrape.com/"
page_number = 1

# obtenir le contenu HTML de la page actuelle et beautiful pour analyser l'HTML
response = requests.get(base_url)
soup = BeautifulSoup(response.content, 'lxml')
link_category = []

# Trouver le menu de navigation contenant les catégories
nav_menu = soup.find('div', class_='side_categories')
# Trouver toutes les catégories
categories = nav_menu.find_all('a')

# Afficher les catégories
#  la méthode .strip() est utilisée pour supprimer les espaces et les sauts de ligne éventuels autour du texte
for category in categories:
    print("je cherche des cat")
    category_name = category.text.strip()
    category_url = base_url + category['href']
    category_url = category_url.replace('index.html', '')
    link_category.append(category_url)
    print("liste cat")
    print("url cat", category_url)
    print("nom cat", category_name)

    name_csv = "{category_name}.csv"
    print("avant appel one cat")
    one_category(category_url, name_csv)
print("fin")
