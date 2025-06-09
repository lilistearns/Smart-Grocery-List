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

# adds user and does it by incrementing uid
def addUserInfo(name, email,username, password):
    connection = db()
    if not connection:
        return None
    connector = connection.cursor()

    try:
        connector.execute("""
            INSERT INTO userInfo (name,username, password email)
            VALUES (%s, %s)
        """, (name, email))
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

# can be used to add or update preferences for user
def updatePreferences(uid, qual, price, quant, size, diet):
    connection = db()
    if not connection:
        return
    connector = connection.cursor()

    try:
        connector.execute("SELECT uid FROM userPreferences WHERE uid = %s", (uid,))
        if connector.fetchone():
            connector.execute("""
                UPDATE userPreferences SET
                    qualPercent = %s, pricePercent = %s, quantPercent = %s,
                    shoppingSize = %s, diet = %s
                WHERE uid = %s
            """, (qual, price, quant, size, diet, uid))
            print(f"Updated preferences for uid {uid}")
        else:
            connector.execute("""
                INSERT INTO userPreferences (uid, qualPercent, pricePercent, quantPercent, shoppingSize, diet)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (uid, qual, price, quant, size, diet))
            print(f"Added preferences for uid {uid}")
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Preference error: {err}")
    finally:
        connector.close()
        connection.close()

# can be used to add store to user in userStores
def userStores(uid, storeIDs):
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

# main program
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Add user:           python user.py addUser <name> <email> <username> <password>")
        print("  Update prefs:       python user.py prefs <uid> <qual> <price> <quant> <size> <diet>")
        print("  Add store:          python user.py store <uid> <storeID> <storeID> .. up to 5")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "addUser" and len(sys.argv) == 4:
        name = sys.argv[2]
        email = sys.argv[3]
        username = sys.argv[4]
        password = sys.argv[5]
        
        addUserInfo(name, email, username, password)

    elif cmd == "prefs" and len(sys.argv) == 8:
        uid = int(sys.argv[2])
        qual = float(sys.argv[3])
        price = float(sys.argv[4])
        quant = float(sys.argv[5])
        size = sys.argv[6]
        diet = sys.argv[7]
        updatePreferences(uid, qual, price, quant, size, diet)

    elif cmd == "store" and len(sys.argv) >= 4:
        uid = int(sys.argv[2])
        storeIDs = [int(arg) if arg.lower() != "none" else None for arg in sys.argv[3:8]]
        userStores(uid, storeIDs)

    else:
        print("Invalid command or arguments.")
