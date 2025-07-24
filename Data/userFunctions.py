import mysql.connector
import sys
import json
import os
import re


def db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="comp5500",
            password="1qaz2wsx!QAZ@WSX",
            database="listBase"
        )
    except mysql.connector.Error as err:
        print(f"DB connection error: {err}")
        return None

# userInfoCreation
def addUserInfo(name, username, password, email):
    connection = db()
    if not connection:
        return None
    connector = connection.cursor()

    try:
        connector.execute("""
            INSERT INTO userInfo (name, username, password, email)
            VALUES (%s, %s,%s,%s)
        """, (name, username, password, email))
        connection.commit()
        uid = connector.lastrowid
        print(f"New user added with uid: {uid}")
        return uid
    except mysql.connector.Error as err:
        print(f"Insert error: {err}")
        return None
    finally:
        connector.close()
        connection.close()

# creates User Preferences
def insertPreferences(uid, qual, price, quant, size, diet):
    connection = db()
    if not connection:
        return
    connector = connection.cursor()

    try:
        connector.execute("""
            INSERT INTO userPreferences (uid, qualPercent, pricePercent, quantPercent, shoppingSize, diet)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (uid, qual, price, quant, size, diet))
        connection.commit()
        print(f"Inserted preferences for uid {uid}")
    except mysql.connector.Error as err:
        print(f"Insert preference error: {err}")
    finally:
        connector.close()
        connection.close()

#update prefernces
def updatePreferences(uid, qual, price, quant):
    connection = db()
    if not connection:
        return
    connector = connection.cursor()

    try:
        connector.execute("""
            UPDATE userPreferences
            SET qualPercent = %s, pricePercent = %s, quantPercent = %s
            WHERE uid = %s
        """, (qual, price, quant, uid))
        connection.commit()
        print(f"Updated percent preferences for uid {uid}")
    except mysql.connector.Error as err:
        print(f"Update percent error: {err}")
    finally:
        connector.close()
        connection.close()

# update shopping size
def updateShoppingSize(uid, size):
    connection = db()
    if not connection:
        return
    connector = connection.cursor()

    try:
        connector.execute("""
            UPDATE userPreferences
            SET shoppingSize = %s
            WHERE uid = %s
        """, (size, uid))
        connection.commit()
        print(f"Updated shoppingSize for uid {uid}")
    except mysql.connector.Error as err:
        print(f"Update shoppingSize error: {err}")
    finally:
        connector.close()
        connection.close()

# updates diet
def updateDiet(uid, diet):
    connection = db()
    if not connection:
        return
    connector = connection.cursor()
    print(diet)
    try:
        connector.execute("""
            UPDATE userPreferences
            SET diet = %s
            WHERE uid = %s
        """, (diet, uid))
        connection.commit()
        print(f"Updated diet for uid {uid}")
    except mysql.connector.Error as err:
        print(f"Update diet error: {err}")
    finally:
        connector.close()
        connection.close()

# storesUpdater
def updateStores(uid, storeIDs):
    connection = db()
    if not connection:
        return
    connector = connection.cursor()

    try:
        storeIDs = list(storeIDs) + [None] * (5 - len(storeIDs))
        connector.execute("SELECT uid FROM userStores WHERE uid = %s", (uid,))
        userExists = connector.fetchone()

        if userExists:
            connector.execute("""
                UPDATE userStores
                SET store1ID = %s, store2ID = %s, store3ID = %s, store4ID = %s, store5ID = %s
                WHERE uid = %s
            """, (*storeIDs, uid))
            print(f"Updated stores for user {uid}")
        else:
            connector.execute("""
                INSERT INTO userStores (uid, store1ID, store2ID, store3ID, store4ID, store5ID)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (uid, *storeIDs))
            print(f"Inserted new user {uid} with stores")

        connection.commit()
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        connector.close()
        connection.close()

