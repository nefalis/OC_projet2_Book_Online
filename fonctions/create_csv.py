import csv
import os

# Création fichier CSV
def write_csv(file_name, data, category):

    # Création du dossier data_file s'il n'existe pas
    if not os.path.exists('data_file'):
        os.makedirs('data_file')

    # Création du sous-dossier correspondant à la catégorie s'il n'existe pas
    category_path = os.path.join('data_file', category)
    if not os.path.exists(category_path):
        os.makedirs(category_path)

    # Modifier le chemin de sauvegarde du fichier CSV pour l'enregistrer dans le sous-dossier correspondant à la
    # catégorie
    file_path = os.path.join(category_path, file_name + '.csv')

    # Vérifier si le fichier existe
    file_exists = os.path.exists(file_path)

    # Création d'un fichier pour écrire dans  data_file.csv
    with open(file_path, 'a', encoding='utf-8', newline='') as file_csv:
        # Création objet writer (écriture) avec ce fichier
        writer = csv.writer(file_csv, delimiter=',')

        # Écrire l'en-tête si le fichier n'existe pas
        if not file_exists:
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
            writer.writerow(header)

        # Permet de boucler les éléments
        writer.writerow(data)

