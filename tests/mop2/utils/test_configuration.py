import os
import uuid
from configparser import ConfigParser
from dotenv import load_dotenv
from unittest import TestCase
import logging

from mop2.utils.configuration import TESTINGPATH, TESTVARIABLES
from mop2.utils.files import change_dir


class TestConfiguration(TestCase):
    """
    Testing the configuration.py document generation
    """
    def setUp(self) -> None:
        load_dotenv()
        with change_dir(TESTINGPATH):
            self.config = ConfigParser()
            self.config.read(TESTVARIABLES)
