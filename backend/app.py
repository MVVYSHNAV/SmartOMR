from flask import Flask, request, jsonify
from pymongo import MongoClient, errors
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import re
import logging

app = Flask(__name__)
CORS(app)

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Setup MongoDB connection
try:
    client = MongoClient("mongodb+srv://smartomr:smartomrdb1@cluster0.qj6tpvi.mongodb.net/")
    db = client.omrsheer
    users_collection = db.users
    logging.info("Connected to MongoDB successfully")
except errors.ConnectionError as e:
    logging.error(f"Error connecting to MongoDB: {e}")

@app.route('/getdata', methods=['GET'])
def get_data():
    return jsonify({"message": "hello world"}), 200

def is_valid_email(email):
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(regex, email)

@app.route('/signup', methods=['POST'])
def signup():
    logging.debug("Sign-up request received")
    if request.is_json:
        data = request.get_json()
        logging.debug(f"Request data: {data}")
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            logging.warning("Missing username, email, or password")
            return jsonify({"error": "Please provide username, email, and password"}), 400

        if not is_valid_email(email):
            logging.warning("Invalid email format")
            return jsonify({"error": "Invalid email format"}), 400

        if len(password) < 6:
            logging.warning("Password too short")
            return jsonify({"error": "Password must be at least 6 characters long"}), 400

        try:
            if users_collection.find_one({"email": email}):
                logging.warning("Email already exists")
                return jsonify({"error": "Email already exists"}), 400

            hashed_password = generate_password_hash(password)
            user = {"username": username, "email": email, "password": hashed_password}
            users_collection.insert_one(user)
            logging.info("User registered successfully")

            return jsonify({"message": "User registered successfully"}), 201
        except errors.PyMongoError as e:
            logging.error(f"Database error: {e}")
            return jsonify({"error": f"Database error: {e}"}), 500
    else:
        logging.error("Invalid request. Non-JSON data received")
        return jsonify({"error": "Invalid request. Please provide JSON data."}), 415

@app.route('/signin', methods=['POST'])
def signin():
    logging.debug("Sign-in request received")
    if request.is_json:
        data = request.get_json()
        logging.debug(f"Request data: {data}")
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            logging.warning("Missing email or password")
            return jsonify({"error": "Please provide email and password"}), 400

        try:
            user = users_collection.find_one({"email": email})
            logging.debug(f"User found: {user}")
            if user and check_password_hash(user['password'], password):
                logging.info("Signed in successfully")
                return jsonify({"message": "Signed in successfully"}), 200
            else:
                logging.warning("Invalid email or password")
                return jsonify({"error": "Invalid email or password"}), 401
        except errors.PyMongoError as e:
            logging.error(f"Database error: {e}")
            return jsonify({"error": f"Database error: {e}"}), 500
    else:
        logging.error("Invalid request. Non-JSON data received")
        return jsonify({"error": "Invalid request. Please provide JSON data."}), 415

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
