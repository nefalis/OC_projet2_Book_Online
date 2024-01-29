import requests
from bs4 import BeautifulSoup
import urllib.request
from fonctions.one_category import one_category
from fonctions.one_book import recup_book

url_one_book = "http://books.toscrape.com/catalogue/charlie-and-the-chocolate-factory-charlie-bucket-1_13/index.html"
print(recup_book(url_one_book))

url_one_category = "https://books.toscrape.com/catalogue/category/books_1/"

print(one_category(url_one_category, file_name))
