import pandas as pd

from requests.cookies import cookiejar_from_dict
from typing import Dict
from urllib.parse import urlencode
from datetime import datetime
import sys
sys.path.append("./Data")
import webscrapingFunctions
import threading


#For scraping all items into individual files
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

store_functions = {
    "starmarket": webscrapingFunctions.starmarket,
    "shaws": webscrapingFunctions.shaws,
    "hannaford": webscrapingFunctions.hannaford
}
threads = []


for store in stores:
    if store in store_functions:
        thread = threading.Thread(target=store_functions[store], args=(listOfItems, 15,True,))  
        threads.append(thread)
        thread.start()


for thread in threads:
    thread.join()

print("Complete!")