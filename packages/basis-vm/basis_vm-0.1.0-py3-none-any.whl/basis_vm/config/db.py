from pymongo import MongoClient
from .env import MONGO_CLIENT, DB_NAME

class Database:
    def __init__(self, uri: str, db_name: str):
        self._client = MongoClient(uri, connect=False)
        self._db = self._client[db_name]

    @property
    def smart_contracts(self):
        return self._db.smart_contracts

database = Database(MONGO_CLIENT, DB_NAME)
