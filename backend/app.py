from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

# Setup MongoDB connection
client = MongoClient("mongodb+srv://smartomr:smartomrdb1@cluster0.qj6tpvi.mongodb.net/") 
db = client.omrsheer 
users_collection = db.users  

@app.route('/getdata', methods=['GET'])
def get_data():
    return jsonify({"message": "hello world"})

@app.route('/signup', methods=['POST'])
def signup():
    if request.is_json:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return jsonify({"error": "Please provide username, email, and password"}), 400

        if users_collection.find_one({"email": email}):
            return jsonify({"error": "Email already exists"}), 400

        hashed_password = generate_password_hash(password)
        user = {"username": username, "email": email, "password": hashed_password}
        users_collection.insert_one(user)

        return jsonify({"message": "User registered successfully"}), 201
    else:
        return jsonify({"error": "Invalid request. Please provide JSON data."}), 415

@app.route('/signin', methods=['POST'])
def signin():
    if request.is_json:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"error": "Please provide email and password"}), 400

        user = users_collection.find_one({"email": email})
        if user and check_password_hash(user['password'], password):
            return jsonify({"message": "Signed in successfully"}), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401
    else:
        return jsonify({"error": "Invalid request. Please provide JSON data."}), 415

if __name__ == "__main__":
    app.run(host='192.168.1.17', port=5000, debug=True)