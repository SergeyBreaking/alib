import re

from database import session_scope, create_car_table, create_car_image_table
from bs4 import BeautifulSoup as bs
import requests
from selenium_scrapper import SeleniumScraper

url = 'https://www.alibaba.com/product-detail/2023-1-2T-Toyota-Japan-Large_1600898730837.html'
scrapper = SeleniumScraper()
responce = scrapper.get_response(url)

soup = bs(responce, 'html.parser')

element = soup.find('div', id='popup-root')
print(element)
