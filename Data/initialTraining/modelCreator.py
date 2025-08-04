import json
import os
import tensorflow as tf
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import re
import sys
sys.path.append("./Data")
import dataFunctions


prefs = [
    'quality', 'price', 'quantity', 'balanced', 'premium', 'budget', 'bulk'
]

#static preference Weights for sorting
preferenceWeights = {
    'quality':  (0.4, 0.3, 0.3),
    'price':    (0.3, 0.4, 0.3),
    'quantity': (0.3, 0.3, 0.4),
    'balanced': (0.33, 0.33, 0.33),
    'premium':  (0.5, 0.25, 0.25),
    'budget':   (0.25, 0.5, 0.25),
    'bulk':     (0.25, 0.3, 0.45)
}


#ranks the entire set of data by quality, price, and quantity. Then it gets a static range premade by development team, uses that range as a filter of what to copy over for training. Returns the twice filtered data.
def filterDataByPreference(df, preference):
    df['qualityPct'] = df['quality'].rank(pct=True)
    df['pricePct'] = (1 - df['price'].rank(pct=True))  
    df['quantityPct'] = df['quantity'].rank(pct=True)
    df['valuePct'] = (df['quality'] / df['price']).rank(pct=True)
    df['pricePerUnit'] = df['price'] / df['quantity']

    if preference == 'quality':
        mask = (df['qualityPct'] >= 0.7) & (df['pricePct'] >= 0.2)
    elif preference == 'price':
        mask = (df['pricePct'] >= 0.6) | (df['valuePct'] >= 0.5)
    elif preference == 'quantity':
        mask = (df['quantityPct'] >= 0.6) | (df['quantity'] / df['price'] >= (df['quantity'] / df['price']).quantile(0.6))
    elif preference == 'balanced':
        score = df['qualityPct'] * 0.4 + df['pricePct'] * 0.3 + df['quantityPct'] * 0.3
        mask = score >= score.quantile(0.4)
    elif preference == 'premium':
        mask = df['qualityPct'] >= 0.85
    elif preference == 'budget':
        mask = (df['pricePct'] >= 0.7) | (df['valuePct'] >= 0.7)
    elif preference == 'bulk':
        mask = (df['quantityPct'] >= 0.8) | (df['pricePerUnit'] <= df['pricePerUnit'].quantile(0.3))
    else:
        mask = pd.Series([True] * len(df)) 

    return df[mask].copy()

#main trainer, for each prefernece it will go through the filtered item file and train based off of those items and their ratings. Uses static weights to find better weights and biases in the model, helps focus on the important preferences.
def trainModel(data, preference):
    #gets all the training data and normalizes
    weights = preferenceWeights.get(preference)
    for item in data:
        item["quantity"] = dataFunctions.quantityNormalizer(item["quantity"])
        item["quality"] = float(item.get("quality", 1))

    df = pd.DataFrame(data)
    df = dataFunctions.normalizer(df)

    filtered = filterDataByPreference(df, preference)

    if filtered.empty:
        return

    qualityWeight, priceWeight, qualityWeight = weights

    filtered["rating"] = (
        filtered["quality"] * qualityWeight +
        filtered["inv_price"] * priceWeight +
        filtered["quantity"] * qualityWeight
    )

    #sets inputs
    X = filtered[["inv_price", "quantity", "quality"]].values
    y = filtered["rating"].values

    #sets model layers 32 relu for actual training, final sigmoid for 0-1 output
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(3,)),
        tf.keras.layers.Dense(16, activation="relu"),
        tf.keras.layers.Dense(16, activation="relu"),
        tf.keras.layers.Dense(1, activation="sigmoid")
    ])

    #compiles and trains
    model.compile(optimizer='adam', loss='mse')
    model.fit(X, y, epochs=100, verbose=1)

    modelDirectory = "./TrainedModels"
    os.makedirs(modelDirectory, exist_ok=True)
    model.save(os.path.join(modelDirectory, f"{preference}.h5"))
    print(f"Model for '{preference}' saved to {os.path.join(modelDirectory, f'{preference}.h5')}")

#main function starts up the trainer for all preferences
def main():
    for pref in prefs:
        fileName = f"./Data/filtered/{pref}TrainingData.json"  
        if not os.path.exists(fileName):
            print(f"Data file {fileName} not found, scrape then filter")
            return
        with open(fileName, "r") as f:
            data = json.load(f)
        print(f"\nTraining model for preference: {pref}")
        trainModel(data, pref)


if __name__ == "__main__":
    main()
