import mysql.connector
import sys

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
            WHERE username = %s
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
        connector.close()
        connection.close()
