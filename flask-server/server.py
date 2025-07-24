from flask import Flask, request, jsonify, session
from flask_session import Session # server-side sessions
from cachelib.file import FileSystemCache # session backend
from flask_bcrypt import Bcrypt # password hashing
from flask_cors import CORS
from threading import Thread
import os 
import sys
sys.path.append("./Data")
import userFunctions
sys.path.append("./ML")
import item
import modelCreator
import shutil

# Initializations
app = Flask(__name__)

app.config["SECRET_KEY"] = "secret" # set for testing purposes
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "cachelib"
app.config['SESSION_CACHELIB'] = FileSystemCache(cache_dir='flask_session', threshold=500)
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "None"

Session(app)
bcrypt = Bcrypt(app)
CORS(app, supports_credentials = True)


@app.route("/", methods=["GET"])
def getHome():
    email = session.get("email")

    if email is not None:
        return jsonify({
            "email": email,
        })
    else:
        return jsonify({"error": "Not logged in"})


@app.route("/signup", methods=["POST"])
def create_user():
    name = request.json.get("sendName")
    email = request.json.get("sendEmail")
    username = request.json.get("sendUsername")
    password = request.json.get("sendPassword")
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    if not (email and password and name and username):

        return jsonify({"message": "Please Fill all fields"}), 400
    else:

        session["email"] = email
        userFunctions.addUserInfo(name, username, password_hash, email)
        return jsonify({"message": "Sign-up Successful"})


@app.route("/insertPreferences", methods=["POST"])
def insertPreferences():
    qual = request.json.get("qual")
    price = request.json.get("price") 
    quant = request.json.get("quant") 
    size = request.json.get("size")
    diet = request.json.get("diet")

    email = session.get("email")
    uid = userFunctions.getUID(email)
    dest_dir = f"UserData/{uid}"
    os.makedirs(dest_dir, exist_ok=True)
    userFunctions.insertPreferences(uid, qual, price, quant, size, diet)
    modelName = userFunctions.getModel(qual,price,quant)
    shutil.copy(f"TrainedModels/{modelName}.h5", f"UserData/{uid}/model-{uid}.h5")

    return jsonify({"message": "Preference Creation Successful"})


@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("sendEmail")
    password = request.json.get("sendPassword")

    # Logic to get user account based on email and check if hashed password matches input
    if not (email and password):
        return jsonify({"message": "Please enter your email and password"}), 400
    else:
        password_hash = userFunctions.userLogin(email,password)
        if(password_hash == "Wrong Username"):
            return jsonify({"message": "Username or Password cannot be found"})
        if(bcrypt.check_password_hash(password_hash, password)):
            session["email"] = email
            return jsonify({"message": "Login Successful"})
        else:
            return jsonify({"message": "Username or Password incorrect"})
 
    
@app.route("/logout", methods=["POST"])
def logout():
    session.pop("email", None)
    return jsonify({"action": "Logged Out"})

@app.route("/updateStores", methods=["POST"])
def updateStores():
    storeID1 = request.json.get("storeID1")
    storeID2 = request.json.get("storeID2")
    storeID3 = request.json.get("storeID3")
    storeID4 = request.json.get("storeID4")
    storeID5 = request.json.get("storeID5")
    stores = [storeID1,storeID2,storeID3,storeID4,storeID5]

    email = session.get("email")
    uid = userFunctions.getUID(email)
    storeIDS = userFunctions.getStoreIDs(stores)
    print(storeIDS)
    userFunctions.updateStores(uid,storeIDS)
    return jsonify({"message": "Update Successful"})

@app.route("/insertStores", methods=["POST"])
def insertStores():
    storeID1 = request.json.get("storeID1")
    storeID2 = request.json.get("storeID2")
    storeID3 = request.json.get("storeID3")
    storeID4 = request.json.get("storeID4")
    storeID5 = request.json.get("storeID5")
    stores = [storeID1,storeID2,storeID3,storeID4,storeID5]

    email = session.get("email")
    uid = userFunctions.getUID(email)
    storeIDS = userFunctions.getStoreIDs(stores)
    print(storeIDS)
    userFunctions.insertStores(uid,storeIDS)
    return jsonify({"message": "Update Successful"})

