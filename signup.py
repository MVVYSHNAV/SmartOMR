from flask import jsonify, request
from werkzeug.security import generate_password_hash

def signup(users_collection):
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Please provide both email and password'}), 400

    user = users_collection.find_one({'email': email})
    if user:
        return jsonify({'message': 'Email already exists'}), 400

    hashed_password = generate_password_hash(password, method='sha256')
    users_collection.insert_one({'email': email, 'password': hashed_password})
    return jsonify({'success': True, 'message': 'User account created successfully', 'user': email}), 201
