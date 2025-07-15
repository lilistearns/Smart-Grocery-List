
import pandas as pd
import re
from bs4 import BeautifulSoup
import json
from requests.cookies import cookiejar_from_dict
from typing import Dict
import requests
from urllib.parse import urlencode
import urllib.parse
import random
import math


requestid = math.floor(1e13 * random.random())
cookied = [
    {
        "name": "OptanonConsent",
        "value": "consentId=6d7afd61-5570-4c1f-8587-0c453256e48c&datestamp=Mon+Jul+14+2025+12%3A08%3A55+GMT-0400+(Eastern+Daylight+Time)&version=202409.1.0&interactionCount=0&isAnonUser=1&isGpcEnabled=0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=https%3A%2F%2Fwww.starmarket.com%2Fshop%2Fsearch-results.html%3Fq%3Deggs%26tab%3Dproducts&groups=C0001%3A1%2CC0002%3A1%2CC0004%3A1%2CC0003%3A1",
        "domain": ".starmarket.com",
        "path": "/"
    },
    {
        "name": "__gads",
        "value": "ID=d6ed2b5da487c0b6:T=1752509336:RT=1752509336:S=ALNI_MaU7tcki1jLi7H8VV8L6-LyotN0zg",
        "domain": ".starmarket.com",
        "path": "/"
    },
    {
        "name": "__eoi",
        "value": "ID=61b52c08e344b289:T=1752509336:RT=1752509336:S=AA-Afjbqe17XoJt2HoyjQzLWcjNR",
        "domain": ".starmarket.com",
        "path": "/"
    }
]


headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "upgrade-insecure-requests": "1",
    "ocp-apim-subscription-key": "5e790236c84e46338f4290aa1050cdd4",
    "priority": "u=0, i",
    "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none"
}

params = {
    "request-id": requestid,
    "url": "https://www.starmarket.com",
    "pageurl": "https://www.starmarket.com",
    "pagename": "search",
    "rows": "30",
    "start": "0",
    "search-type": "keyword",
    "storeid": "2576",
    "featured": "true",
    "q": "eggs",
    "sort": "",
    "dvid": "web-4.1search",
    "channel": "instore",
    "visitorId": "2efdbc64-e6f8-4623-9fde-349bb9177ca4",
    "pgm": "intg-search,merch-banner",
    "banner": "starmarket"
}

def cookieGetter(storeURL,proxy):
    print("Made It Here")
    url = "http://localhost:8191/v1"
    headers = {"Content-Type": "application/json"}
    data = {
        "cmd": "request.get",
        "url": storeURL,
        "maxTimeout": 60000,
        "returnOnlyCookies": True,
        "proxy" : proxy
    }
    response = requests.post(url, headers=headers, json=data)
    print(response.status_code)
    return response.json()["solution"]["cookies"]

def cleanCookies(cookies):
    bad_flags = {"+browser_env_anomaly", "+non_human", "browser_env_anomaly", "non_human","bad_user_agents"}
    
    def clean_xdtags(xdtags_str):
        # Split tags by comma, strip whitespace
        tags = [tag.strip() for tag in xdtags_str.split(",")]
        cleaned = [tag for tag in tags if tag not in bad_flags]
        return ", ".join(cleaned)
    
    for cookie in cookies:
        # Handle both dictionary format and string format cookies
        if isinstance(cookie, dict):
            cookie_value = cookie.get('value', '')
        else:
            # For string format cookies, extract the value part
            if '=' in cookie:
                cookie_value = cookie.split('=', 1)[1]
            else:
                continue
        
        # Try to decode URL-encoded values
        try:
            decoded_value = urllib.parse.unquote(cookie_value)
            
            # Check if it's JSON-like data
            if decoded_value.startswith('{') and '"xDTags"' in decoded_value:
                try:
                    # Parse the JSON
                    json_data = json.loads(decoded_value)
                    
                    # Recursively clean xDTags in nested structures
                    def clean_json_recursive(obj):
                        if isinstance(obj, dict):
                            for key, value in obj.items():
                                if key == 'xDTags' and isinstance(value, str):
                                    obj[key] = clean_xdtags(value)
                                elif isinstance(value, (dict, list)):
                                    clean_json_recursive(value)
                        elif isinstance(obj, list):
                            for item in obj:
                                if isinstance(item, (dict, list)):
                                    clean_json_recursive(item)
                    
                    clean_json_recursive(json_data)
                    
                    # Convert back to JSON string and URL encode
                    cleaned_json = json.dumps(json_data, separators=(',', ':'))
                    cleaned_encoded = urllib.parse.quote(cleaned_json)
                    
                    # Update the cookie value
                    if isinstance(cookie, dict):
                        cookie['value'] = cleaned_encoded
                    else:
                        # For string format, replace the value part
                        cookie_parts = cookie.split('=', 1)
                        cookies[cookies.index(cookie)] = f"{cookie_parts[0]}={cleaned_encoded}"
                        
                except json.JSONDecodeError:
                    # If JSON parsing fails, try simple string replacement
                    if 'xDTags' in decoded_value:
                        # Use regex to find and clean xDTags values
                        pattern = r'"xDTags":"([^"]*)"'
                        def replace_xdtags(match):
                            xdtags_value = match.group(1)
                            cleaned_value = clean_xdtags(xdtags_value)
                            return f'"xDTags":"{cleaned_value}"'
                        
                        cleaned_decoded = re.sub(pattern, replace_xdtags, decoded_value)
                        cleaned_encoded = urllib.parse.quote(cleaned_decoded)
                        
                        if isinstance(cookie, dict):
                            cookie['value'] = cleaned_encoded
                        else:
                            cookie_parts = cookie.split('=', 1)
                            cookies[cookies.index(cookie)] = f"{cookie_parts[0]}={cleaned_encoded}"
        
        except Exception as e:
            # If any error occurs, skip this cookie
            continue
    
    return cookies


url = "https://www.starmarket.com/abs/pub/xapi/pgmsearch/v1/search/products"
full_url = url + "?" + urlencode(params)
print("Full Request URL:\n", full_url)


session = requests.Session()
proxy = "156.242.39.55:3129"
sproxy = "http://" + proxy
session.proxies = {
"http": sproxy,
"https": sproxy,
}



cookieList = cookieGetter("https://www.starmarket.com/shop/search-results.html?q=eggs&tab=products", proxy)
cookieList = cleanCookies(cookieList)
print(cookieList)

cookieList.extend(cookied)

cookieJar = {c["name"]: c["value"] for c in cookieList}


res = '\n'.join([f"{k}={v}" for k, v in cookieJar.items()])
with open("cookies.html", "w", encoding="utf-8") as f:
    f.write(res)

session.cookies.update(cookieJar)
#session.cookies = cookiejar_from_dict(cookieJar)
rep = session.get("https://httpbin.org/ip")
print(rep.text)


response = session.get(
    "https://www.starmarket.com/shop/search-results.html?q=eggs&tab=products",
    timeout=15
)

subscriptionKey = re.search('"apimProgramSubscriptionKey"\s*:\s*"([a-f0-9]{32})"', response.text)
response = requests.get(url, headers=headers, params=params, timeout=30)
with open("starmarket_response.html", "w", encoding="utf-8") as f:
            f.write(response.text)
print("Status:", response.status_code)

print(subscriptionKey)
    