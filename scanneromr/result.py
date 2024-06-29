from pymongo import MongoClient

class ResultDatabase:
    def __init__(self, db_url='mongodb://localhost:27017/', db_name='omr_app'):
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.results = self.db['results']

    def add_result(self, user_id, score, details):
        result_data = {
            'user_id': user_id,
            'score': score,
            'details': details
        }
        result = self.results.insert_one(result_data)
        return result.inserted_id

    def get_result(self, result_id):
        return self.results.find_one({'_id': result_id})

    def update_result(self, result_id, update_data):
        result = self.results.update_one({'_id': result_id}, {'$set': update_data})
        return result.modified_count

    def delete_result(self, result_id):
        result = self.results.delete_one({'_id': result_id})
        return result.deleted_count
