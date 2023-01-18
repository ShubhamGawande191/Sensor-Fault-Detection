import pymongo
from sensor.constant.database import DATABASE_NAME
import certifi
ca = certifi.where()

class MongoDBClient:
    client = None
    db = None
    def __init__(self, database_name=DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                mongodb_url = ''
                MongoDBClient.client = pymongo.MongoClient()
            self.client = pymongo.MongoClient()
            self.db = self.client[database_name]
            self.db_name = database_name
        except Exception as e:
            raise