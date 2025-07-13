import json
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
import json
from requests.cookies import cookiejar_from_dict
from typing import Dict

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
    storeURL = "https://www.starmarket.com/"
    cookies = cookieGetter(storeURL)
    session = requests.Session()
    proxy = "http://156.228.85.146:3129"
    session.proxies = {
       "http": proxy,
       "https": proxy,
    }
    session = loadCookies(session, cookies)

    #Check if IP is correct
    response = session.get("https://httpbin.org/ip")
    print(response.json())
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.starmarket.com/",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Cache-Control": "max-age=0"
    }
    
    for itemName in itemList:
        print("Finding: " + itemName + " on Star Market")
        URL = f"https://www.starmarket.com/shop/search-results.html?q={itemName}&tab=products"
        print(URL)
        response = session.get(URL, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        products = soup.find_all("product-item-al-v2", {"data-qa": "prd-itm"})
        
        with open("starmarket.html", "w", encoding="utf-8") as f:
            f.write(soup.prettify())
            
        print(f"Found {len(products)} products")
        non_sponsored_products = []
        for product in products:
            sponsored_element = product.find("span", {"data-qa": "prd-itm-spnsrd"})
            if not sponsored_element:
                non_sponsored_products.append(product)
        
        for product in non_sponsored_products[:num]:
            try:
                name_element = product.find("a", {"data-qa": "prd-itm-pttl"})
                name = name_element.get_text(strip=True) if name_element else ""
                price_element = product.find("span", {"data-qa": "prd-itm-prc"})
                price_text = ""
                if price_element:
                    price_span = price_element.find("span", {"aria-hidden": "true"})
                    if price_span:
                        price_text = price_span.get_text(strip=True)
                
                price = 0.0
                if price_text:
                    price_clean = re.sub(r'[^\d.]', '', price_text)
                    try:
                        price = float(price_clean)
                    except ValueError:
                        price = 0.0
                
                quantity_element = product.find("span", {"data-qa": "prd-itm-sqty"})
                quantity_text = quantity_element.get_text(strip=True) if quantity_element else ""
                
                quantity = re.search(r'(\d+(?:\.\d+)?)\s*(ct|count|oz|gallon|gal|pack|pk|pcs|each|EA|lb|lbs)', 
                                   name + " " + quantity_text, re.IGNORECASE)
                if quantity:
                    quantityUnits = f"{quantity.group(1)} {quantity.group(2)}"
                else:
                    quantityUnits = quantity_text if quantity_text else "1 each"
                
                url_element = product.find("a", {"data-qa": "prd-itm-pttl"})
                href = url_element.get("href", "") if url_element else ""
                itemURL = f"https://www.starmarket.com{href}" if href.startswith("/") else href
                
                quality = 0.75
                
                rating_element = product.find("div", class_="rating-stars")
                if rating_element:
                    sr_only = rating_element.find("span", class_="sr-only")
                    if sr_only:
                        rating_text = sr_only.get_text()
                        rating_match = re.search(r'Rated ([\d.]+) out of 5', rating_text)
                        if rating_match:
                            rating = float(rating_match.group(1))
                            quality = rating / 5.0  # Convert to 0-1 scale
                
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
                print(f"Error processing product: {e}")
                continue
                
    return pd.DataFrame(rows)

#print(starmarket("Eggs", 10))