@app.route("/updatePreferences", methods=["POST"])
def updatePreferences():
    qual = request.json.get("qual")
    price = request.json.get("quant")
    quant = request.json.get("price")

    email = session.get("email")
    uid = userFunctions.getUID(email)
    status = userFunctions.updatePreferences(uid, qual, price, quant)
    print(status)
    return jsonify({"message": "Update Successful"})

@app.route("/updateDiet", methods=["POST"])
def updateDiet():
    diet = request.json.get("diet")
    print(diet)
    email = session.get("email")
    uid = userFunctions.getUID(email)
    userFunctions.updateDiet(uid, diet)
    return jsonify({"message": "Update Successful"})


@app.route("/updateShoppingSize", methods=["POST"])
def updateShoppingSize():
    size = request.json.get("size")
    email = session.get("email")
    uid = userFunctions.getUID(email)
    userFunctions.updateShoppingSize(uid, size)
    return jsonify({"message": "Update Successful"})

@app.route("/findItem", methods=["POST"])
def findItem():
    inputItem = request.json.get("item")
    email = session.get("email")
    uid = userFunctions.getUID(email)
    return item.itemRecommender(inputItem,uid)
    #OUTPUT: [('Hannaford', 1.49, 'https://www.hannaford.com/product/hannaford-whole-milk/932359?hdrKeyword=Milk', 'Hannaford Whole Milk', 'Quart'), ('Walmart', 1.88, 'https://www.walmart.com/ip/Great-Value-Milk-2-Reduced-Fat-Half-Gallon-64-fl-oz-Jug/10450119?classType=REGULAR&athbdg=L1600', 'Great Value Milk, 2% Reduced Fat, Half Gallon, 64 fl oz Jug', '1 each'), ('Walmart', 1.94, 'https://www.walmart.com/ip/Great-Value-Milk-Whole-Vitamin-D-Half-Gallon-Plastic-Jug-64oz/10450118?classType=REGULAR&athbdg=L1600', 'Great Value Milk Whole Vitamin D, Half Gallon, Plastic, Jug, 64oz', '64 oz')]
    #[(Store,price,URL,Product Name,quantity)]

    #NEW OUTPUT: [("Shaw's", 3.69, 'https://www.shaws.com/shop/product-details/970038173', 'Hood Whole Milk - 64 Oz', 'GAL HG'), ('Star Market', 3.69, 'https://www.starmarket.com/shop/product-details/970038173', 'Hood Whole Milk - 64 Oz', 'GAL HG'), ("Shaw's", 2.69, 'https://www.shaws.com/shop/product-details/136010013', 'Lucerne Milk - Half Gallon (container may vary)', 'GAL HG'), ('Star Market', 2.69, 'https://www.starmarket.com/shop/product-details/136010013', 'Lucerne Milk - Half Gallon (container may vary)', 'GAL HG'), ('Star Market', 2.69, 'https://www.starmarket.com/shop/product-details/136010016', 'Lucerne Milk Reduced Fat 2% Milkfat - 64 Fl. Oz. (package may vary)', 'GAL HG'), ("Shaw's", 2.69, 'https://www.shaws.com/shop/product-details/136010016', 'Lucerne Milk Reduced Fat 2% Milkfat - 64 Fl. Oz. (package may vary)', 'GAL HG'), ('Star Market', 6.99, 'https://www.starmarket.com/shop/product-details/136050129', 'Lactaid Whole Milk - 96 Oz', 'GAL. FZ'), ("Shaw's", 6.99, 'https://www.shaws.com/shop/product-details/136050129', 'Lactaid Whole Milk - 96 Oz', 'GAL. FZ'), ("Shaw's", 3.99, 'https://www.shaws.com/shop/product-details/136010449', 'Lucerne Milk Lowfat 1% Milkfat 1 Gallon - 128 Fl. Oz.', 'GAL. GA'), ('Star Market', 3.99, 'https://www.starmarket.com/shop/product-details/136010121', 'Lucerne Milk Whole 1 Gallon - 128 Fl. Oz.', 'GAL. GA')]


