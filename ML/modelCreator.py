from sklearn.preprocessing import MinMaxScaler
import mysql.connector
import tensorflow as tf
import numpy as np
import pandas as pd
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
        #df = pd.read_sql(f"""
        #    SELECT store, price, quantity, quality 
        #    FROM items 
        #    WHERE uid = %s AND item_name = %s
        #""", conn, params=(uid, item_name))
        conn.close()
    else:
        print("Connection to DB unsuccessful")


def modelMaker(uid):
    
    # v will be webscraped later
    sdata = {
        "price": [2.99, 2.49, 3.49, 3.29],
        "quantity": [1.0, 1.5, 1.0, 1.2],
        "quality": [0.8, 0.9, 0.85, 0.88],
        "rating": [0.6, 0.9, 0.5, 0.7]  # ^ simulated user and data
    }

    X, Y = getTrainingData(sdata)
    modelPath = f"models/model-{uid}.h5"

    # If model exists, load and continue training
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

