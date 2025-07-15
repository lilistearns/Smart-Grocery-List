from sklearn.preprocessing import MinMaxScaler
import mysql.connector
import tensorflow as tf
import numpy as np
import pandas as pd
import json
import os
import sys

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

def modelMaker(uid):
    user_dir = f"/home/comp5500/git/Smart-Grocery-List/UserData/{uid}"
    os.makedirs(user_dir, exist_ok=True)

    jsonPath = f"{user_dir}/SampleData-{uid}.json"
    modelPath = f"{user_dir}/model-{uid}.h5"

    # Connect and get user preferences
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

    if not os.path.exists(jsonPath):
        print(f"No sample data found for UID {uid}. Training minimal model with only preference scores.")

        # Create dummy training data: One sample, rating = average of weights
        x = np.array([[pref["quantPercent"], pref["qualPercent"], pref["pricePercent"]]])
        y = np.array([(pref["quantPercent"] + pref["qualPercent"] + pref["pricePercent"]) / 3])

        model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(3,)),
            tf.keras.layers.Dense(8, activation="relu"),
            tf.keras.layers.Dense(1, activation="sigmoid")
        ])
        model.compile(optimizer='adam', loss=tf.keras.losses.MeanSquaredError())
        model.fit(x, y, epochs=100, verbose=1)

        model.save(modelPath)
        print(f"Minimal model trained and saved to {modelPath}")
        return

    
    # If sample data exists, do full training
    X, Y = dataRetrieval(jsonPath, uid)
    df = pd.DataFrame(X, columns=[
        "price", "quantity", "quality",
        "pricePercent", "qualPercent", "quantPercent"
    ])
    data = normalizer(df)
    X_norm = data[["inv_price", "quantity", "quality", "pricePercent", "qualPercent", "quantPercent"]].values

    if os.path.exists(modelPath):
        print(f"Model already exists for UID {uid}")
        model = tf.keras.models.load_model(modelPath)

        expected_input_shape = model.input_shape[-1]
        new_input_shape = X_norm.shape[1]

        if expected_input_shape != new_input_shape:
            print(f"Input shape changed from {expected_input_shape} to {new_input_shape}, retraining full model.")
            model = tf.keras.Sequential([
                tf.keras.layers.Input(shape=(new_input_shape,)),
                tf.keras.layers.Dense(16, activation="relu"),
                tf.keras.layers.Dense(1, activation="sigmoid")
            ])
        else:
            print("Updating existing model...")

    else:
        print(f"Creating full model for UID {uid}")
        model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(6,)),
            tf.keras.layers.Dense(16, activation="relu"),
            tf.keras.layers.Dense(1, activation="sigmoid")
        ])

    model.compile(optimizer='adam', loss=tf.keras.losses.MeanSquaredError())
    model.fit(X_norm, Y, epochs=100, verbose=1)
    model.save(modelPath)
    print(f"Full model saved to {modelPath}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: modelCreator.py <uid>")
    else:
        uid = sys.argv[1]
        modelMaker(uid)
        dbQuery()