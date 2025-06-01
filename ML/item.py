from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
import numpy as np
import pandas as pd
from keras.models import load_model
import sys
import mysql.connector
tf.config.run_functions_eagerly(True)


# Simulated data for testing
sdata = {
    "item": ["milk", "milk", "eggs", "eggs"],
    "store": ["Store A", "Store B", "Store A", "Store B"],
    "price": [2.99, 2.49, 3.49, 3.29],       # Lower is better
    "quantity": [1.0, 1.5, 1.0, 1.2],         
    "quality": [0.8, 0.9, 0.85, 0.88],        
}

data = pd.DataFrame(sdata)
def normalizer(data):
    data = data.copy()
    data["inv_price"] = 1 / data["price"]
    scaler = MinMaxScaler()
    data[["inv_price", "quantity", "quality"]] = scaler.fit_transform(data[["inv_price", "quantity", "quality"]])
    return data


# to be removed, this just simulates uid
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python modelCreator.py <uid>")
    else:
        uid = sys.argv[1]


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
        connection.close()
    else:
        print("Connection to DB unsuccessful")


#query databse for model saved by modelCreator based on uid "model-$uid.h5"
#uid = (sys.argv[2])
modelTitle = 'model-' + uid + '.h5'
model = load_model(f"models/{modelTitle}")


def recommender(data, model, priceWeight, quality_weight, quantity_weight, top):
    normalizedData = normalizer(data)
    #normalizes data based off of user preferenece
    total = priceWeight + quality_weight + quantity_weight
    pw, qw, qtw = priceWeight / total, quality_weight / total, quantity_weight / total

    # takes weights into account and adjusts data accordingly
    input = normalizedData[["inv_price", "quantity", "quality"]].copy()
    input["inv_price"] *= pw
    input["quality"] *= qw
    input["quantity"] *= qtw

    # main prediction based off of models
    data["score"] = model.predict(input)
    
    # sort, return top (3)
    return data.sort_values("score", ascending=False).head(top)


recommendations = recommender(
    data,
    model,
    priceWeight=60,
    quality_weight=30,
    quantity_weight=10,
    top=3
)


print(recommendations[["store", "price", "quantity", "quality", "score"]])
dbQuery()