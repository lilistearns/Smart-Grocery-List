import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
from requests.cookies import cookiejar_from_dict
from typing import Dict
from urllib.parse import urlencode
import math
import random
from datetime import datetime
import os
import json
import threading

#Items used for prescraping
listOfItems = [
    "milk", "eggs", "bread", "butter", "cheese", "yogurt", "cream", "sour cream", "cottage cheese", "ice cream",
    "chicken breast", "ground beef", "pork chops", "bacon", "sausage", "ham", "turkey", "hot dogs", "deli meat", "rotisserie chicken",
    "salmon", "tuna", "shrimp", "cod", "tilapia", "crab", "lobster", "sardines", "anchovies", "fish sticks",
    "apples", "bananas", "oranges", "grapes", "strawberries", "blueberries", "raspberries", "blackberries", "peaches", "pineapple",
    "mangoes", "kiwis", "watermelon", "cantaloupe", "honeydew", "lemons", "limes", "avocados", "plums", "cherries",
    "carrots", "potatoes", "sweet potatoes", "onions", "garlic", "lettuce", "spinach", "kale", "broccoli", "cauliflower",
    "green beans", "peas", "corn", "zucchini", "cucumbers", "tomatoes", "bell peppers", "jalapeños", "mushrooms", "celery",
    "cabbage", "brussels sprouts", "asparagus", "eggplant", "radishes", "beets", "turnips", "squash", "artichokes", "leeks",
    "rice", "pasta", "spaghetti", "macaroni", "noodles", "quinoa", "couscous", "flour", "sugar", "brown sugar",
    "baking powder", "baking soda", "salt", "pepper", "cinnamon", "nutmeg", "vanilla extract", "honey", "maple syrup", "olive oil",
    "vegetable oil", "canola oil", "peanut butter", "jelly", "jam", "mayonnaise", "ketchup", "mustard", "soy sauce", "hot sauce",
    "vinegar", "salad dressing", "barbecue sauce", "tomato sauce", "canned tomatoes", "canned beans", "black beans", "chickpeas",
    "soup", "chicken broth", "beef broth", "vegetable broth", "cereal", "oatmeal", "granola", "crackers", "chips", "pretzels",
    "popcorn", "cookies", "candy", "chocolate", "cake mix", "brownie mix", "pancake mix", "syrup", "tea", "coffee",
    "soda", "juice", "bottled water", "sports drinks", "energy drinks", "beer", "wine", "frozen vegetables", "frozen fruit", "frozen pizza",
    "frozen meals", "frozen burritos", "frozen waffles", "frozen fries", "ice", "toilet paper", "paper towels", "tissues", "napkins", "aluminum foil"
]

stores = ["starmarket","shaws","hannaford"]
fileLock = {item: threading.Lock() for item in listOfItems}
dateString = datetime.now().strftime("%Y-%m-%d")
baseName = "scrapedData"



#retrieves cookies, obsolete
def cookieGetter(storeURL):
    print("Made It Here")
    url = "http://0.0.0.0:8191/v1"
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

#loads cookies into session, obsolete
def loadCookies(session: requests.Session, cookiesDict: Dict):
    cookie = {}
    for elem in cookiesDict:
        cookie[elem["name"]] = elem["value"]
    session.cookies = cookiejar_from_dict(cookie)
    return session

#appends an item to the name to the json file for itemName-{date}.json (This is for daily retrievals and longterm product information storage)
def appendItem(data, itemName):
    if not data:
        return
    
    itemName = re.sub(r'[^\w\s-]', '', itemName).strip()
    i = re.sub(r'[-\s]+', '_', itemName)
    filePath =  f"Data/scrapingLibrary/{dateString}/{itemName}_{dateString}.json"
    
    with fileLock[itemName]:
        os.makedirs(os.path.dirname(filePath), exist_ok=True)
        
        if os.path.exists(filePath):
            with open(filePath, "r", encoding="utf-8") as f:
                try:
                    existingData = json.load(f)
                except json.JSONDecodeError:
                    existingData = []
        else:
            existingData = []
        
        existingData.extend(data)
        
        with open(filePath, "w", encoding="utf-8") as f:
            json.dump(existingData, f, indent=2, ensure_ascii=False)


#dumps all data into one file, this is for training all models
def appendData(data):

    outputName = f"Data/scrapingLibrary/{baseName}_{dateString}.json"
    if os.path.exists(outputName):
        with open(outputName, "r", encoding="utf-8") as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []
    
    existing_data.extend(data)
    
    with open(outputName, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, indent=2, ensure_ascii=False)

#looks for the itemName as a path, this will return if it was already retrieved and stored before webscraping.
def tryPrescraped(itemName):
    itemName = re.sub(r'[^\w\s-]', '', itemName).strip()
    i = re.sub(r'[-\s]+', '_', itemName)
    filePath =  f"Data/scrapingLibrary/{dateString}/{itemName}_{dateString}.json"
    if os.path.exists(filePath):
        try:
            return pd.read_json(filePath)
        except Exception as e:
            print(f"Error loading cached file for {itemName}: {e}")
            return None

