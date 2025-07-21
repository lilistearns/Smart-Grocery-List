import os
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

warnings.filterwarnings('ignore')
warnings.filterwarnings('ignore', category=DeprecationWarning)
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
tf.get_logger().setLevel('ERROR')
tf.autograph.set_verbosity(0)
import absl.logging
absl.logging.set_verbosity(absl.logging.ERROR)
import numpy as np
import pandas as pd
from keras.models import load_model
import mysql.connector
import sys
import re
import json
sys.path.append("./Data/webScraping")
import webscraper
tf.config.run_functions_eagerly(True)

def normalizer(data):
    data = data.copy()
    data["inv_price"] = 1 / data["price"]
    scaler = MinMaxScaler()
    data[["inv_price", "quantity", "quality"]] = scaler.fit_transform(
        data[["inv_price", "quantity", "quality"]]
    )
    return data

def quantityNormalizer(data):
    data = str(data)
    match = re.search(r'(\d+(?:\.\d+)?)\s*(.+)', data)
    if not match:
        number = 1.0
        unit = data
    else:
        number = float(match.group(1))
        unit = match.group(2).strip().lower()

    
    if unit in ['gallon', 'gal', 'Gallon', 'Gal']:
        normalizedQuantity = number * 128
    elif unit in ['half gallon', 'half gal', 'Half Gallon', 'Half Gal']:
        normalizedQuantity = number * 64
    elif unit in ['quart', 'qt']:
        normalizedQuantity = number * 32
    elif unit in ['pint', 'pt']:
        normalizedQuantity = number * 16
    elif unit in ['liter', 'l']:
        normalizedQuantity = number * 33.814
    elif unit in ['ml', 'milliliter']:
        normalizedQuantity = number * 0.033814
    elif unit in ['fl oz', 'oz'] and 'fl' in data.lower():
        normalizedQuantity = number
    elif unit in ['lb', 'lbs', 'pound', 'pounds']:
        normalizedQuantity = number * 16
    elif unit in ['kg', 'kilogram', 'kilograms']:
        normalizedQuantity = number * 35.274
    elif unit in ['g', 'gram', 'grams']:
        normalizedQuantity = number * 0.035274
    elif unit in ['oz', 'ounce', 'ounces'] and 'fl' not in data.lower():
        normalizedQuantity = number
    elif unit in ['count', 'ct', 'pieces', 'pcs', 'each', 'ea', 'items', 'item']:
        normalizedQuantity = number
    elif unit in ['dozen', 'doz']:
        normalizedQuantity = number * 12
    elif unit in ['pair', 'pairs']:
        normalizedQuantity = number * 2

    elif unit in ['pack', 'pk', 'package', 'packages', 'box', 'boxes', 'bag', 'bags']:
        normalizedQuantity = number
    else:
        normalizedQuantity = number
    
    return float(normalizedQuantity)


