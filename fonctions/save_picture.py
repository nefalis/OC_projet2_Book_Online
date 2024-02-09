# Librairies utilisées
import urllib.request
import os

# Fonction pour récupérer l'url des images
def recup_img(parse_img):
    target_link_img = parse_img.find('div', class_="item active").find('img')['src']
    base_url_img = "http://books.toscrape.com/"
    # Base url + target link permet d'avoir l'adresse de l'image complete et on remplace le '../../' de devant
    # par rien
    complete_link_img = base_url_img + target_link_img
    return complete_link_img.replace("../../", '')

# Fonction pour enregistré les images
def save_img(image_url, title, category):
    # Nettoyage des caracteres non supporter pour le nom de l'image
    clean_title = title.replace(":", "").replace("/", " ").replace('"', '').replace(
        'Ã©', 'e').replace(",", "").replace(".", "").replace("&", "").replace("*", "").replace("?", "").replace(
        "#", "").replace("é", "e")
    # Limiter le nombre à 50 caractères
    clean_title = clean_title[:50]
    # Nom de l'image
    name_img = f"{clean_title}.jpg"
    # Chemin pour enregistrer l'image
    image_path = os.path.join('data_file', category, name_img)
    # urlretrieve va enregistré l'image avec son nom
    urllib.request.urlretrieve(image_url, image_path)
