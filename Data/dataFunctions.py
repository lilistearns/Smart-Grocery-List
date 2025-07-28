import re
from sklearn.preprocessing import MinMaxScaler
import mysql
import mysql.connector

#references:
#   item.py.userQuery
#   modelTrainer.py.
def dbConnect():
    connection = mysql.connector.connect(
        host="localhost",
        user="comp5500",
        password="1qaz2wsx!QAZ@WSX",
        database="listBase"
    )
    if connection.is_connected():
        print("Connection to DB successful")
        return connection
    else:
        return None


#references:
#   item.py.recommender
#   modelTrainer.py.getTrainingData
#   modelTrainer.py.modelMaker
def normalizer(data):
    data = data.copy()
    data["inv_price"] = 1 / data["price"]
    scaler = MinMaxScaler()
    data[["inv_price", "quantity", "quality"]] = scaler.fit_transform(
        data[["inv_price", "quantity", "quality"]]
    )
    return data

#references:
#   item.py.itemRecommender
#   item.py.listRecommender
#   dataFilterer.py.self
#   modelTrainer.py.modelMaker
def quantityNormalizer(quantityStr):
    quantityStr = str(quantityStr)
    match = re.search(r'(\d+(?:\.\d+)?)\s*(.+)', quantityStr)
    if not match:
        return 1.0

    number = float(match.group(1))
    unit = match.group(2).strip().lower()

    conversions = {
        'gallon': 128, 'gal': 128, 'half gallon': 64, 'half gal': 64,
        'quart': 32, 'qt': 32, 'pint': 16, 'pt': 16,
        'liter': 33.814, 'l': 33.814, 'ml': 0.033814, 'milliliter': 0.033814,
        'fl oz': 1, 'fluid ounce': 1, 'lb': 16, 'lbs': 16, 'pound': 16,
        'pounds': 16, 'kg': 35.274, 'kilogram': 35.274,
        'g': 0.035274, 'gram': 0.035274, 'oz': 1, 'ounce': 1, 'ounces': 1,
        'count': 1, 'ct': 1, 'each': 1, 'ea': 1, 'dozen': 12, 'doz': 12
    }

    return number * conversions.get(unit, 1)


#references:
#   item.py.itemRecommender
#   item.py.listRecommender
#   modelTrainer.py.modelMaker
#   modelTrainer.py.
def userQuery(uid):
    connection = dbConnect()
    if connection is None:
        print("Could Not Connect to DB")
        return 
    
    query = """
        SELECT qualPercent, pricePercent, quantPercent, shoppingSize, diet
        FROM userPreferences 
        WHERE uid = %s;
    """
    query2 = """
        SELECT store1ID, store2ID, store3ID, store4ID, store5ID
        FROM userStores
        WHERE uid = %s;
    """

    cursor = connection.cursor()
    cursor.execute(query, (uid,))
    row = cursor.fetchone()
    cursor.execute(query2, (uid,))
    stored = cursor.fetchall()
    print(stored)
    stores = [store for store in stored[0] if store]
    print(stores)

    format_strings = ','.join(['%s'] * len(stores))
    storeQuery = f"""
        SELECT storeName, storeAddress
        FROM storeInfo
        WHERE storeID IN ({format_strings});
    """
    cursor.execute(storeQuery, tuple(stores))
    storeInfo = cursor.fetchall()
    connection.close()
    return {
        "qualPercent": row[0],
        "pricePercent": row[1],
        "quantPercent": row[2],
        "shoppingSize": row[3],
        "diet": row[4]
    }, storeInfo

