import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

books = []

print("Starting scraping...")

# Pagination loop
for page in range(1, 6):

    url = BASE_URL.format(page)

    # ---------------------------
    # ERROR HANDLING (IMPORTANT)
    # ---------------------------
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
    except Exception as e:
        print(f"Request failed for page {page}: {e}")
        continue

    # ---------------------------
    # STATUS CHECK (IMPORTANT)
    # ---------------------------
    if response.status_code != 200:
        print(f"Skipping page {page}, status code: {response.status_code}")
        continue

    time.sleep(1)

    soup = BeautifulSoup(response.text, "html.parser")

    items = soup.find_all("article", class_="product_pod")

    # Safety check
    if not items:
        print(f"No items found on page {page}")
        continue

    for item in items:
        try:
            title = item.h3.a["title"]
            price = item.find("p", class_="price_color").text
            rating = item.p["class"][1]

            books.append([title, price, rating])

        except Exception as e:
            print("Error parsing item:", e)
            continue

    print(f"Page {page} done")

# Save CSV
df = pd.DataFrame(books, columns=["Title", "Price", "Rating"])
df.to_csv("data.csv", index=False)

print("Scraping completed successfully!")
print("data.csv created")