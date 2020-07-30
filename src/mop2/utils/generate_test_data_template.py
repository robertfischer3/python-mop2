from configparser import ConfigParser
from contextlib import contextmanager
import os

from dotenv import load_dotenv

from mop2.utils.atomic_writes import atomic_write
from mop2.utils.files import change_dir

CONFVARIABLES = "app.config.ini"
OPERATIONSPATH = "../../../data"
TESTVARIABLES = "test.app.config.ini"
TESTINGPATH = "../../../data"

def create_baseline_configuration(configuration_file):
    """
        This method supports the auto-generation of test data.  Use this method in any way that supports
        the secure management of test data
    :return:
    """
    load_dotenv()
    config = ConfigParser()