#insertStores
def insertStores(uid, storeIDs):
    connection = db()
    if not connection:
        return
    cursor = connection.cursor()

    try:
        storeIDs = list(storeIDs) + [0] * (5 - len(storeIDs))
        storeIDs = storeIDs[:5]
        storeIDs = [int(s) if str(s).isdigit() else 0 for s in storeIDs]

        cursor.execute("""
            INSERT INTO userStores (uid, store1ID, store2ID, store3ID, store4ID, store5ID)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (uid, *storeIDs))
        
        connection.commit()
        print(f"Inserted stores for user {uid}: {storeIDs}")

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        cursor.close()
        connection.close()


def getStoreIDs(stores):
    connection = db()
    if not connection:
        return [0] * len(stores)
    cursor = connection.cursor()
    try:
        presentStores = []
        index = []
        for i, store in enumerate(stores):
            if store and store != "0" and store != "":
                presentStores.append(store)
                index.append(i)
        storeIDs = [0] * len(stores)
        if not presentStores:
            return storeIDs
        placeholders = ','.join(['%s' for _ in presentStores])
        query = f"SELECT storeID, storeName FROM storeInfo WHERE storeName IN ({placeholders})"
        cursor.execute(query, presentStores)
        results = cursor.fetchall()
        storeIDMap = {row[1]: row[0] for row in results}
        for i, store in enumerate(presentStores):
            original_pos = index[i]
            storeIDs[original_pos] = storeIDMap.get(store, 0)
        return storeIDs
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return [0] * len(stores)
    finally:
        cursor.close()
        connection.close()

# usernameChanger
def updateUserName(uid, new_name):
    connection = db()
    if not connection:
        return
    connector = connection.cursor()

    try:
        connector.execute("SELECT uid FROM userInfo WHERE uid = %s", (uid,))
        if connector.fetchone():
            connector.execute("UPDATE userInfo SET name = %s WHERE uid = %s", (new_name, uid))
            connection.commit()
            print(f"Updated name for uid {uid}")
        else:
            print(f"No user found with uid {uid}")
    except mysql.connector.Error as err:
        print(f"Update name error: {err}")
    finally:
        connector.close()
        connection.close()

# emailChanger
def updateUserEmail(uid, new_email):
    connection = db()
    if not connection:
        return
    connector = connection.cursor()

    try:
        connector.execute("SELECT uid FROM userInfo WHERE uid = %s", (uid,))
        if connector.fetchone():
            connector.execute("UPDATE userInfo SET email = %s WHERE uid = %s", (new_email, uid))
            connection.commit()
            print(f"Updated email for uid {uid}")
        else:
            print(f"No user found with uid {uid}")
    except mysql.connector.Error as err:
        print(f"Update email error: {err}")
    finally:
        connector.close()
        connection.close()

# passwordChanger
def updateUserPassword(uid, new_password):
    connection = db()
    if not connection:
        return
    connector = connection.cursor()

    try:
        connector.execute("SELECT uid FROM userInfo WHERE uid = %s", (uid,))
        if connector.fetchone():
            connector.execute("UPDATE userInfo SET password = %s WHERE uid = %s", (new_password, uid))
            connection.commit()
            print(f"Updated password for uid {uid}")
        else:
            print(f"No user found with uid {uid}")
    except mysql.connector.Error as err:
        print(f"Update password error: {err}")
    finally:
        connector.close()
        connection.close()

#logs user in returns boolean
def userLogin(username, password):
    connection = db()
    if not connection:
        return None
    connector = connection.cursor()

    try:
        connector.execute("""
            SELECT password FROM userInfo
            WHERE email = %s
        """, (username,))
        result = connector.fetchone()
        return result[0] if result else None
    except mysql.connector.Error as err:
        print(f"DB error: {err}")
        return "Wrong Username"
    finally:
        connector.close()
        connection.close()

#retrieves uid
def getUID(email):
    connection = db()
    if not connection:
        return None
    connector = connection.cursor()
    try:
        connector.execute("SELECT uid FROM userInfo WHERE email = %s", (email,))
        result = connector.fetchone()
        return result[0] if result else None
    except mysql.connector.Error as err:
        print(f"DB error: {err}")
        return None
    finally:
        connection.close()

def appendJson(filename, newData):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                existingData = json.load(f)
                if not isinstance(existingData, list):
                    existingData = [existingData]
            except json.JSONDecodeError:
                existingData = []
    else:
        existingData = []
    new_items = newData if isinstance(newData, list) else [newData]


    existing_urls = {item.get("url"): item for item in existingData if "url" in item}
    for item in new_items:
        existing_urls[item["url"]] = item  

    with open(filename, "w") as f:
        json.dump(list(existing_urls.values()), f, indent=2)

def acceptItem(item, uid):
    filename = f"./UserData/{uid}/Accepted/acceptedItems.json"
    cartname = f"./UserData/{uid}/cart.json"
    item_dict = {
        "store": item[0],
        "price": item[1],
        "url": item[2],
        "productName": item[3],
        "quantity": item[4]
    }
    appendJson(filename, item_dict)
    appendJson(cartname,item_dict)
    print(f"Appended item to {filename}")

def rejectItem(item, uid):
    filename = f"./UserData/{uid}/Rejected/rejectedItems.json"
    item_dict = {
        "store": item[0],
        "price": item[1],
        "url": item[2],
        "productName": item[3],
        "quantity": item[4]
    }
    appendJson(filename, item_dict)
    print(f"Appended item to {filename}")

def acceptList(itemlist, uid):
    filename = f"./UserData/{uid}/Accepted/acceptedItems.json"
    cartname = f"./UserData/{uid}/cart.json"
    items = []
    for item in itemlist:
        item_dict = {
            "store": item[0],
            "price": item[1],
            "url": item[2],
            "productName": item[3],
            "quantity": item[4]
        }
        items.append(item_dict)

    appendJson(filename, items)
    appendJson(cartname,item_dict)

    directory = f"./UserData/{uid}/Accepted/"
    saveListRecommendation(itemlist, uid, directory)
    print(f"Appended {len(items)} items to {filename}")

def rejectList(itemlist, uid):
    directory = f"./UserData/{uid}/Rejected/"
    saveListRecommendation(itemlist, uid, directory)

def saveListRecommendation(itemlist, uid, directory):
    os.makedirs(directory, exist_ok=True)

    existing = [
        f for f in os.listdir(directory)
        if f.startswith(f"list-") and f.endswith(".json")
    ]
    numbers = []
    for f in existing:
        try:
            num = int(f.split("list-")[1].split(".json")[0])
            numbers.append(num)
        except ValueError:
            continue

    nextNum = max(numbers, default=0) + 1
    filename = f"list-{nextNum}.json"
    filepath = os.path.join(directory, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(itemlist, f, indent=2)

    print(f"Saved list to {filepath}")

def getMax(directory):
    pattern = re.compile(r"list-(\d+)\.json$")
    numbers = []

    for filename in os.listdir(directory):
        match = pattern.match(filename)
        if match:
            numbers.append(int(match.group(1)))

    return max(numbers) if numbers else None

def getPastList(listNumber, uid, directory):
    directoryPath = f"./UserData/{uid}/{directory}"
    pageMax = getMax(directoryPath)
    num = pageMax-listNumber
    if(num<=0):
        return "No More Lists"
    directoryPath = f"./UserData/{uid}/{directory}"
    fullPath = f"{directoryPath}/list-{num}.json"

    with open(fullPath, "r") as f:
        data = json.load(f)  


    pastList= [tuple(item) for item in data]

    return pastList

def getCart(uid):
    with open(f"./UserData/{uid}/cart.json", "r") as f:
        data = json.load(f)  

    cart= [tuple(item) for item in data]

    return cart

def getCartSize(uid):
    with open(f"./UserData/{uid}/cart.json", "r") as f:
        data = json.load(f)  
    x = 0
    for item in data:
        x+=1
    return x

def getModel(qual, price, quant):
    # Ensure numeric input
    qual = float(qual)
    price = float(price)
    quant = float(quant)

    weights = {
        'quality': qual,
        'price': price,
        'quantity': quant
    }

    if max(weights.values()) - min(weights.values()) < 0.1:
        return 'balanced'

    if qual >= 0.8 and price <= 0.4:
        return 'premium'
    elif price >= 0.8 and qual <= 0.5:
        return 'budget'
    elif quant >= 0.8:
        return 'bulk'
    
    dominant = max(weights, key=weights.get)
    return dominant
