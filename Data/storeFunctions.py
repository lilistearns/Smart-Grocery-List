import mysql.connector
import sys
import dataFunctions

def addOrUpdateStore(storeAddress, storeName, qualRating, priceRating, quantRating):
    connection = dataFunctions.dbConnect()()
    if not connection:
        return
    connector = connection.cursor()
    connector.execute("SELECT storeID FROM storeInfo WHERE storeAddress = %s", (storeAddress,))
    result = connector.fetchone()
    if result:
        storeID = result[0]
        connector.execute("""
            UPDATE storeInfo SET
                storeName = %s,
                qualRating = %s,
                priceRating = %s,
                quantRating = %s
            WHERE storeID = %s
        """, (storeName, qualRating, priceRating, quantRating, storeID))
        print(f"Updated store with ID {storeID}")
    else:
        connector.execute("""
            INSERT INTO storeInfo (storeAddress, storeName, qualRating, priceRating, quantRating)
            VALUES (%s, %s, %s, %s, %s)
        """, (storeAddress, storeName, qualRating, priceRating, quantRating))
        storeID = connector.lastrowid
        print(f"Added new store with ID {storeID}")
    connection.commit()
    connection.close()

if __name__ == "__main__":
    print(len(sys.argv))
    if len(sys.argv) != 6:
        print("Usage:")
        print("  python store.py <storeID> <storeAddress> <qualRating> <priceRating> <quantRating>")
        sys.exit(1)
        storeAddress = sys.argv[1]
        storeName = sys.argv[2]
        qualRating = float(sys.argv[3])
        priceRating = float(sys.argv[4])
        quantRating = float(sys.argv[5])
    addOrUpdateStore(storeAddress, storeName, qualRating, priceRating, quantRating)
    print("Store Information Updated")