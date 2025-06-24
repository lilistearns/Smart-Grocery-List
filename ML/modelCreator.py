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
    data["inv_price"] = 1 / data["price"] # price needs to be lower thus inverse
    scaler = MinMaxScaler()
    data[["inv_price", "quantity", "quality"]] = scaler.fit_transform(
        data[["inv_price", "quantity", "quality"]]
    )
    return data

def getTrainingData(sdata):

    data = pd.DataFrame(sdata)
    data= normalizer(data)
    X = data[["inv_price", "quantity", "quality"]].values
    y = np.array(data["rating"])
    return X, y

def dbQuery():
    connection = mysql.connector.connect(
        host="localhost",      # or your DB server
        user="comp5500",
        password="1qaz2wsx!QAZ@WSX",
        database="listBase"
    )

    if(connection.is_connected()):
        print("Connection to DB successful")
    else:
        print("Connection to DB unsuccessful")

def dataRetrieval(jsonFile):
    with open(jsonFile, "r") as f:
        data = json.load(f)

    X, Y = [], []
    for entry in data:
        try:
            features = [entry["price"], entry["quantity"], entry["quality"]]
            X.append(features)
            Y.append(entry["rating"])
        except KeyError as e:
            print(f"Missing key in entry: {e}")

    return np.array(X), np.array(Y)

def modelMaker(uid):
    jsonPath = f"../UserJson/SampleData-{uid}.json"
    if not os.path.exists(jsonPath):
        print(f"Data file not found: {jsonPath}")
        return

    X, Y = dataRetrieval(jsonPath)
    modelPath = f"models/model-{uid}.h5"

    # If model exists, load and update it
    if os.path.exists(modelPath):
        print(f"Updating existing model for UID {uid}")
        model = tf.keras.models.load_model(modelPath)
        model.compile(optimizer='adam', loss=tf.keras.losses.MeanSquaredError())
        model.fit(X, Y, epochs=50, verbose=1)
    else:
        print(f"Creating new model for UID {uid}")
        model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(3,)),
            tf.keras.layers.Dense(8, activation="relu"),
            tf.keras.layers.Dense(1, activation="sigmoid")
        ])
        model.compile(optimizer='adam', loss=tf.keras.losses.MeanSquaredError())
        model.fit(X, Y, epochs=100, verbose=1)

    model.save(modelPath)
    print(f"Model saved to {modelPath}")

# to be removed, this just simulates uid
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: modelCreator.py <uid>")
    else:
        uid = sys.argv[1]
        modelMaker(uid)
        dbQuery()

