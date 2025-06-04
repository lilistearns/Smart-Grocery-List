from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def getHome():
   return "Welcome..."


@app.route("/test", methods=["GET"])
def get():
   return "Fetching Message..."
    
@app.route("/test", methods=["POST"])
def post():
    message = request.json.get("sendMessage")

    if not message:
        return jsonify({"message": "Please input some text"}), 400
    else:
        return jsonify({"message": message})
    

@app.route("/signup", methods=["POST"])
def create_user():
    email = request.json.get("sendEmail")
    password = request.json.get("sendPassword")

    if not (email and password):
        return jsonify({"message": "Please input an email and a password"}), 400
    else:
        return jsonify({
            "email": email,
            "password": password
        })


@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("sendEmail")
    password = request.json.get("sendPassword")

    if not (email and password):
        return jsonify({"message": "Please enter your email and password"}), 400
    else:
        return jsonify({
            "email": email,
            "password": password
        })



if __name__ == '__main__':
    app.run(debug=True)