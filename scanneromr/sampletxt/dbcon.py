from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']
collection = db['mycollection']

@app.route('/')
def home():
    return "Welcome to the Flask-MongoDB server!"

# Create
@app.route('/add', methods=['POST'])
def add_document():
    data = request.json
    result = collection.insert_one(data)
    return jsonify(str(result.inserted_id))

# Read
@app.route('/get/<id>', methods=['GET'])
def get_document(id):
    document = collection.find_one({"_id": ObjectId(id)})
    if document:
        return jsonify(document)
    else:
        return jsonify({"error": "Document not found"}), 404

# Update
@app.route('/update/<id>', methods=['PUT'])
def update_document(id):
    data = request.json
    result = collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    if result.modified_count > 0:
        return jsonify({"msg": "Document updated"})
    else:
        return jsonify({"error": "Document not found or data is same"}), 404

# Delete
@app.route('/delete/<id>', methods=['DELETE'])
def delete_document(id):
    result = collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count > 0:
        return jsonify({"msg": "Document deleted"})
    else:
        return jsonify({"error": "Document not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
