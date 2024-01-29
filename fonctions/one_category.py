# librairies utilisées
import requests
from bs4 import BeautifulSoup
import urllib.request
import csv
import os
from fonctions.save_picture import recup_img
from fonctions.create_csv import write_csv

print("trululu")
"""# Création fichier CSV
def write_csv(file_name, data):
    # création du dossier data_file s'il n'existe pas
    if not os.path.exists('data_file'):
        os.makedirs('data_file')

    # Création d'un fichier pour écrire dans  data_file.csv
    with open('data_file/' + file_name + '.csv', 'a', encoding='utf-8', newline='') as file_csv:
        # Création objet writer (écriture) avec ce fichier
        writer = csv.writer(file_csv, delimiter=',')
        # Permet de boucler les éléments
        writer.writerow(data)"""

def one_category(url_one_category, file_name):

    print("pouet")
    # Supprimer le fichier CSV s'il existe déjà
    if os.path.exists(file_name):
        os.remove(file_name)

    """# Écrire l'en-tête une seule fois avant la boucle
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

    write_csv(file_name, header)"""

    # Récupération de la page catégorie. page number permet d'initialisé la page actuelle a 1.
    page_number = 1
    next_page_url = url_one_category
    # boucle pour parcourir les pages
    while next_page_url:
        # obtenir le contenu HTML de la page actuelle et beautiful pour analyser l'HTML
        response = requests.get(next_page_url)
        soup = BeautifulSoup(response.content, 'lxml')

        # Récupération des liens des livres sur la page actuelle
        book_links = soup.find_all('h3')
        for book_link in book_links:
            # boucle sur les liens pour construire url final
            relative_url = book_link.a['href']
            final_url = url_one_category + relative_url

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
            name_img = f"{title}_image.jpg"
            # urlretrieve va enregistré l'image avec son nom et l'image
            urllib.request.urlretrieve(image_url, name_img)

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
            write_csv(file_name, data)

        # Chercher le lien vers la page suivante
        # Mise à jour de next_page_url si une page suivante existe, sinon, le définir sur None pour arrêter la boucle.
        next_page = soup.find('li', class_='next')
        if next_page:
            next_page_url = url_one_category + next_page.a['href']
            page_number += 1
        else:
            next_page_url = None

    # Après chaque boucle affichage du nombre total total de pages traitées
    print(f"Extraction terminée.")
    print("fichier csv fait")

# programme principal

"""
file_name = 'book_data.csv'
base_url = "https://books.toscrape.com/catalogue/category/books_1/"

one_category(base_url, file_name)"""

"""one_category => Uniquement ce qui concerne la recupération de toute ta catégorie !
Soit tu crée un fihier externe avec juste la recup des informations d('un livre  SOIt tu ré écris '
                                                                      'ton extraction d')information d'un livre dans one category.
Tout ça ( tout ton code que one catégori , le mettre dans une fonction - fonction recup one catégory )
Aller travailler sur le fichier externe csv pour vérifier que ta fonction csv elle fonctionne dans son fichier seule .
soit tu vas dans le main , SOIt tu vas dans ton one catégory ( Tu vas appeler la fonction csv fichier externe pour la
faire fonctionne avec le parametrre de ta fonction recup one catgory)

Guide d'étape one catégory :

fonction 1  = recup url catégory

fonction 2 = recup tous les url de tout les livre de ta cétgory

fonction 3 = fonction extraction information  sans les prints

fonction 4 = Rassemble fonction 1 à 3 + fichier externe csv + fichier externe telechargement image

Focntion 4 tu l'appelles dans le main
"""
