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

    token = "3:ZMQfNdiQU6L87zW2hg81pA==:/5hDB+FgGXk3i1QrRco7DAmvkBFaQH0pJ+H5wnCTKMFEYDE+lzkgnSfiytr0jhZoeEN59GaTb+ik1X15zCnmfWEiiUQBPWCOmpEA2sqctjlF3j20g0XdNKbRe15YP9091htEibaEwTg9P/3sLkSE78JiAIJJXqH0qaomMNfNHZl6MJMngrzYoGuhTw7t8YsM7+EdwYpHkMBdNKqi8JapJaIWPVrXnTQrB//BmqDm2Lpfzz7SEdrpFwd+7k6FvxB1QCJgH6m4dHGqQ+SKF/uVMM8m2XIwAwJUUJVE+g3f1OiBzuNqlJaHdy72Z/1EPq5SSIueyvU1+Roi2JAv2xTRxdd7HqpQ8skV/lqn7GEMZTcHBQHUF3AGxjDg+qzdXosuCyQdLKzPs9ZilzRISiPHIiw3aVyTPbcrRCux4+ExCwas3GxlKuxVcRLsG4t7wPVZ6VViP+UlqwZHLbL7xU68S/Kqy1llfbUG3edZvGs2mb829inMTjxB0w6wHH3PaDKhS7XJ5Taoc8mmrdG/BJnCCcj2JppDpyWVo3Bdpy31VeM=:rACvAXUA5HHI5yDNmCDsmmmHZPiiEf/aDN0zKTmbZow="
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
            "request-id": "1081752589096177482",
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

    token = "3:liY80ijxUCBy1Gi5QtGRKg==:qLsZ7YnNGzXV0fmM4Pax/wsmeO/ICpA5BSgzv1AnnrryKVWJN6d7rNDeEc3KDKgtRBvJwQibFE0CKuRnqq1FJCj4ME4/BpQHtx/HGedxdOe3RMTZHZosjjN3BI9ZkEztc3kJS4n50mXa/31t1nWJl0Gjv/6GdxwXhG8OJ4uX8bjksdQf8RobbNiRsJKQV2LRz5XKHRhTLKVPfPYUUq1uaMjTWPHRx8uHlig81ztWP9ji87Cdlm7mFCmxjwevjc7e+URRqQVk93rkJhcV1fA3Umh/9zjgddFfo9FVH94GymAUMBlihDOo8BxG5Skh58eyDSEeBdUO7kJlgbUROdCXvFXK4ruoglmE8s2U7E4gi42UD02gzxl+ecnRFao50gZKgcgMHzekuWrmT8AQ3hrBf1ZNHzzKQXwFTN//HPPjW+9mgeYlA/5S2NLggM2VkYZt+dwODKn5YzTEzyEbUbQYqXDSSX0TkQGcdkkyrq9XXaFT3Cfgk1Rb+azzSauI7z1cOHJPeIb1659UxthlsJrkm802j2CDc2sshfqzn0nT/Wk=:wvlVtOBLmfyLBikRG7aRwFxxPgrGhZ0ci1PnygMPX/g="
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
            "request-id": "1081752589096177482",
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
    print("Scraping Shaws")
    rows = []

    if isinstance(itemList, str):
        itemList = [itemList]

    headers = {
        "accept": "application/json, text/plain, */*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "ocp-apim-subscription-key": "5e790236c84e46338f4290aa1050cdd4",
    }

    token = "3:liY80ijxUCBy1Gi5QtGRKg==:qLsZ7YnNGzXV0fmM4Pax/wsmeO/ICpA5BSgzv1AnnrryKVWJN6d7rNDeEc3KDKgtRBvJwQibFE0CKuRnqq1FJCj4ME4/BpQHtx/HGedxdOe3RMTZHZosjjN3BI9ZkEztc3kJS4n50mXa/31t1nWJl0Gjv/6GdxwXhG8OJ4uX8bjksdQf8RobbNiRsJKQV2LRz5XKHRhTLKVPfPYUUq1uaMjTWPHRx8uHlig81ztWP9ji87Cdlm7mFCmxjwevjc7e+URRqQVk93rkJhcV1fA3Umh/9zjgddFfo9FVH94GymAUMBlihDOo8BxG5Skh58eyDSEeBdUO7kJlgbUROdCXvFXK4ruoglmE8s2U7E4gi42UD02gzxl+ecnRFao50gZKgcgMHzekuWrmT8AQ3hrBf1ZNHzzKQXwFTN//HPPjW+9mgeYlA/5S2NLggM2VkYZt+dwODKn5YzTEzyEbUbQYqXDSSX0TkQGcdkkyrq9XXaFT3Cfgk1Rb+azzSauI7z1cOHJPeIb1659UxthlsJrkm802j2CDc2sshfqzn0nT/Wk=:wvlVtOBLmfyLBikRG7aRwFxxPgrGhZ0ci1PnygMPX/g="
    cookies = {
        "reese84": token,

    }

    URL = "https://www.shaws.com/abs/pub/xapi/pgmsearch/v1/search/products"

    for itemName in itemList:
        print("Finding:", itemName)

        params = {
            "request-id": "6531752589803083615",
            "url": "https://www.shaws.com",
            "pageurl": "https://www.shaws.com",
            "pagename": "search",
            "rows": "30",
            "start": "0",
            "search-type": "keyword",
            "storeid": "2653",         
            "featured": "false",
            "q": itemName,
            "sort": "",
            "dvid": "web-4.1search",
            "channel": "instore",
            "visitorId": "54eb4cba-028b-4892-a38e-9310a2ca7d44",
            "pgm": "intg-search,merch-banner",
            "banner": "shaws"
        }

        try:
            response = requests.get(URL, headers=headers, cookies=cookies, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"Failed for {itemName}: {e}")
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
                    "store": "Shaws",
                    "URL": itemURL,
                    "productName": name
                })

            except Exception as e:
                print(f"Error parsing product JSON for '{itemName}': {e}")
                continue

    return pd.DataFrame(rows)

#print(shaws("Eggs",3))