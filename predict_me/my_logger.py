import logging
import os
import sys
import traceback
from pathlib import Path


def setup_logging_to_file():
    '''
    Setup and initializes the logging file
    :return: logger
    '''
    ERROR_LOGGER_FILE = Path(__file__).parent.parent
    ERROR_LOGGER_FILE = os.path.join(ERROR_LOGGER_FILE, 'Core', 'Errors.log')
    logger = logging.getLogger(__name__)
    formatter = logging.Formatter(
        '%(asctime)s, %(levelname)-4s [%(filename)s:%(lineno)d] %(funcName)s %(module)s %(msg)s',
        '%d-%m-%Y:%H:%M:%S')  # set log format
    logger.setLevel(logging.DEBUG)  # set the logger level
    file_handler = logging.FileHandler(ERROR_LOGGER_FILE)  # set the log file
    file_handler.setLevel(logging.ERROR)  # set the level for file handler
    file_handler.setFormatter(formatter)  # set the formatter for file handler
    logger.addHandler(file_handler)
    return logger


def log_exception(exp: Exception):
    # create logger obj
    logger = setup_logging_to_file()
    # first Extracts failing function name from Traceback
    tb = sys.exc_info()[-1]
    stk = traceback.extract_tb(tb, 1)
    fname = stk[0][3]
    exc_type, exc_obj, exc_tb = sys.exc_info()
    logger.error("{} {} {} ".format(exc_type, fname, exc_tb.tb_lineno))
    sys.stderr.write("{} {} {} ".format(exc_type, fname, exc_tb.tb_lineno))
    exc_type, exc_obj, exc_tb = sys.exc_info()
    # error_msg = str(exp) + " " + str(exc_tb.tb_lineno) + " " + str(fname)
    error_msg = str(sys.exc_info()[1])
    sys.stderr.write(error_msg)
    return error_msg
