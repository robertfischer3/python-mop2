import os
import logging
import sys
import uuid
from configparser import ConfigParser
from dotenv import load_dotenv
from unittest import TestCase

from mop2.comprehension.azure.identity.azure_identity_credential_adapter import AzureIdentityCredentialAdapter
from mop2.comprehension.azure.resource_manager.policy_assignment import PolicyAssignment as MopPolicyAssignment

from mop2.utils.configuration import TESTINGPATH, TESTVARIABLES
from mop2.utils.files import change_dir


class TestPolicyAssignment(TestCase):

    def setUp(self) -> None:
        load_dotenv()
        with change_dir(TESTINGPATH):
            self.config = ConfigParser()
            self.config.read(TESTVARIABLES)
            self.test_data_config = ConfigParser()
            test_data_file = self.config['DEFAULT']['test_data_file']
            self.test_data_config.read(test_data_file)

        self.subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
        self.tenant_id = os.environ["AZURE_TENANT_ID"]
        self.management_group_id = os.environ["AZURE_MANAGEMENT_GROUP_ID"]
        client_id = os.environ["CLIENT"]
        client_secret = os.environ["KEY"]

        logging_level = self.config['LOGGING']['level']
        logging.basicConfig(stream=sys.stdout, level=logging_level)

    def test_list_for_management_group(self):
        policy_assignment = MopPolicyAssignment(operations_path=TESTINGPATH, config_variables=TESTVARIABLES)
        policy_assignments = policy_assignment.list_for_management_group(management_group_id=self.management_group_id)

        self.assertGreater(len(policy_assignments), 0)
        logging.debug("Subscription policy definition list count {}".format(len(policy_assignments)))
        for policy_assignment in policy_assignments:
            logging.debug(policy_assignment)

    def test_policy_assignments_create_manage_group_assignment(self):
        policy_assignment_name = "security{}".format(str(uuid.uuid4().hex))[0:23]

        policy_assignment = MopPolicyAssignment(operations_path=TESTINGPATH, config_variables=TESTVARIABLES)

        policy_defintion_name = self.test_data_config['AZURE_POLICY']["policy_name_01"],

        policy_assignment.create_manage_group_assignment(policy_defintion_name=policy_defintion_name,
                                                         policy_assignment_name=policy_assignment_name,
                                                         )


