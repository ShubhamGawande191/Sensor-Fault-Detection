import logging
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%d-%m-%Y-%H-%M-%S')}.log"
LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
LOG_NAME = "sensor"

logging.basicConfig(
    filename=LOG_PATH,
    format="[%(asctime)s] %(lineno)d %(name)s %(levelname)s %(threadName)s : %(message)s",
    level=logging.INFO,
)
    
