import json
import pandas as pd
import numpy as np
import os
import re
import sys
sys.path.append("./Data")
import dataFunctions
from datetime import datetime


dateString = datetime.now().strftime("%Y-%m-%d")

preferences = ['quality', 'price', 'quantity', 'balanced', 'premium', 'budget', 'bulk']

ratingParams = {
    'quality':  ((8.5, 1.5), (6.0, 2.0), (6.5, 1.8)),
    'price':    ((6.5, 2.0), (8.5, 1.2), (6.0, 1.8)),
    'quantity': ((6.0, 2.0), (6.5, 1.8), (8.5, 1.3)),
    'balanced': ((7.0, 1.8), (7.0, 1.8), (7.0, 1.8)),
    'premium':  ((9.2, 0.8), (5.0, 2.5), (5.5, 2.0)),
    'budget':   ((5.5, 2.2), (9.0, 1.0), (7.0, 1.8)),
    'bulk':     ((5.0, 2.0), (7.5, 1.5), (9.0, 1.0)),
}

def loadData(dataPath):
    with open(dataPath, 'r') as f:
        raw = json.load(f)
    df = pd.DataFrame(raw)
    df['normalizedQuantity'] = df['quantity'].apply(dataFunctions.quantityNormalizer)
    df['pricePerUnit'] = df['price'] / df['normalizedQuantity']
    df['qualityPerDollar'] = df['quality'] / df['price']
    df['quantityPerDollar'] = df['normalizedQuantity'] / df['price']
    df['qualityPct'] = df['quality'].rank(pct=True)
    df['pricePct'] = 1 - df['price'].rank(pct=True)
    df['quantityPct'] = df['normalizedQuantity'].rank(pct=True)
    df['valuePct'] = df['qualityPerDollar'].rank(pct=True)
    return df

def filter(df, preference):
    if preference == 'quality':
        range = (df['qualityPct'] >= 0.7) & (df['pricePct'] >= 0.2)
    elif preference == 'price':
        range = (df['pricePct'] >= 0.6) | (df['valuePct'] >= 0.5)
    elif preference == 'quantity':
        range = (df['quantityPct'] >= 0.6) | (df['quantityPerDollar'] >= df['quantityPerDollar'].quantile(0.6))
    elif preference == 'balanced':
        score = df['qualityPct'] * 0.4 + df['pricePct'] * 0.3 + df['quantityPct'] * 0.3
        range = score >= score.quantile(0.4)
    elif preference == 'premium':
        range = df['qualityPct'] >= 0.85
    elif preference == 'budget':
        range = (df['pricePct'] >= 0.7) | (df['valuePct'] >= 0.7)
    elif preference == 'bulk':
        range = (df['quantityPct'] >= 0.8) | (df['pricePerUnit'] <= df['pricePerUnit'].quantile(0.3))

    qParams, pParams, qtParams = ratingParams[preference]
    ratingData = df[range].copy()
    ratingData['qualityRating'] = np.clip(np.random.normal(*qParams, len(ratingData)), 1, 10).round().astype(int)
    ratingData['priceRating'] = np.clip(np.random.normal(*pParams, len(ratingData)), 1, 10).round().astype(int)
    ratingData['quantityRating'] = np.clip(np.random.normal(*qtParams, len(ratingData)), 1, 10).round().astype(int)
    return ratingData

def saveFiltered(df, outputDir="Data/filtered/"):
    os.makedirs(outputDir, exist_ok=True)


    for pref in preferences:
        print(f"Filtering for {pref}")
        filtered = filter(df, pref)
        records = []
        for _, row in filtered.iterrows():
            records.append({
                "item": row.get("item", ""),
                "price": row["price"],
                "quantity": row["quantity"],
                "quality": row["quality"],
                "store": row["store"],
                "URL": row.get("URL", ""),
                "productName": row["productName"],
                "ratings": {
                    "quality": row["qualityRating"],
                    "price": row["priceRating"],
                    "quantity": row["quantityRating"]
                },
                "decision": "accept"
            })

        outPath = os.path.join(outputDir, f"{pref}TrainingData.json")
        with open(outPath, 'w') as f:
            json.dump(records, f, indent=2)


if __name__ == "__main__":
    saveFiltered(loadData(f"./Data/scrapingLibrary/scrapedData_{dateString}.json"))