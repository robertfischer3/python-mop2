from configparser import ConfigParser

from mop2.utils.configuration import OPERATIONSPATH, CONFVARIABLES
from mop2.utils.files import change_dir


class ManagementGroupInsightScope:

    def __init__(self, operations_path=OPERATIONSPATH, config_variables=CONFVARIABLES):
        with change_dir(operations_path):
            self.config = ConfigParser()
            self.config.read(config_variables)
            self.subscription_id = self.config["DEFAULT"]["azure_subscription_id"]
            self.management_group_id = self.config["DEFAULT"][
                "azure_management_group_id"
            ]
            self.operations_path = operations_path
            self.config_variables = config_variables
