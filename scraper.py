import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

HEADERS = {"User-Agent": "Mozilla/5.0"}

books = []

print("Starting scraping...")

for page in range(1, 6):
    url = BASE_URL.format(page)
    response = requests.get(url, headers=HEADERS)
    time.sleep(1)

    soup = BeautifulSoup(response.text, "html.parser")

    items = soup.find_all("article", class_="product_pod")

    for item in items:
        title = item.h3.a["title"]
        price = item.find("p", class_="price_color").text
        rating = item.p["class"][1]

        books.append([title, price, rating])

    print(f"Page {page} done")

print("Scraping finished")