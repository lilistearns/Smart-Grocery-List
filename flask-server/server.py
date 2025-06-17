from flask import Flask, request, jsonify, session
from flask_session import Session # server-side sessions
from cachelib.file import FileSystemCache # session backend
from flask_bcrypt import Bcrypt # password hashing
from flask_cors import CORS

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
    email = request.json.get("sendEmail")
    password = request.json.get("sendPassword")

    hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')

    session["email"] = email

    if not (email and password):
        return jsonify({"message": "Please input an email and a password"}), 400
    else:
        return jsonify({
            "email": email,
            "password": hashed_password
        })


@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("sendEmail")
    password = request.json.get("sendPassword")

    # Logic to get user account based on email and check if hashed password matches input
    # bcrypt.check_password_hash(____, password)

    session["email"] = email

    if not (email and password):
        return jsonify({"message": "Please enter your email and password"}), 400
    else:
        return jsonify({
            "email": email,
        })
    
    
@app.route("/logout", methods=["POST"])
def logout():
    session.pop("email", None)
    return jsonify({"action": "Logged Out"})



if __name__ == '__main__':
    app.run(debug=True)