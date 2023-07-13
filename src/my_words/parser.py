import requests
from bs4 import BeautifulSoup

link = 'https://quotes.toscrape.com/'
response = requests.get(link)
soup = BeautifulSoup(response.text, 'lxml')
