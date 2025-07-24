from sklearn.preprocessing import MinMaxScaler
import mysql.connector
import tensorflow as tf
import numpy as np
import pandas as pd
import json
import os
import sys
import re
tf.config.run_functions_eagerly(True)

def normalizer(data):
    data = data.copy()
    data["inv_price"] = 1 / data["price"]
    to_scale = ["inv_price", "quantity", "quality", "pricePercent", "qualPercent", "quantPercent"]
    scaler = MinMaxScaler()
    data[to_scale] = scaler.fit_transform(data[to_scale])
    return data

def getTrainingData(sdata):
    data = pd.DataFrame(sdata)
    data = normalizer(data)
    X = data[["inv_price", "quantity", "quality"]].values
    y = np.array(data["rating"])
    return X, y

def dbQuery():
    connection = mysql.connector.connect(
        host="localhost",
        user="comp5500",
        password="1qaz2wsx!QAZ@WSX",
        database="listBase"
    )

    if connection.is_connected():
        print("Connection to DB successful")
    else:
        print("Connection to DB unsuccessful")

def dataRetrieval(jsonFile, uid):
    with open(jsonFile, "r") as f:
        data = json.load(f)

    conn = mysql.connector.connect(
        host="localhost",
        user="comp5500",
        password="1qaz2wsx!QAZ@WSX",
        database="listBase"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT qualPercent, pricePercent, quantPercent
        FROM userPreferences
        WHERE uid = %s
    """, (uid,))
    pref = cursor.fetchone()
    cursor.close()
    conn.close()

    if not pref:
        raise ValueError(f"No preferences found for uid: {uid}")

    X, Y = [], []
    for entry in data:
        features = [
            entry["price"],
            entry["quantity"],
            entry["quality"],
            pref["pricePercent"],
            pref["qualPercent"],
            pref["quantPercent"]
        ]
        X.append(features)
        Y.append(entry["rating"])

    return np.array(X), np.array(Y)

def loadUserLabeledData(uid):
    accepted_path = f"./UserData/{uid}/Accepted/acceptedItems.json"
    rejected_path = f"./UserData/{uid}/Rejected/rejectedItems.json"

    data = []

    if os.path.exists(accepted_path):
        with open(accepted_path, "r") as f:
            accepted = json.load(f)
            if isinstance(accepted, dict):
                accepted = [accepted]
            for item in accepted:
                item["rating"] = 1
                data.append(item)

    if os.path.exists(rejected_path):
        with open(rejected_path, "r") as f:
            rejected = json.load(f)
            if isinstance(rejected, dict):
                rejected = [rejected]
            for item in rejected:
                item["rating"] = 0
                data.append(item)

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

def modelMaker(uid):
    user_dir = f"/home/comp5500/git/Smart-Grocery-List/UserData/{uid}"
    os.makedirs(user_dir, exist_ok=True)

    modelPath = f"{user_dir}/model-{uid}.h5"

    conn = mysql.connector.connect(
        host="localhost",
        user="comp5500",
        password="1qaz2wsx!QAZ@WSX",
        database="listBase"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT qualPercent, pricePercent, quantPercent
        FROM userPreferences
        WHERE uid = %s
    """, (uid,))
    pref = cursor.fetchone()
    cursor.close()
    conn.close()

    if not pref:
        raise ValueError(f"No preferences found for UID {uid}")

    labeled_data = loadUserLabeledData(uid)

    if not labeled_data:
        print(f"No user feedback found for UID {uid}. Training minimal model using preferences.")
        x = np.array([[pref["quantPercent"], pref["qualPercent"], pref["pricePercent"]]])
        y = np.array([(pref["quantPercent"] + pref["qualPercent"] + pref["pricePercent"]) / 3])

        model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(3,)),
            tf.keras.layers.Dense(16, activation="relu"),
            tf.keras.layers.Dense(16, activation="relu"),
            tf.keras.layers.Dense(2, activation="sigmoid")
        ])
        model.compile(optimizer='adam', loss=tf.keras.losses.MeanSquaredError())
        model.fit(x, y, epochs=100, verbose=1)

        model.save(modelPath)
        print(f"Minimal model trained and saved to {modelPath}")
        return

    for item in labeled_data:
        item["pricePercent"] = pref["pricePercent"]
        item["qualPercent"] = pref["qualPercent"]
        item["quantPercent"] = pref["quantPercent"]

    df = pd.DataFrame(labeled_data)
    df["quantity"] = df["quantity"].apply(quantityNormalizer)
    df["quality"] = df.get("quality", 1)  

    df = normalizer(df)

    X = df[["inv_price", "quantity", "quality", "pricePercent", "qualPercent", "quantPercent"]].values
    Y = np.array(df["rating"])

    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(6,)),
        tf.keras.layers.Dense(16, activation="relu"),
        tf.keras.layers.Dense(1, activation="sigmoid")
    ])

    model.compile(optimizer='adam', loss=tf.keras.losses.MeanSquaredError())
    model.fit(X, Y, epochs=100, verbose=1)
    model.save(modelPath)
    print(f"Full model trained and saved to {modelPath}")
