# librairies utilisées
import requests
from bs4 import BeautifulSoup
import urllib.request
import os
from fonctions.save_picture import recup_img
from fonctions.create_csv import write_csv

# fonction regroupant toute les fonctions d'extraction de donnée des livres d'une catégorie
# qui sera ensuite appelé dans le main
def one_category(url_one_category, file_name):
    data_folder = 'data_file'

    # Vérification si les dossier existe
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    # Supprimer le fichier CSV s'il existe déjà
    if os.path.exists(file_name):
        os.remove(file_name)

    page_number = 1

    # Fonction pour récuperer l'url de la categorie. page number permet d'initialisé la page actuelle a 1.
    def url_category(url_one_category):
        # pour récupere l'url de la categorie
        response = requests.get(url_one_category)
        soup = BeautifulSoup(response.content, 'lxml')
        return soup

    # fonction pour recupérer les url des livres d'une category
    def url_book_category(next_page_url):
        # obtenir le contenu HTML de la page actuelle et beautiful pour analyser l'HTML
        response = requests.get(next_page_url)
        soup = BeautifulSoup(response.content, 'lxml')

        # Récupération des liens des livres sur la page actuelle
        book_links = soup.find_all('h3')
        for book_link in book_links:
            # boucle sur les liens pour construire url final
            relative_url = book_link.a['href']
            final_url = url_one_category + relative_url
            return final_url

    # fonction pour extraire les information des livres
    def info_book_category(final_url, next_page_url, file_name):
        # Écrire l'en-tête une seule fois avant la boucle
        header = ["product_page_url",
                  "universal_ product_code",
                  "title",
                  "price_including_tax",
                  "price_excluding_tax",
                  "number_available",
                  "product_description",
                  "category",
                  "review_rating",
                  "image_url"]
        write_csv(file_name, header)

        # boucle pour parcourir les pages
        while next_page_url:
            # extraction des donnes sur la page de chaque livre
            # 2eme requete pour acceder à la page specifique  du livre
            response_book = requests.get(final_url)
            # utilisation de beautiful soup pour analyse de la page du livre
            soup_book = BeautifulSoup(response_book.content, 'lxml')

            product_page_url = final_url
            title = soup_book.find("h1").text
            print("titre", title)
            review_rating = soup_book.find('p', class_='star-rating').get('class').pop()
            product_description = soup_book.find("article", {"class": "product_page"}).find_all("p")[3].text
            category = soup_book.find("ul", {"class": "breadcrumb"}).find_all("a")[2].text
            print("categorie", category)
            # On recherche tout les elements td de la page
            list_table = soup_book.find_all('td')
            # On recherche de l'element précis contenu uniquement dans les td
            universal_product_code = list_table[0].text
            price_including_tax = list_table[2].text
            price_excluding_tax = list_table[3].text
            number_available = list_table[5].text

            # pour enregistrer l'image
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

            # Appeler la fonction pour écrire dans le fichier CSV
            file_name = category
            write_csv(file_name, data, category)

            # enlever les caractere non supporter pour le nom de l'image
            clean_title = title.replace(":", "").replace("/", " ").replace('"', '').replace(
                'Ã©', 'é').replace(",", "").replace(".", "").replace("&", "").replace("*", "").replace("?", "").replace(
                "#", "")
            name_img = f"{clean_title}_image.jpg"
            image_path = os.path.join('data_file', category, name_img)
            # urlretrieve va enregistré l'image avec son nom et l'image
            urllib.request.urlretrieve(image_url, image_path)

            # Chercher le lien vers la page suivante Mise à jour de next_page_url si une page suivante existe, sinon,
            # le définir sur None pour arrêter la boucle.
            next_page = soup.find('li', class_='next')
            if next_page:
                next_page_url = url_one_category + next_page.a['href']
                page_number += 1
            else:
                next_page_url = None

    soup = url_category(url_one_category)
    next_page_url = url_one_category  # Initialisation de next_page_url avec l'URL de la catégorie
    final_url = url_book_category(next_page_url)
    info_book_category(final_url, next_page_url, file_name)


url_one_category = "https://books.toscrape.com/catalogue/category/books/childrens_11/"
file_name = category + '.csv'
one_category(url_one_category, file_name)

# Fin
print(f"Extraction terminée.")
print("fichier csv fait")