@app.route("/findList", methods=["POST"])
def findList():
    inputList = request.json.get("itemList")
    email = session.get("email")
    uid = userFunctions.getUID(email)
    return item.listRecommender(inputList, uid)
    #OUTPUT: [('Hannaford', 2.59, 'https://www.hannaford.com/product/hannaford-whole-milk/932363?hdrKeyword=Milk', 'Hannaford Whole Milk', 'Gallon'), ('Hannaford', 4.19, 'https://www.hannaford.com/product/nature-s-promise-free-range-large-brown-eggs/988051?hdrKeyword=Brown+Eggs', "Nature's Promise Free Range Large Brown Eggs", '12 Ct')]
    #[(Store,price,URL,Product Name,quantity),(Store,price,URL,Product Name,quantity),(Store,price,URL,Product Name,quantity),...,]

    #NEW OUTPUT: [[('Star Market', 3.99, 'https://www.starmarket.com/shop/product-details/136010121', 'Lucerne Milk Whole 1 Gallon - 128 Fl. Oz.', '1 ea'), ('Star Market', 4.49, 'https://www.starmarket.com/shop/product-details/960273951', 'Lucerne Farms Eggs Large Cage Free - 12 Count', 'DOZEN CT')], [("Shaw's", 3.99, 'https://www.shaws.com/shop/product-details/136010121', 'Lucerne Milk Whole 1 Gallon - 128 Fl. Oz.', '1 ea'), ("Shaw's", 4.49, 'https://www.shaws.com/shop/product-details/960273951', 'Lucerne Farms Eggs Large Cage Free - 12 Count', 'DOZEN CT')], [('Hannaford', 2.59, 'https://www.hannaford.com/product/hannaford-whole-milk/932363?hdrKeyword=Milk', 'Hannaford Whole Milk', 'Gallon'), ('Hannaford', 4.39, 'https://www.hannaford.com/product/pete-gerry-s-organic-cage-free-grade-a-extra-large-eggs/866130?hdrKeyword=Eggs', "Pete & Gerry's Organic Cage Free Grade A Extra Large Eggs", '6 Ct')]]
    

@app.route("/acceptItem", methods=["POST"])
def acceptItem():
    goodItem = request.json.get("itemAccept")
    email = session.get("email")
    uid = userFunctions.getUID(email)
    userFunctions.acceptItem(goodItem,uid)
    return jsonify({"message": "Item Accepted"}), 200

@app.route("/acceptList", methods=["POST"])
def acceptList():
    goodList = request.json.get("listAccept")
    email = session.get("email")
    uid = userFunctions.getUID(email)
    userFunctions.acceptList(goodList,uid)
    return jsonify({"message": "List Accepted"}), 200

@app.route("/rejectItem", methods=["POST"])
def rejectItem():
    badItem = request.json.get("itemReject")
    email = session.get("email")
    print(badItem)
    uid = userFunctions.getUID(email)
    userFunctions.rejectItem(badItem,uid)
    return jsonify({"message": "Item rejected"}), 200

@app.route("/rejectList", methods=["POST"])
def rejectList():
    badList= request.json.get("listReject")
    email = session.get("email")
    uid = userFunctions.getUID(email)
    userFunctions.rejectList(badList,uid)
    return jsonify({"message": "List rejected"}), 200

@app.route("/getPastList", methods=["POST"])
def getPastList():
    pageNumber = request.json.get("pageNumber")
    email = session.get("email")
    uid = userFunctions.getUID(email)
    return userFunctions.getPastList(pageNumber,uid)

@app.route("/getCart", methods=["POST"])
def getCart():
    email = session.get("email")
    uid = userFunctions.getUID(email)
    return userFunctions.getCart(uid)

@app.route("/getCartSize", methods=["POST"])
def getCartSize():
    email = session.get("email")
    uid = userFunctions.getUID(email)
    return userFunctions.getCartSize(uid)


if __name__ == '__main__':
    app.run(debug=True)