from flask import request, jsonify
from werkzeug.security import check_password_hash

def signin(users_collection):
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        # Validate input data
        if not email or not password:
            return jsonify({'message': 'Please provide both email and password'}), 400

        # Check if user exists
        user = users_collection.find_one({'email': email})
        if not user:
            return jsonify({'message': 'Invalid email or password'}), 401

        # Verify password
        if not check_password_hash(user['password'], password):
            return jsonify({'message': 'Invalid email or password'}), 401

        # Remove sensitive information before returning the user object
        user.pop('password')
        return jsonify({'success': True, 'message': 'Signin successful', 'user': user}), 200

    except Exception as error:
        print("Error while signing in:", error)
        return jsonify({'message': 'Failed to sign in'}), 500
