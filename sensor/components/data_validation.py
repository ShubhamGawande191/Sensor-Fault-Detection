import os, sys
from sensor.logger import logging
from sensor.exception import SensorException
import pandas as pd
from scipy.stats import ks_2samp
from distutils import dir_util
from sensor.constant.training_pipeline import SCHEMA_FILE_PATH
from sensor.entity.artifact_entity import DataValidationArtifact, DataIngestionArtifact
from sensor.entity.config_entity import DataValidationConfig
from sensor.utils.main_utils import read_yaml_file, write_yaml_file

class DataValidation:

    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise SensorException(e, sys)
        
    def drop_zero_variance_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            df = df.loc[:, df.var() != 0]
            return df
        except Exception as e:
            raise SensorException(e, sys)
        
    def validate_number_of_columns(self, df: pd.DataFrame) -> bool:
        try:
            logging.info("Validating number of columns")
            logging.info("Number of columns in the dataframe: {}".format(df.shape[1]))
            logging.info("Required number of columns: {}".format(len(self._schema_config['columns'])))
            if df.shape[1] == len(self._schema_config['columns']):
                return True
            else:
                return False
        except Exception as e:
            raise SensorException(e, sys)
    
    def is_numerical_column_exist(self, dataframe: pd.DataFrame) -> bool:
        try:
            numerical_columns = self._schema_config["numerical_columns"]
            dataframe_columns = dataframe.columns

            numerical_column_present = True
            missing_numerical_columns = []
            for num_column in numerical_columns:
                if num_column not in dataframe_columns:
                    numerical_column_present=False
                    missing_numerical_columns.append(num_column)
            
            logging.info(f"Missing numerical columns: [{missing_numerical_columns}]")
            return numerical_column_present
        except Exception as e:
            raise SensorException(e,sys)
    
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            raise SensorException(e, sys)
        
    def detect_dataset_drift(self, base_df, current_df, threshold=0.05)->bool:
        try:
            status=True
            report ={}
            for column in base_df.columns:
                d1 = base_df[column]
                d2  = current_df[column]
                is_same_dist = ks_2samp(d1,d2)
                if threshold<=is_same_dist.pvalue:
                    is_found=False
                else:
                    is_found = True 
                    status=False
                report.update({column:{
                    "p_value":float(is_same_dist.pvalue),
                    "drift_status":is_found
                    
                    }})
            
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            
            # Create directory if not exists
            if not os.path.exists(os.path.dirname(drift_report_file_path)):
                os.makedirs(os.path.dirname(drift_report_file_path))
            write_yaml_file(file_path=drift_report_file_path,content=report,)
            return status
        except Exception as e:
            raise SensorException(e,sys)
        
    def validate_data(self) -> DataValidationArtifact:
        try:
            error_message = ""
            status = True
            # Read data from the file
            train_dataframe = DataValidation.read_data(self.data_ingestion_artifact.train_data_file_path)
            test_dataframe = DataValidation.read_data(self.data_ingestion_artifact.test_data_file_path)

            # Validate number of columns
            if not self.validate_number_of_columns(train_dataframe):
                error_message = f"{error_message} Number of columns in the train data is not matching with the schema file. \n"
            if not self.validate_number_of_columns(test_dataframe):
                error_message = f"{error_message} Number of columns in the test data is not matching with the schema file. \n"

            # Validate numerical columns
            if not self.is_numerical_column_exist(train_dataframe):
                error_message = f"{error_message} Numerical columns are missing in the train data. \n"
            if not self.is_numerical_column_exist(test_dataframe):
                error_message = f"{error_message} Numerical columns are missing in the test data. \n"

            if len(error_message) > 0:
                raise Exception(error_message)
            
            # Detect dataset drift
            status = self.detect_dataset_drift(base=train_dataframe, current_df=test_dataframe)
            data_validation_artifact = DataValidationArtifact(validation_status=status, 
                                                              validation_train_file_path=self.data_ingestion_artifact.train_file_path, 
                                                              validation_test_file_path=self.data_ingestion_artifact.test_file_path,
                                                              invalid_train_file_path=None, 
                                                              invalid_test_file_path=None,
                                                              drift_report_file_path=self.data_validation_config.drift_report_file_path)
            
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise SensorException(e, sys)
            