#Webscrapes for item information on shaws/starmarket works the exact same most documentation and code is shared.
def shaws(itemList, num, isCache):
    rows = []
    print("Scraping Shaw's")
    if isinstance(itemList, str):
        itemList = [itemList]

    #necessary headers
    headers = {
        "accept": "application/json, text/plain, */*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "ocp-apim-subscription-key": "5e790236c84e46338f4290aa1050cdd4",
    }

    #retrieves constantly retrieved cookies
    with open("/mnt/hgfs/Cookies/request-ids.json", "r") as f:
        tokens = json.load(f)
    values = tokens.get("shaws", {})
    requestID = values.get("requestId", "")
    token = values.get("cookie", "")
    cookies = {
        "reese84": token
    }
    #begins session for retrieval
    session = requests.Session()
    URL = "https://www.shaws.com/abs/pub/xapi/pgmsearch/v1/search/products"

    #For each item in the list it will create a new request using the parameters, and with the cookies and headers generate a fulfillable request, then it is all parsed out and returned
    for itemName in itemList:
        if isCache:
            rows = []
        else:
            prescrapedData = tryPrescraped(itemName.lower()) 
            if prescrapedData is not None: 
                rows.extend(prescrapedData.to_dict(orient="records")[:num])
                print("Found in Library")
                continue
        print("Finding:", itemName)
        params = {
            "request-id": requestID,
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


        #Begins parsing out each product and returns important information
        docs = data.get("primaryProducts", {}).get("response", {}).get("docs", [])
        print(f"Found {len(docs)} products for {itemName}")
        if(len(docs)==0):
            with open("failed.txt","w") as f:
                f.write(str(data))
            break
        for product in docs[:num]:
            try:
                name = product.get("name", "")
                price = float(product.get("price", 0.0))
                unitQuantity = product.get("unitQuantity", "1")
                unitMeasure = product.get("unitOfMeasure", "ea")
                quantityUnits = f"{unitQuantity} {unitMeasure}"

                review = product.get("productReview", {})
                rating = float(review.get("avgRating", 0.0))
                quality = rating / 5.0 if rating else 0.75

                itemURL = f"https://www.shaws.com/shop/product-details.{product.get('pid')}.html"

                rows.append({
                    "item": itemName,
                    "price": price,
                    "quantity": quantityUnits,
                    "quality": quality,
                    "store": "Shaw's",
                    "URL": itemURL,
                    "productName": name
                })

            except Exception as e:
                print(f"Error parsing product JSON for '{itemName}': {e}")
                continue
        if isCache:
            appendItem(rows, itemName)
    return rows


def starmarket(itemList, num, isCache):
    print("Scraping Star Market")
    rows = []
    if isinstance(itemList, str):
        itemList = [itemList]

    headers = {
        "accept": "application/json, text/plain, */*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "ocp-apim-subscription-key": "5e790236c84e46338f4290aa1050cdd4",
    }
    with open("/mnt/hgfs/Cookies/request-ids.json", "r") as f:
        tokens = json.load(f)
    values = tokens.get("starmarket", {})
    requestID = values.get("requestId", "")
    token = values.get("cookie", "")
    cookies = {
        "reese84": token
    }

    session = requests.Session()
    URL = "https://www.starmarket.com/abs/pub/xapi/pgmsearch/v1/search/products"

    for itemName in itemList:
        if isCache:
            rows = []
        else:
            prescrapedData = tryPrescraped(itemName.lower()) 
            if prescrapedData is not None: 
                rows.extend(prescrapedData.to_dict(orient="records")[:num])
                print("Found in Library")
                continue
        print("Finding:", itemName)
        params = {
            "request-id": requestID,
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
                unitQuantity = product.get("unitQuantity", "1")
                unitMeasure = product.get("unitOfMeasure", "ea")
                quantityUnits = f"{unitQuantity} {unitMeasure}"

                review = product.get("productReview", {})
                rating = float(review.get("avgRating", 0.0))
                quality = rating / 5.0 if rating else 0.75

                itemURL = f"https://www.starmarket.com/shop/product-details.{product.get('pid')}.html"

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
        if isCache:
            appendItem(rows, itemName)

    return rows

#webscrapes for walmart by calling an external API, scraperAI walmart is too big of a task to crack and would take up too much time in project
def walmart(itemList, num, isCache):
    print("Scraping Walmart")
    rows = []
    if isinstance(itemList, str):
        itemList = [itemList]
    
    for itemName in itemList:
        if isCache:
            rows = []
        else:
            prescrapedData = tryPrescraped(itemName.lower()) 
            if prescrapedData is not None: 
                rows.extend(prescrapedData.to_dict(orient="records")[:num])
                print("Found in Library")
                continue
        payload = {
            'api_key': '852615c755f41faf2cc763b2f8c8a54a',
            'query': itemName,
            'tld': 'com'
        }
        r = requests.get('https://api.scraperapi.com/structured/walmart/search', params=payload)
        data = json.loads(r.text)
        
        with open("walmarttest.json", "w", encoding="utf-8") as f:
            f.write(r.text)
        
        itemAdded = 0
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
            itemAdded += 1
            if itemAdded >= num:
                break
        if isCache:
            appendItem(rows,itemName)

    return rows

#Uses requests to request full html page and fromt there it is parsed by BS4
def hannaford(itemList, num, isCache):
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
        if isCache:
            rows =[]
        else:
            prescrapedData = tryPrescraped(itemName.lower()) 
            if prescrapedData is not None: 
                rows.extend(prescrapedData.to_dict(orient="records")[:num])
                print("Found in Library")
                continue
        URL = f"https://www.hannaford.com/search/product?form_state=searchForm&keyword={itemName}&ieDummyTextField=&productTypeId=P"
        response = requests.get(URL, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        products = soup.find_all("div", class_="plp_thumb_wrap product-impressions")
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
        if isCache:
            appendItem(rows,itemName)


    return rows