def saveListRecommendation(list, uid):
    directory = f"./UserData/{uid}/"
    existing = [
        f for f in os.listdir(directory)
        if f.startswith(f"{uid}-list-") and f.endswith(".json")
    ]
    numbers = []
    for f in existing:
        try:
            num = int(f.split("-list-")[1].split(".json")[0])
            numbers.append(num)
        except ValueError:
            continue
    nextNum = max(numbers, default=0) + 1
    filename = f"{uid}-list-{nextNum}.json"
    filepath = os.path.join(directory, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(list, f, indent=2)

    print(f"Saved list to {filepath}")

def dbQuery():
    connection = mysql.connector.connect(
        host="localhost",
        user="comp5500",
        password="1qaz2wsx!QAZ@WSX",
        database="listBase"
    )
    if connection.is_connected():
        print("Connection to DB successful")
        connection.close()
        return True
    else:
        print("Connection to DB unsuccessful")
        return False


def userQuery(uid):
    connection = mysql.connector.connect(
        host="localhost",
        user="comp5500",
        password="1qaz2wsx!QAZ@WSX",
        database="listBase"
    )

    if connection.is_connected():
        print("Connection to DB successful")
        query = """
            SELECT qualPercent, pricePercent, quantPercent, shoppingSize, diet
            FROM userPreferences 
            WHERE uid = %s;
        """
        query2 = """
            SELECT store1ID, store2ID, store3ID, store4ID, store5ID
            FROM userStores
            WHERE uid = %s;
        """

        cursor = connection.cursor()
        cursor.execute(query, (uid,))
        row = cursor.fetchone()
        cursor.execute(query2, (uid,))
        stored = cursor.fetchall()
        print(stored)
        stores = [store for store in stored[0] if store]
        print(stores)

        format_strings = ','.join(['%s'] * len(stores))
        storeQuery = f"""
            SELECT storeName, storeAddress
            FROM storeInfo
            WHERE storeID IN ({format_strings});
        """
        cursor.execute(storeQuery, tuple(stores))
        storeInfo = cursor.fetchall()
        connection.close()
        return {
            "qualPercent": row[0],
            "pricePercent": row[1],
            "quantPercent": row[2],
            "shoppingSize": row[3],
            "diet": row[4]
        }, storeInfo


def recommender(data, model, pricePercent, qualityPercent, quantityPercent):
    normalizedData = normalizer(data)
    total = pricePercent + qualityPercent + quantityPercent
    pw, qw, qtw = pricePercent / total, qualityPercent / total, quantityPercent / total

    input = normalizedData[["inv_price", "quantity", "quality"]].copy()
    input["inv_price"] *= pw
    input["quality"] *= qw
    input["quantity"] *= qtw

    if model.input_shape[-1] == 6:
        input["pricePercent"] = pricePercent 
        input["qualPercent"] = qualityPercent 
        input["quantPercent"] = quantityPercent 

    data["score"] = model.predict(input)
    return data.sort_values("score", ascending=False)

def bestList(data, model, pricePercent, qualityPercent, quantityPercent, original_item_list):
    scored_data = recommender(
        data,
        model,
        pricePercent,
        qualityPercent,
        quantityPercent
    )
    baskets = []
    stores = scored_data["store"].unique()

    for store in stores:
        store_items = scored_data[scored_data["store"] == store]
        basket = []

        for item_name in original_item_list:
            match = store_items[
                store_items["item"].str.lower() == item_name.lower()
            ]
            if not match.empty:
                basket.append(match.iloc[0])

        if len(basket) == len(original_item_list):
            basket_df = pd.DataFrame(basket)
            avg_score = basket_df["score"].mean()
            baskets.append((avg_score, basket_df))

    baskets.sort(reverse=True, key=lambda x: x[0])
    return [basket_df for _, basket_df in baskets]

def parallelScrape(listOfStores, *args, exclude_stores=None, max_workers=None):
    exclude_stores = set(exclude_stores or [])
    dfs = []

    def scrape_wrapper(store_name):
        if store_name in exclude_stores:
            return pd.DataFrame()
        func = getattr(webscraper, store_name, None)
        if callable(func):
            try:
                df = func(*args)
                if isinstance(df, pd.DataFrame):
                    return df
            except Exception as e:
                print(f"[Error] {store_name}: {e}")
        return pd.DataFrame()

    with ThreadPoolExecutor(max_workers=max_workers or len(listOfStores)) as executor:
        futures = {
            executor.submit(scrape_wrapper, store[0]): store[0]
            for store in listOfStores
        }
        for future in as_completed(futures):
            result = future.result()
            if not result.empty:
                dfs.append(result)

    return dfs 

def itemRecommender(item, uid):
    model = load_model(f"UserData/{uid}/model-{uid}.h5")
    prefs, listOfStores = userQuery(uid)

    dfs = parallelScrape(listOfStores, item, 10,exclude_stores={"walmart"})

    originalData = pd.concat(dfs, ignore_index=True)
    data = originalData.copy()
    data['quantity'] = data['quantity'].apply(quantityNormalizer)

    recommendations = recommender(
        data,
        model,
        prefs["pricePercent"],
        prefs["qualPercent"],
        prefs["quantPercent"],
    )

    predicted = recommendations.head(10).index

    itemsR = list(
        originalData.loc[predicted, ["store", "price", "URL", "productName", "quantity"]]
        .itertuples(index=False, name=None)
    )

    return itemsR

def listRecommender(itemList, uid):
    model_path = f"UserData/{uid}/model-{uid}.h5"
    model = load_model(model_path)
    prefs, listOfStores = userQuery(uid)

    dfs = parallelScrape(listOfStores, itemList, 5, exclude_stores={"walmart"})

    if not dfs:
        return []

    originalData = pd.concat(dfs, ignore_index=True)
    data = originalData.copy()
    data['quantity'] = data['quantity'].apply(quantityNormalizer)

    baskets = bestList(
        data,
        model,
        prefs["pricePercent"],
        prefs["qualPercent"],
        prefs["quantPercent"],
        itemList
    )

    if not baskets:
        return []

    results = []

    for basket in baskets:
        merged = (
            pd.merge(
                basket[["store", "item"]],
                originalData,
                on=["store", "item"],
                how="left"
            )
            .drop_duplicates(subset=["item"])
        )

        item_set = list(
            merged[["store", "price", "URL", "productName", "quantity"]]
            .itertuples(index=False, name=None)
        )
        results.append(item_set)

    return results

#listItem = itemRecommender("Milk",3)
#print(listItem)
#saveListRecommendation(listItem,3)