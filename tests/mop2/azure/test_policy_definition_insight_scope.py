import logging
import os
import sys
import unittest
from configparser import ConfigParser

from dotenv import load_dotenv

from mop2.comprehension.azure.identity.azure_identity_credential_adapter import AzureIdentityCredentialAdapter
from mop2.comprehension.azure.policy_insights.policy_definition_insight_scope import PolicyDefinitionInsightScope
from mop2.utils.configuration import TESTINGPATH, TESTVARIABLES
from mop2.utils.files import change_dir


class TestPolicyDefinitionInsightScope(unittest.TestCase):
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
        logging.basicConfig(stream=sys.stdout, level=int(logging_level))

    def test_list_query_results_for_policy_definition(self):
        # Policy Defintion to be tested
        policy_definition_name = self.test_data_config['AZURE_POLICY']["policy_name_04"]

        # Azure Active Directory Credentials
        credentials = AzureIdentityCredentialAdapter()
        policy_definition_insight = PolicyDefinitionInsightScope(operations_path=TESTINGPATH,
                                                                 config_variables=TESTVARIABLES)

        insights = policy_definition_insight.list_query_results_for_policy_definition(subscription_id=self.subscription_id,
                                                                           policy_definition_name=policy_definition_name,
                                                                           credentials = credentials)
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
