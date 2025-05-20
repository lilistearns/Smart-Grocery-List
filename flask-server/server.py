from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def get():
   return "Temp"

    
@app.route("/", methods=["POST"])
def post():
    message = request.json.get("sendMessage")

    if not message:
        return jsonify({"message": "Please input some text"}), 400
    else:
        return jsonify({"message": message})
    

if __name__ == '__main__':
    app.run(debug=True)