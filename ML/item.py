import os
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
warnings.filterwarnings('ignore')
warnings.filterwarnings('ignore', category=DeprecationWarning)

import tensorflow as tf
tf.get_logger().setLevel('ERROR')
tf.autograph.set_verbosity(0)
import absl.logging
absl.logging.set_verbosity(absl.logging.ERROR)
import numpy as np
import pandas as pd
from keras.models import load_model
import mysql.connector
import sys
import re
import json
sys.path.append("./Data")
import dataFunctions
import webscrapingFunctions

tf.config.run_functions_eagerly(True)

def recommender(data, model, pricePercent, qualityPercent, quantityPercent):
    normalizedData = dataFunctions.normalizer(data)
    total = pricePercent + qualityPercent + quantityPercent
    pw, qw, qtw = pricePercent / total, qualityPercent / total, quantityPercent / total

    input = normalizedData[["inv_price", "quantity", "quality"]].copy()
    input["inv_price"] *= pw
    input["quality"] *= qw
    input["quantity"] *= qtw

    if model.input_shape[-1] == 6:
        input["pricePercent"] = pricePercent 
        input["qualPercent"] = qualityPercent 
        input["quantPercent"] = quantityPercent 

    data["score"] = model.predict(input)[:, 0]
    return data.sort_values("score", ascending=False)

def bestList(data, model, pricePercent, qualityPercent, quantityPercent, original_item_list):
    scored_data = recommender(
        data,
        model,
        pricePercent,
        qualityPercent,
        quantityPercent
    )
    baskets = []
    stores = scored_data["store"].unique()

    for store in stores:
        store_items = scored_data[scored_data["store"] == store]
        basket = []

        for item_name in original_item_list:
            match = store_items[
                store_items["item"].str.lower() == item_name.lower()
            ]
            if not match.empty:
                basket.append(match.iloc[0])

        if len(basket) == len(original_item_list):
            basket_df = pd.DataFrame(basket)
            avg_score = basket_df["score"].mean()
            baskets.append((avg_score, basket_df))

    baskets.sort(reverse=True, key=lambda x: x[0])
    return [basket_df for _, basket_df in baskets]

def parallelScrape(listOfStores, *args, excludedStores=None, maxWorkers=None):
    excludedStores = set(excludedStores or [])
    dfs = []

    def scraper(storeName):
        if storeName in excludedStores:
            return pd.DataFrame()
        func = getattr(webscrapingFunctions, storeName, None)
        if callable(func):
            try:
                df = pd.DataFrame(func(*args))
                if isinstance(df, pd.DataFrame):
                    return df
            except Exception as e:
                print(f"[Error] {storeName}: {e}")
        return pd.DataFrame()

    with ThreadPoolExecutor(max_workers=maxWorkers or len(listOfStores)) as executor:
        futures = {
            executor.submit(scraper, store[0]): store[0]
            for store in listOfStores
        }
        for future in as_completed(futures):
            result = future.result()
            if not result.empty:
                dfs.append(result)

    return dfs 

def itemRecommender(item, uid):
    model = load_model(f"UserData/{uid}/model-{uid}.h5", compile=False)
    prefs, listOfStores = dataFunctions.userQuery(uid)

    dfs = parallelScrape(listOfStores, item, 10, False, excludedStores={"walmart"})

    originalData = pd.concat(dfs, ignore_index=True)
    data = originalData.copy()
    data['quantity'] = data['quantity'].apply(dataFunctions.quantityNormalizer)

    recommendations = recommender(
        data,
        model,
        prefs["pricePercent"],
        prefs["qualPercent"],
        prefs["quantPercent"],
    )

    predicted = recommendations.head(10).index
    print(recommendations.head(10))
    itemsR = list(
        originalData.loc[predicted, ["store", "price", "URL", "productName", "quantity"]]
        .itertuples(index=False, name=None)
    )

    return itemsR

def listRecommender(itemList, uid):
    model = load_model(f"UserData/{uid}/model-{uid}.h5", compile=False)
    prefs, listOfStores = dataFunctions.userQuery(uid)

    dfs = parallelScrape(listOfStores, itemList, 5, False, excludedStores={"walmart"})

    if not dfs:
        return []

    originalData = pd.concat(dfs, ignore_index=True)
    data = originalData.copy()
    data['quantity'] = data['quantity'].apply(dataFunctions.quantityNormalizer)

    baskets = bestList(
        data,
        model,
        prefs["pricePercent"],
        prefs["qualPercent"],
        prefs["quantPercent"],
        itemList
    )

    if not baskets:
        return []

    results = []

    for basket in baskets:
        merged = (
            pd.merge(
                basket[["store", "item"]],
                originalData,
                on=["store", "item"],
                how="left"
            )
            .drop_duplicates(subset=["item"])
        )

        item_set = list(
            merged[["store", "price", "URL", "productName", "quantity"]]
            .itertuples(index=False, name=None)
        )
        results.append(item_set)
    return results