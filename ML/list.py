from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
import numpy as np
import pandas as pd
from keras.models import load_model
import mysql.connector
import sys
from collections import defaultdict

tf.config.run_functions_eagerly(True)


def normalizer(data):
    data = data.copy()
    data["inv_price"] = 1 / data["price"]
    scaler = MinMaxScaler()
    data[["inv_price", "quantity", "quality"]] = scaler.fit_transform(data[["inv_price", "quantity", "quality"]])
    return data


def userPreferencesQuery(uid):
    connection = mysql.connector.connect(
        host="localhost",      
        user="comp5500",
        password="1qaz2wsx!QAZ@WSX",
        database="listBase"
    )

    if connection.is_connected():
        query = """
            SELECT qualPercent, pricePercent, quantPercent, shoppingSize, diet
            FROM userPreferences 
            WHERE uid = %s;
        """
        cursor = connection.cursor()
        cursor.execute(query, (uid,))
        row = cursor.fetchone()
        connection.close()

        if row:
            return {
                "qualPercent": row[0],
                "pricePercent": row[1],
                "quantPercent": row[2],
                "shoppingSize": row[3],
                "diet": row[4]
            }
    return None


def score_items(data, model, priceWeight, qualityWeight, quantityWeight):
    normalized = normalizer(data)
    total = priceWeight + qualityWeight + quantityWeight
    pw, qw, qtw = priceWeight / total, qualityWeight / total, quantityWeight / total

    input = normalized[["inv_price", "quantity", "quality"]].copy()
    input["inv_price"] *= pw
    input["quality"] *= qw
    input["quantity"] *= qtw

    scores = model.predict(input)
    data = data.copy()
    data["score"] = scores
    return data


def best_store_basket(data, model, user_prefs):
    # Score all items
    scored_data = score_items(
        data,
        model,
        priceWeight=user_prefs["pricePercent"],
        qualityWeight=user_prefs["qualPercent"],
        quantityWeight=user_prefs["quantPercent"]
    )

    # Group by item and store
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


# Example: Call via CLI or another script
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python multi_item_recommender.py <uid>")
        sys.exit()

    uid = sys.argv[1]
    model_path = f"models/model-{uid}.h5"

    try:
        model = load_model(model_path)
    except:
        print(f"Model for user {uid} not found at {model_path}")
        sys.exit()

    prefs = userPreferencesQuery(uid)
    if not prefs:
        print(f"No preferences found for user {uid}")
        sys.exit()

    # Simulated item list across multiple stores
    simulated_data = pd.DataFrame([
        {"item": "milk", "store": "Store A", "price": 2.99, "quantity": 1.0, "quality": 0.8},
        {"item": "milk", "store": "Store B", "price": 2.49, "quantity": 1.5, "quality": 0.9},
        {"item": "eggs", "store": "Store A", "price": 3.49, "quantity": 1.0, "quality": 0.85},
        {"item": "eggs", "store": "Store B", "price": 3.29, "quantity": 1.2, "quality": 0.88},
        {"item": "bread", "store": "Store A", "price": 1.99, "quantity": 1.0, "quality": 0.7},
        {"item": "bread", "store": "Store B", "price": 2.09, "quantity": 1.1, "quality": 0.75}
    ])

    best_list = best_store_basket(simulated_data, model, prefs)

    if not best_list.empty:
        print("Best shopping list from a single store:")
        print(best_list[["store", "item", "price", "quantity", "quality", "score"]])
    else:
        print("No single store contained all required items.")