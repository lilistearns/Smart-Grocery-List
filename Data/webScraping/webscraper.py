import json
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup


def walmart(itemList, num):
    rows = []

    if isinstance(itemList, str):
        itemList = [itemList]

    for itemName in itemList:
        print(itemName)
        payload = {
            'api_key': '852615c755f41faf2cc763b2f8c8a54a',
            'query': itemName,
            'tld': 'com'
        }
        r = requests.get('https://api.scraperapi.com/structured/walmart/search', params=payload)
        data = json.loads(r.text)

        for item in data.get("items", [])[:num]:
            name = item.get("name", "")
            price = item.get("price", 0.0)
            rating = item.get("rating", {}).get("average_rating", 0.0)
            url = item.get("url", "")
            
            quantityMatch = re.search(r'(\d+)\s*(Count|ct|pieces|pcs)', name, re.IGNORECASE)
            quantityUnits = int(quantityMatch.group(1)) if quantityMatch else 1

            quality = round(rating / 5.0, 2)
            if quality == 0:
                quality = .5

            rows.append({
                "item": itemName,
                "price": price,
                "quantity": quantityUnits,
                "quality": quality,
                "store": "Walmart",
                "URL": url
            })

    return pd.DataFrame(rows)

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def hannaford(itemList, num):
    rows = []

    if isinstance(itemList, str):
        itemList = [itemList]

    headers = {
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Referer": "https://www.hannaford.com/",
                    "DNT": "1",
                    "Connection": "keep-alive",
                    "Upgrade-Insecure-Requests": "1",
                    "Sec-Fetch-Dest": "document",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-Site": "same-origin",
                    "Cache-Control": "max-age=0"
                }
    print("Made it here")
    for itemName in itemList:
        URL = f"https://www.hannaford.com/search/product?form_state=searchForm&keyword={itemName}&ieDummyTextField=&productTypeId=P"
        print(URL)
        response = requests.get(URL, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        products = soup.find_all("div", class_="plp_thumb_wrap product-impressions visited-product-impressions")
        with open("hannaford_page.html", "w", encoding="utf-8") as f:
            f.write(soup.prettify())
        for product in products[:num]:
            name = product.get("data-name", "").strip()
            price = float(product.get("data-price", "0.0").strip() or 0.0)
            unit = product.get("data-variant", "").strip()


            quantity = re.search(r'(\d+)\s*(ct|count|oz|gallon|pack|pk|pcs|each|EA)', name + " " + unit, re.IGNORECASE)
            quantityUnits = int(quantity.group(1)) if quantity else 1
            quality = 0.5  
            productInfo = product.find("div", class_="catalog-product")
            href = productInfo.get("data-url", "") if productInfo else ""
            itemURL = f"https://www.hannaford.com{href}" 

            rows.append({
                "item": itemName,
                "price": price,
                "quantity": quantityUnits,
                "quality": quality,
                "store": "Hannaford",
                "URL": itemURL
            })

    return pd.DataFrame(rows)


print(hannaford("Milk",10))
