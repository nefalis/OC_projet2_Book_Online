# librairies utilisées
import urllib.request
import os

# fonction pour récupérer l'url des images
def recup_img(parse_img):
    target_link_img = parse_img.find('div', class_="item active").find('img')['src']
    base_url_img = "http://books.toscrape.com/"
    # base url + target link permet d'avoir l'adresse de l'image complete et on remplace le '../../' de devant
    # par rien
    complete_link_img = base_url_img + target_link_img
    return complete_link_img.replace("../../", '')

# fonction pour enregistré les simages
def save_img(image_url, title, category):
    # Nettoyage des caractere non supporter pour le nom de l'image
    clean_title = title.replace(":", "").replace("/", " ").replace('"', '').replace(
        'Ã©', 'é').replace(",", "").replace(".", "").replace("&", "").replace("*", "").replace("?", "").replace(
        "#", "")
    name_img = f"{clean_title}_image.jpg"
    # Chemin pour enregistrer l'image
    image_path = os.path.join('data_file', category, name_img)
    # urlretrieve va enregistré l'image avec son nom et l'image
    urllib.request.urlretrieve(image_url, image_path)