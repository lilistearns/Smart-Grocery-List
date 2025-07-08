from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
import numpy as np
import pandas as pd
from keras.models import load_model
import mysql.connector
import sys
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

    expected_input_shape = model.input_shape[-1]

    if expected_input_shape == 6:
        input["pricePercent"] = pricePercent / 100
        input["qualPercent"] = qualityPercent / 100
        input["quantPercent"] = quantityPercent / 100

    data["score"] = model.predict(input)
    return data.sort_values("score", ascending=False).head(3)

def bestList(itemList, uid):
    model_path = f"UserData/{uid}/model-{uid}.h5"
    model = load_model(model_path)
    prefs, listOfStores = userQuery(uid)

    dfs = []
    for store in listOfStores:
        func = getattr(webscraper, store[0], None)
        if callable(func):
            storeDF = func(itemList,5)
            if isinstance(storeDF, pd.DataFrame):
                dfs.append(storeDF)

    if not dfs:
        return pd.DataFrame()  

    data = pd.concat(dfs, ignore_index=True)

    scored_data = recommender(
        data,
        model,
        pricePercent=prefs["pricePercent"],
        qualityPercent=prefs["qualPercent"],
        quantityPercent=prefs["quantPercent"]
    )

    stores = scored_data["store"].unique()
    items = scored_data["item"].unique()
    baskets = []

    for store in stores:
        store_items = scored_data[scored_data["store"] == store]
        basket = []
        for item in items:
            match = store_items[store_items["item"] == item]
            if not match.empty:
                basket.append(match.iloc[0])
        if len(basket) == len(items):
            basket_df = pd.DataFrame(basket)
            avg_score = basket_df["score"].mean()
            baskets.append((avg_score, basket_df))

    baskets.sort(reverse=True, key=lambda x: x[0])
    return baskets[0][1] if baskets else pd.DataFrame()


def itemRecommender(item,uid):
    model = load_model(f"UserData/{uid}/model-{uid}.h5")
    prefs, listOfStores = userQuery(uid)
    dfs =[]
    for store in listOfStores:
        func = getattr(webscraper, store[0], None)
        storeDF = func(item,10)
        dfs.append(storeDF)
    data = pd.concat(dfs,ignore_index=True)
    #data["z_qty"] = zscore(data["quantity"])
    #data = data[data["z_qty"].abs() <= 2.5]
    #data.drop(columns=["z_qty"], inplace=True)
    print(data)
    recommendations = recommender(
        data,
        model,
        prefs["pricePercent"],
        prefs["qualPercent"],
        prefs["quantPercent"],
    )
    itemsR = list(
        recommendations[["store", "price", "URL"]]
        .head(3)
        .itertuples(index=False, name=None)
    )

    return itemsR

def listRecommender(itemList, uid):
    recommendations = bestList(itemList, uid)
    listR = list(
        recommendations[["store", "price", "URL"]]
        .itertuples(index=False, name=None)
    )

    return listR
    


print(listRecommender("Milk",3))