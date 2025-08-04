import pandas as pd

from requests.cookies import cookiejar_from_dict
from typing import Dict
from urllib.parse import urlencode
from datetime import datetime
import sys
sys.path.append("./Data")
import webscrapingFunctions
import threading

##
# This for retrieving all data into one bulk training file
##

#For scraping all items into one library
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

#list of currently avaialble stores
stores = ["starmarket","shaws","hannaford"]

#creates callable function library
store_functions = {
    "starmarket": webscrapingFunctions.starmarket,
    "shaws": webscrapingFunctions.shaws,
    "hannaford": webscrapingFunctions.hannaford
}

results = {}

def run_scraper(store, func): results[store] = func(listOfItems, 150, False)

#begins multithreading through the function call library
threads = [
    threading.Thread(target=run_scraper, args=(s, store_functions[s]))
    for s in stores if s in store_functions
]

# starts and joins, then appends the data all into one file for training
[t.start() for t in threads]
[t.join() for t in threads]

for data in results.values():
    if data: webscrapingFunctions.appendData(data)

print("Complete!")
