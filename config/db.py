from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()


class Connection:
    def __init__(self):
        self.client = MongoClient(os.getenv('MONGO_URI'))
        self.db = self.client['influencerai']

    def get_connection(self):
        return self.db

    def close_connection(self):
        self.client.close()


db = Connection().get_connection()
influencers_collection = db['influencers']
transcripts_collection = db['transcripts']
qna_collection = db['qnas']
