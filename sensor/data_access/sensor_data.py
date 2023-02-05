import sys
from typing import Optional
import pandas as pd
import numpy as np
import json
from sensor.configuration.mongodb_connection import MongoDBClient
from sensor.exception import SensorException

class SensorData:
    """
    This class is responsible for exporting data from mongodb record as dataframe
    """
    
    def __init__(self):
        try:
            self.mongodb_client = MongoDBClient()
        except Exception as e:
            raise SensorException(e, sys)
        
    def save_csv_file(self, file_path, collection_name: str, database_name: Optional[str] = None):
        try:
            data_frame = pd.read_csv(file_path)
            data_frame.reset_index(drop=True, inplace=True)
            records = list(json.loads(data_frame.T.to_json()).values())
            if database_name is None:
                collection = self.mongodb_client.database[collection_name]
            else:
                collection = self.mongodb_client.client[database_name][collection_name]
            collection.insert_many(records)
            return len(records)
        except Exception as e:
            raise SensorException(e, sys)
        
    def export_collection_as_dataframe(self, collection_name: str, database_name: Optional[str] = None) -> pd.DataFrame:
        """
        This method is responsible for exporting collection as dataframe
        :param collection_name: collection name
        :param database_name: database name
        :return: dataframe
        """
        try:
            if database_name is None:
                collection = self.mongodb_client.database[collection_name]
            else:
                collection = self.mongodb_client.client[database_name][collection_name]
            data_frame = pd.DataFrame(list(collection.find()))

            if "_id" in data_frame.columns.to_list():
                data_frame.drop(columns="_id", axis=1)
            data_frame.replace({np.nan: None}, inplace=True)
            return data_frame
        except Exception as e:
            raise SensorException(e, sys)