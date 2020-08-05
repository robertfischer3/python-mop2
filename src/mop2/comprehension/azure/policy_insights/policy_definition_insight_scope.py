from configparser import ConfigParser

from azure.mgmt.policyinsights import PolicyInsightsClient

from mop2.utils.configuration import OPERATIONSPATH, CONFVARIABLES
from mop2.utils.files import change_dir


class PolicyDefinitionInsightScope:

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

    def list_query_results_for_policy_definition(self, subscription_id, policy_definition_name, query_options=None, raw=None, credentials=None):
        policy_insights_client = PolicyInsightsClient(credentials)
        summarize_for_policy_definition = policy_insights_client.policy_states.summarize_for_policy_definition(subscription_id=subscription_id,
                                                                             policy_definition_name=policy_definition_name,
                                                                             query_options=query_options,
                                                                             raw=raw)
        return summarize_for_policy_definition