import pymongo
from sensor.constant.database import DATABASE_NAME
import os
import certifi
ca = certifi.where()

class MongoDBClient:
    client = None

    def __init__(self, database_name=DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                mongodb_url = os.getenv("MONGODB_URL_KEY")
                print(mongodb_url)
                if "localhost" in mongodb_url:
                    MongoDBClient.client = pymongo.MongoClient(mongodb_url)
                else:
                    MongoDBClient.client = pymongo.MongoClient(mongodb_url, tlsCAFile=ca)
            self.client = MongoDBClient.client
            self.db = self.client[database_name]
            self.db_name = database_name
        except Exception as e:
            raise e