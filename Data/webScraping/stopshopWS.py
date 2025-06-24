# DOESN'T WORK -------------- BOT DETECTION













from bs4 import BeautifulSoup
import urllib.request

# STOP & SHOP
keyWord = "eggs"
URL = "https://www.starmarket.com/shop/search-results.html?q=" + keyWord + "&tab=products"


print(URL)


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:113.0) Gecko/20100101 Firefox/113.0'
}

req = urllib.request.Request(URL, headers=headers)

try:
    with urllib.request.urlopen(req) as response:
        fullHTML = response.read().decode("utf8")
        print(fullHTML)
except Exception as e:
    print("Error:", e)
