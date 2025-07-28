from sklearn.preprocessing import MinMaxScaler
import mysql.connector
import tensorflow as tf
import numpy as np
import pandas as pd
import json
import os
import sys
import re
import sys
sys.path.append("./Data")
import dataFunctions
tf.config.run_functions_eagerly(True)

def getTrainingData(sdata):
    data = pd.DataFrame(sdata)
    data = dataFunctions.normalizer(data)
    X = data[["inv_price", "quantity", "quality"]].values
    y = np.array(data["rating"])
    return X, y


def loadUserData(uid):
    acceptedPath = f"./UserData/{uid}/Accepted/acceptedItems.json"
    rejectedPath = f"./UserData/{uid}/Rejected/rejectedItems.json"

    data = []

    if os.path.exists(acceptedPath):
        with open(acceptedPath, "r") as f:
            accepted = json.load(f)
            if isinstance(accepted, dict):
                accepted = [accepted]
            for item in accepted:
                item["rating"] = 1
                data.append(item)

    if os.path.exists(rejectedPath):
        with open(rejectedPath, "r") as f:
            rejected = json.load(f)
            if isinstance(rejected, dict):
                rejected = [rejected]
            for item in rejected:
                item["rating"] = 0
                data.append(item)

    return data


def modelMaker(uid):
    user_dir = f"/home/comp5500/git/Smart-Grocery-List/UserData/{uid}"
    os.makedirs(user_dir, exist_ok=True)

    modelPath = f"{user_dir}/model-{uid}.h5"
    prefs, listOfStores = dataFunctions.userQuery(uid)
    if not prefs:
        raise ValueError(f"No preferences found for UID {uid}")

    data = loadUserData(uid)

    if not data:
        print(f"No user feedback found for UID {uid}. Training minimal model using preferences.")
        x = np.array([[prefs["quantPercent"], prefs["qualPercent"], prefs["pricePercent"]]])
        y = np.array([(prefs["quantPercent"] + prefs["qualPercent"] + prefs["pricePercent"]) / 3])

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

    for item in data:
        item["pricePercent"] = prefs["pricePercent"]
        item["qualPercent"] = prefs["qualPercent"]
        item["quantPercent"] = prefs["quantPercent"]

    df = pd.DataFrame(data)
    df["quantity"] = df["quantity"].apply(dataFunctions.quantityNormalizer)
    df["quality"] = df.get("quality", 1)  
    df = dataFunctions.normalizer(df)

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
