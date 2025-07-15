import json
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
import json
from requests.cookies import cookiejar_from_dict
from typing import Dict
from urllib.parse import urlencode
import math
import random

def cookieGetter(storeURL):
    print("Made It Here")
    url = "http://localhost:8191/v1"
    headers = {"Content-Type": "application/json"}
    data = {
        "cmd": "request.get",
        "url": storeURL,
        "maxTimeout": 60000,
        "returnOnlyCookies": True,
        "proxy" : "156.228.85.146:3129"
    }
    response = requests.post(url, headers=headers, json=data)
    print(response.status_code)
    return response.json()["solution"]["cookies"]

def loadCookies(session: requests.Session, cookiesDict: Dict):
    cookie = {}
    for elem in cookiesDict:
        cookie[elem["name"]] = elem["value"]
    session.cookies = cookiejar_from_dict(cookie)
    return session

def walmart(itemList, num):
    print("Scraping Walmart")
    rows = []
    if isinstance(itemList, str):
        itemList = [itemList]
    
    for itemName in itemList:
        payload = {
            'api_key': '852615c755f41faf2cc763b2f8c8a54a',
            'query': itemName,
            'tld': 'com'
        }
        r = requests.get('https://api.scraperapi.com/structured/walmart/search', params=payload)
        data = json.loads(r.text)
        
        with open("walmarttest.json", "w", encoding="utf-8") as f:
            f.write(r.text)
        
        items_added = 0
        for item in data.get("items", []):
            if item.get("sponsored") is True:
                continue
            
            name = item.get("name", "")
            price = item.get("price", 0.0)
            rating = item.get("rating", {}).get("average_rating", 0.0)
            url = item.get("url", "")
            productName = item.get("name", "")
            
            quantityMatch = re.search(r'(\d+(?:\.\d+)?)\s*(Count|ct|pieces|pcs|oz|gallon|gal|pack|pk|each|EA|lb|lbs)', name, re.IGNORECASE)
            if quantityMatch:
                quantityUnits = f"{quantityMatch.group(1)} {quantityMatch.group(2)}"
            else:
                quantityUnits = "1 each"
            
            quality = round(rating / 5.0, 2)
            if quality == 0:
                quality = .75
        
            rows.append({
                "item": itemName,
                "price": price,
                "quantity": quantityUnits,
                "quality": quality,
                "store": "Walmart",
                "URL": url,
                "productName": productName
            })
            items_added += 1
            if items_added >= num:
                break

    return pd.DataFrame(rows)

