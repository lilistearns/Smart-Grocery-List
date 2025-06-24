from flask import Flask, request, jsonify, session
from flask_session import Session # server-side sessions
from cachelib.file import FileSystemCache # session backend
from flask_bcrypt import Bcrypt # password hashing
from flask_cors import CORS
import sys
sys.path.append("./Data")
import userFunctions


# Initializations
app = Flask(__name__)

app.config["SECRET_KEY"] = "secret" # set for testing purposes
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "cachelib"
app.config['SESSION_CACHELIB'] = FileSystemCache(cache_dir='flask_session', threshold=500)
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

Session(app)
bcrypt = Bcrypt(app)
CORS(app, supports_credentials = True)


""" @app.route("/test", methods=["GET"])
def get():
   return "Fetching Message..."


@app.route("/test", methods=["POST"])
def post():
    message = request.json.get("sendMessage")

    if not message:
        return jsonify({"message": "Please input some text"}), 400
    else:
        return jsonify({"message": message}) """


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
    username = request.jason.get("sendUsername")
    password = request.json.get("sendPassword")
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    if not (email and password):
        return jsonify({"message": "Please input an email and a password"}), 400
    else:
        session["email"] = email
        userFunctions.addUserInfo(name, username, password_hash, email)


@app.route("/insertPreferences", methods=["POST"])
def insertPreferences():
    qual = request.json.get("qual")
    price = request.json.get("quant")
    quant = request.json.get("price")
    size = request.json.get("size")
    diet = request.json.get("diet")
    email = session.get("email")
    uid = userFunctions.getUID(email)

    userFunctions.insertPreferences(uid, qual, price, quant,size, diet)


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

    email = session.get("email")
    uid = userFunctions.getUID(email)
    userFunctions.updateStores(uid,[storeID1,storeID2,storeID3,storeID4,storeID5])

@app.route("/updatePreferences", methods=["POST"])
def updatePreferences():
    qual = request.json.get("qual")
    price = request.json.get("quant")
    quant = request.json.get("price")

    email = session.get("email")
    uid = userFunctions.getUID(email)
    userFunctions.updatePreferences(uid, qual, price, quant)

@app.route("/updateDiet", methods=["POST"])
def updateDiet():
    diet = request.json.get("diet")
    email = session.get("email")
    uid = userFunctions.getUID(email)
    userFunctions.updateDiet(uid, diet)


@app.route("/updateShoppingSize", methods=["POST"])
def updateShoppingSize():
    size = request.json.get("size")
    email = session.get("email")
    uid = userFunctions.getUID(email)
    userFunctions.updateShoppingSize(uid, size)

if __name__ == '__main__':
    app.run(debug=True)