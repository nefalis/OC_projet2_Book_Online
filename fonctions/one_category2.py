# librairies utilisées
import requests
from bs4 import BeautifulSoup
import urllib.request
import os
from fonctions.save_picture import recup_img
from fonctions.create_csv import write_csv

# fonction pour extraire les informations des livres d'une catégorie
def one_category(base_url, file_name):
    print("start one cat")
    # Nom du dossier où seront stocké les données extraites
    data_folder = 'data_file'
    # Chemin du dossier image

    # Vérification (exists) et création des dossiers (makedirs)
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    if os.path.exists(file_name):
        os.remove(file_name)

    # Page number permet d'initialisé la page actuelle a 1.
    page_number = 1
    next_page_url = base_url

    # Boucle pour parcourir les pages de la catégorie
    while next_page_url:
        # Récupération du contenu HTML de la page actuelle et beautiful pour analyser l'HTML
        response = requests.get(next_page_url)
        soup = BeautifulSoup(response.content, 'lxml')

        # Récupération des liens des livres sur la page actuelle
        book_links = soup.find_all('h3')

        # Boucle sur les liens des livres pour extraire les informations
        for book_link in book_links:
            print("je cherche des livres")
            relative_url = book_link.a['href']
            # URL complet du livre
            final_url = base_url + relative_url

            # extraction des données sur la page de chaque livre
            response_book = requests.get(final_url)
            soup_book = BeautifulSoup(response_book.content, 'lxml')

            # Extraction des informations spécifiques du livre
            product_page_url = final_url
            title = soup_book.find("h1").text
            review_rating = soup_book.find('p', class_='star-rating').get('class').pop()
            product_description = soup_book.find("article", {"class": "product_page"}).find_all("p")[3].text
            category = soup_book.find("ul", {"class": "breadcrumb"}).find_all("a")[2].text
            # On recherche tout les elements td de la page
            list_table = soup_book.find_all('td')
            # On recherche de l'element précis contenu uniquement dans les td
            universal_product_code = list_table[0].text
            price_including_tax = list_table[2].text
            price_excluding_tax = list_table[3].text
            number_available = list_table[5].text

            # Récupération de l'URL de l'image du livre
            image_url = recup_img(soup_book)

            # Ajouter les données du livre à la liste
            data = [product_page_url,
                    universal_product_code,
                    title,
                    price_including_tax,
                    price_excluding_tax,
                    number_available,
                    product_description,
                    category,
                    review_rating,
                    image_url]

            # Appel de la fonction pour écrire dans le fichier CSV
            file_name = category
            write_csv(file_name, data, category)

            # Nettoyage des caractere non supporter pour le nom de l'image
            clean_title = title.replace(":", "").replace("/", " ").replace('"', '').replace(
                'Ã©', 'é').replace(",", "").replace(".", "").replace("&", "").replace("*", "").replace("?", "").replace(
                "#", "")
            name_img = f"{clean_title}_image.jpg"
            # Chemin pour enregistrer l'image
            image_path = os.path.join('data_file', category, name_img)
            # urlretrieve va enregistré l'image avec son nom et l'image
            urllib.request.urlretrieve(image_url, image_path)

        # Mise à jour de next_page_url si une page suivante existe, sinon, le définir sur None pour arrêter la boucle.
        next_page = soup.find('li', class_='next')
        if next_page:
            next_page_url = base_url + next_page.a['href']
            page_number += 1
        else:
            next_page_url = None

"""# Définition des paramètres de la fonction One_category
base_url = "https://books.toscrape.com/catalogue/category/books/childrens_11/"
file_name = "exemple.csv"

# Appel de la fonction pour extraire les données
one_category(base_url, file_name)"""
