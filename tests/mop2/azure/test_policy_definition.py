import os
import uuid
from configparser import ConfigParser

from azure.common.client_factory import get_client_from_json_dict
from azure.mgmt.resource import PolicyClient, ResourceManagementClient

from mop2.comprehension.azure.identity.azure_identity_credential_adapter import AzureIdentityCredentialAdapter

from dotenv import load_dotenv
from unittest import TestCase
from mop2.comprehension.azure.resource_manager.policy_definition import PolicyDefinition as MopPolicyDefinition
from mop2.comprehension.azure.resource_manager.policy_assignment import PolicyAssignment as MopPolicyAssignment

import logging
import sys

from mop2.utils.configuration import TESTVARIABLES, TESTINGPATH
from mop2.utils.files import change_dir


class TestPolicyDefinition(TestCase):
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

    def test_get(self):
        credentials = AzureIdentityCredentialAdapter()

        policy_definition_client = MopPolicyDefinition(operations_path=TESTINGPATH, config_variables=TESTVARIABLES)
        policy_definition = policy_definition_client.get_at_management_group(
            policy_definition_name=self.test_data_config['AZURE_POLICY']["policy_name_02"],
            management_group_id=self.tenant_id)

        self.assertTrue("PolicyDefinition" in str(type(policy_definition)))


    def test_get_subscription_level(self):
        credentials = AzureIdentityCredentialAdapter()

        policy_client = PolicyClient(credentials=credentials, subscription_id=self.subscription_id)

        policy_definition = policy_client.policy_definitions.get(
            policy_definition_name=self.test_data_config['AZURE_POLICY']["policy_name_03"])

        self.assertIsNotNone(policy_definition)
        self.assertTrue("PolicyDefinition" in str(type(policy_definition)))

    def test_get_subscription_level_raw(self):
        credentials = AzureIdentityCredentialAdapter()
        policy_client = PolicyClient(credentials=credentials, subscription_id=self.subscription_id)

        policy_definition_name = self.test_data_config['AZURE_POLICY']["policy_name_04"]

        policy_definition = policy_client.policy_definitions.get(
            policy_definition_name=policy_definition_name, raw=True)

        self.assertIsNotNone(policy_definition)

    def test_list_at_subscription_level(self):

        credentials = AzureIdentityCredentialAdapter()
        policy_client = PolicyClient(credentials=credentials, subscription_id=self.subscription_id)
        policy_definitions = list(policy_client.policy_definitions.list())
        self.assertGreater(len(policy_definitions), 0)
        logging.debug("Subscription policy definition list count {}".format(len(policy_definitions)))


    def test_list_by_management_group(self):

        policy_definition_client = MopPolicyDefinition(operations_path=TESTINGPATH, config_variables=TESTVARIABLES)
        policy_definition_list = list(policy_definition_client.list_for_management_group(self.management_group_id))
        self.assertGreater(len(policy_definition_list), 0)
        logging.debug("Management group policy definition list count {}".format(len(policy_definition_list)))

    def test_get_at_management_group(self):

        policy_definition_client = MopPolicyDefinition(operations_path=TESTINGPATH, config_variables=TESTVARIABLES)

        policy_definition_name = self.test_data_config['AZURE_POLICY']["policy_name_02"]
        policy_definition = policy_definition_client.get_at_management_group(policy_definition_name)

        self.assertIsNotNone(policy_definition)
        self.assertTrue("PolicyDefinition" in str(type(policy_definition)))

    def test_create(self):
        credentials = AzureIdentityCredentialAdapter()

        policy_definition = MopPolicyDefinition(operations_path=TESTINGPATH, config_variables=TESTVARIABLES)
        assert policy_definition.create()

    def test_delete(self):
        credentials = AzureIdentityCredentialAdapter()

        policy_definition = MopPolicyDefinition(operations_path=TESTINGPATH, config_variables=TESTVARIABLES)
        assert policy_definition.delete()

    def test_batch_create(self):
        credentials = AzureIdentityCredentialAdapter()

        policy_definition = MopPolicyDefinition(operations_path=TESTINGPATH, config_variables=TESTVARIABLES)
        assert policy_definition.batch_create()
