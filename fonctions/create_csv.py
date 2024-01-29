import csv
import os

# Création fichier CSV
def write_csv(file_name, data):
    # Écrire l'en-tête une seule fois avant la boucle
    header = ["product_page_url",
              "universal_product_code",
              "title",
              "price_including_tax",
              "price_excluding_tax",
              "number_available",
              "product_description",
              "category",
              "review_rating",
              "image_url"]

    # Création d'un fichier pour écrire dans le fichier book_data.csv
    with open('data_file/' + file_name + '.csv', 'a', encoding='utf-8', newline='') as file_csv:
        # Création objet writer (écriture) avec ce fichier
        writer = csv.writer(file_csv, delimiter=',', fieldnames=header)
        # Permet de boucler les éléments
        writer.writerow(data)

        # création du dossier data_file s'il n'existe pas
        if not os.path.exists('../data_file'):
            os.makedirs('../data_file')
