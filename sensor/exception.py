import sys

def error_messsage(error):
    _, _, exc_tb = sys.exc_info()

    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    print("Error in file: " + file_name + " at line: " + str(line_number) + " with error: " + error)

class SensorException(Exception):
    """
    param error message: error message is a string that will be logged to the error log file
    """
    def __init__(self, message):
        super().__init__(message)
        error_messsage(message)

    def __str__(self):
        return self.message
