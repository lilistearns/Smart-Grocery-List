
# DOESN'T WORK -------------- HIDDEN ITEMS









from bs4 import BeautifulSoup
import urllib.request

def starMarket(keyword):
    URL = "https://www.starmarket.com/shop/search-results.html?q=" + keyword + "&tab=products"
    print(URL)
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:113.0) Gecko/20100101 Firefox/113.0'
    }

    req = urllib.request.Request(URL, headers=headers)

    try:
        with urllib.request.urlopen(req) as response:
            fullHTML = response.read().decode("utf8")
            htmlPage = BeautifulSoup(fullHTML, 'html.parser')
            for script in htmlPage.find_all("script"):
                script.decompose()
            with open("output.txt", "w") as file:
                file.write(htmlPage)
            items = htmlPage.find_all(class_="pc-grid-prdItem")
            print(items)

    except Exception as e:
        print("Error:", e)


# STAR MARKET
keyword = "eggs"
store = "Star Market"

match(store):
    case "Star Market":
        starMarket(keyword)


