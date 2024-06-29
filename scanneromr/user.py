from pymongo import MongoClient

class UserDatabase:
    def __init__(self, db_url='mongodb://localhost:27017/', db_name='omr_app'):
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.users = self.db['users']

    def add_user(self, username, email):
        user_data = {
            'username': username,
            'email': email
        }
        result = self.users.insert_one(user_data)
        return result.inserted_id

    def get_user(self, user_id):
        return self.users.find_one({'_id': user_id})

    def update_user(self, user_id, update_data):
        result = self.users.update_one({'_id': user_id}, {'$set': update_data})
        return result.modified_count

    def delete_user(self, user_id):
        result = self.users.delete_one({'_id': user_id})
        return result.deleted_count