import logging
import os
from datetime import datetime

class Logger:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.file_handler = logging.FileHandler(os.path.join(self.path, self.name + '.log'))
        self.file_handler.setLevel(logging.DEBUG)
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

LOG_FILE = f"{datetime.now().strftime('%d-%m-%Y-%H-%M-%S')}.log"
LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
LOG_NAME = "sensor"

logger = Logger(LOG_NAME, LOG_PATH)