def hannaford(itemList, num):
    print("Scraping Hannaford")
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
    for itemName in itemList:
        URL = f"https://www.hannaford.com/search/product?form_state=searchForm&keyword={itemName}&ieDummyTextField=&productTypeId=P"
        response = requests.get(URL, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        products = soup.find_all("div", class_="plp_thumb_wrap product-impressions")
        
        with open("hannaford_page.html", "w", encoding="utf-8") as f:
            f.write(soup.prettify())
            
        print(f"Found {len(products)} products")
        non_sponsored_products = []
        for product in products:
            sponsored_element = product.find("div", class_="elevaate-icon-text")
            if not sponsored_element or "Sponsored" not in sponsored_element.get_text(strip=True):
                non_sponsored_products.append(product)
        
        for product in non_sponsored_products[:num]:
            name = product.get("data-name", "").strip()
            price = float(product.get("data-price", "0.0").strip() or 0.0)
            unit = product.get("data-variant", "").strip()
            
            quantity = re.search(r'(\d+(?:\.\d+)?)\s*(ct|count|oz|gallon|gal|pack|pk|pcs|each|EA|lb|lbs)', name + " " + unit, re.IGNORECASE)
            if quantity:
                quantityUnits = f"{quantity.group(1)} {quantity.group(2)}"
            else:
                quantityUnits = unit if unit else "1 each"
            
            quality = 0.75  
            productInfo = product.find("div", class_="catalog-product")
            href = productInfo.get("data-url", "") if productInfo else ""
            productName = productInfo.get("data-product-name", "")
            itemURL = f"https://www.hannaford.com{href}" 
            
            rows.append({
                "item": itemName,
                "price": price,
                "quantity": quantityUnits,
                "quality": quality,
                "store": "Hannaford",
                "URL": itemURL,
                "productName" : productName
            })
    return pd.DataFrame(rows)  

def starmarket(itemList, num):
    print("Scraping Star Market")
    rows = []
    
    if isinstance(itemList, str):
        itemList = [itemList]

    headers = {
        "accept": "application/json, text/plain, */*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "ocp-apim-subscription-key": "5e790236c84e46338f4290aa1050cdd4",
    }

    token = "3:HzkqWVcMvHxRwVt1SGQDqg==:Q3ovQLgAtEQEfNCAX9LwqFMFSb7dmM5Ra+xlaI1kNNPjvhRR//OK/o7HfdMJwJzFPV3EJgyIWj8GMbHFEiBkT8HneGf5S+RBJkNy1wZ8nMolIA1EINOf0idZVki5yf+q+at3Zh1FYkkH+fL0YaZf40Be592w68QBa5mtXb8FhGUI65KxxOZWVOwBuemMG3KS9pCZFy6rWsc6+P5ozxmsgVj/puglRyIt8uW2tQABSEoTkV0nHpIF9eLsmcR9ObaP9OqfxfpEHRgyOmL131owt7NYXmamaQErHfGpriD7WkxV4NoZCXSzOog92DmepASDm+J8Kc2a2iDX8W3gmDFjwlT7IvRGPZUejgRTfryHGgaXaUmqQKappMTp+PZEb0zxBvdtvDmTsnePzgkVQHESqhnxTLkeegY0OPmZFHQoYToTj34As7DcGG495TPsEqFiBlthuxIaoS4N7kpkyzmrlLnyhjBjUJDQRIgI9EZM9nb+R8cGsficDw/0joaqIE7TfGJo0kvc8bv0HeUR8qmdc8EjkHRjBLzq4vWCC4yAafc=:kaOC6WGuZOnhgMSzfi1iSU4Lx5w32Tk5hiJTuuiOpcE="
    cookies = {
        "reese84": token
    }

    session = requests.Session()
    URL = "https://www.starmarket.com/abs/pub/xapi/pgmsearch/v1/search/products"

    for itemName in itemList:
        print("Finding:", itemName)
        requestID = math.floor(1e13 * random.random())
        requestID = f"{requestID}"
        params = {
            "request-id": "5261752605320579594",
            "url": "https://www.starmarket.com",
            "pageurl": "https://www.starmarket.com",
            "pagename": "search",
            "rows": "30",
            "start": "0",
            "search-type": "keyword",
            "storeid": "2576",
            "featured": "false",
            "q": itemName,
            "sort": "",
            "dvid": "web-4.1search",
            "channel": "instore",
            "visitorId": "2efdbc64-e6f8-4623-9fde-349bb9177ca4",
            "pgm": "intg-search,merch-banner",
            "banner": "starmarket"
        }

        try:
            response = session.get(URL, headers=headers, cookies=cookies, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"Failed to fetch products for {itemName}: {e}")
            continue

        docs = data.get("primaryProducts", {}).get("response", {}).get("docs", [])
        print(f"Found {len(docs)} products for {itemName}")

        for product in docs[:num]:
            try:
                name = product.get("name", "")
                price = float(product.get("price", 0.0))
                unit_quantity = product.get("unitQuantity", "1")
                unit_measure = product.get("unitOfMeasure", "ea")
                quantityUnits = f"{unit_quantity} {unit_measure}"

                review = product.get("productReview", {})
                rating = float(review.get("avgRating", 0.0))
                quality = rating / 5.0 if rating else 0.75

                itemURL = f"https://www.starmarket.com/shop/product-details/{product.get('pid')}"

                rows.append({
                    "item": itemName,
                    "price": price,
                    "quantity": quantityUnits,
                    "quality": quality,
                    "store": "Star Market",
                    "URL": itemURL,
                    "productName": name
                })

            except Exception as e:
                print(f"Error parsing product JSON for '{itemName}': {e}")
                continue

    return pd.DataFrame(rows)

def shaws(itemList, num):
    print("Scraping Star Market")
    rows = []
    
    if isinstance(itemList, str):
        itemList = [itemList]

    headers = {
        "accept": "application/json, text/plain, */*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "ocp-apim-subscription-key": "5e790236c84e46338f4290aa1050cdd4",
    }

    token = "3:NCG3HcQFTcCA+7XGE2XOzg==:D94hyANuMVxIXfvy+utu2zwcNA5iPht4ymhsKSXPquCP8XFDdlDQq/39yGp+hOms4vhlD7Yrx36c+2sg9dEUQkLTGbngmuY25dWDrWh23piL1pe4okiDKFK9MlB7Xot/lkTHrpICZXmX4TtjdAlFkdJXl05NmO1fi28bW77tg5LMleVwJAdycsoNiaYMJ9t2+cRWnMR9lEStmmtAFi7vjqUH2qRIF3mHdJKoipeg4xxoUmAlA2Ol/dit6szmkjzi5s2BVI0ymEoaFGF7P24TPdOlG+b74fP8zKLoCuCWbepGfQ6NwRsz5Z9CBnGwsyYZX4bOJ0S7Z7PyCbVoTq2Ze2nYntSE1OxnuXOT+hpJ0ZM84RfkPM5guMXDItOVvohe8j7QXm5hUSvdmSt6SAAROyP5TB7PiU/SmvyiXsq/vVKY7tau8fF1AqKJXtMu09FQa+VI6a0rQGItkF42oaiTqSNb3XDE/HtCMurtexJ1JciVk/WT33YYS5SH2sq8/DG8uQIhMOQrqhByD2mJZyNPzYjdlxR1DInk+Nl5nm/BDtg=:DaJ6DPc+/e4GCuMj3ozR/2IRNEZlkY0vn4KB4nivzdU="
    cookies = {
        "reese84": token
    }

    session = requests.Session()
    URL = "https://www.shaws.com/abs/pub/xapi/pgmsearch/v1/search/products"

    for itemName in itemList:
        print("Finding:", itemName)
        requestID = math.floor(1e13 * random.random())
        requestID = f"{requestID}"
        params = {
            "request-id": "7201752605321844545",
            "url": "https://www.shaws.com",
            "pageurl": "https://www.shaws.com",
            "pagename": "search",
            "rows": "30",
            "start": "0",
            "search-type": "keyword",
            "storeid": "2576",
            "featured": "false",
            "q": itemName,
            "sort": "",
            "dvid": "web-4.1search",
            "channel": "instore",
            "visitorId": "2efdbc64-e6f8-4623-9fde-349bb9177ca4",
            "pgm": "intg-search,merch-banner",
            "banner": "shaws"
        }

        try:
            response = session.get(URL, headers=headers, cookies=cookies, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"Failed to fetch products for {itemName}: {e}")
            continue

        docs = data.get("primaryProducts", {}).get("response", {}).get("docs", [])
        print(f"Found {len(docs)} products for {itemName}")

        for product in docs[:num]:
            try:
                name = product.get("name", "")
                price = float(product.get("price", 0.0))
                unit_quantity = product.get("unitQuantity", "1")
                unit_measure = product.get("unitOfMeasure", "ea")
                quantityUnits = f"{unit_quantity} {unit_measure}"

                review = product.get("productReview", {})
                rating = float(review.get("avgRating", 0.0))
                quality = rating / 5.0 if rating else 0.75

                itemURL = f"https://www.shaws.com/shop/product-details/{product.get('pid')}"

                rows.append({
                    "item": itemName,
                    "price": price,
                    "quantity": quantityUnits,
                    "quality": quality,
                    "store": "Star Market",
                    "URL": itemURL,
                    "productName": name
                })

            except Exception as e:
                print(f"Error parsing product JSON for '{itemName}': {e}")
                continue

    return pd.DataFrame(rows)

