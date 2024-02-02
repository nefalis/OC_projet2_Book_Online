# librairies utilisées
import urllib.request

# fonction pour récupérer l'url des images
def recup_img(parse_img):
    target_link_img = parse_img.find('div', class_="item active").find('img')['src']
    base_url_img = "http://books.toscrape.com/"
    # base url + target link permet d'avoir l'adresse de l'image complete et on remplace le '../../' de devant
    # par rien
    complete_link_img = base_url_img + target_link_img
    return complete_link_img.replace("../../", '')
