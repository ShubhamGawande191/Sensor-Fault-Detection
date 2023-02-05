import yaml
import os, sys
import numpy as np
from sensor.exception import SensorException
import dill

def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise SensorException(e, sys) from e

def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise SensorException(e, sys)

def save_numpy_array_data(file_path: str, data: np.array):
    """
    Saves numpy array data
    file_path: path to save the data
    data: numpy array data
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(os.path.dir_path, exist_ok=True)
        with open(file_path, "wb") as file:
            np.save(file, data)
    except Exception as e:
        raise SensorException(e, sys) from e
    
def load_numpy_array_data(file_path: str) -> np.array:
    """
    Loads numpy array data
    file_path: path to load the data
    """
    try:
        with open(file_path, "rb") as file:
            return np.load(file)
    except Exception as e:
        raise SensorException(e, sys) from e
    
def save_object(file_path: str, data: object):
    """
    Saves object data
    file_path: path to save the data
    data: object data
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(os.path.dir_path, exist_ok=True)
        with open(file_path, "wb") as file:
            dill.dump(data, file)
    except Exception as e:
        raise SensorException(e, sys) from e
    
def load_object(file_path: str) -> object:
    """
    Loads object data
    file_path: path to load the data
    """
    try:
        if not os.path.exists(file_path):
            raise SensorException("File not found: {}".format(file_path), sys)
        with open(file_path, "rb") as file:
            return dill.load(file)
    except Exception as e:
        raise SensorException(e, sys) from e