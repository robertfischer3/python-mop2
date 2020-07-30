from configparser import ConfigParser

from azure.mgmt.resource import PolicyClient

from mop2.comprehension.azure.identity.azure_identity_credential_adapter import (
    AzureIdentityCredentialAdapter,
)
from mop2.utils.files import change_dir

from mop2.utils.configuration import OPERATIONSPATH, CONFVARIABLES


class PolicyDefinition:
    def __init__(self, operations_path=OPERATIONSPATH, config_variables=CONFVARIABLES):
        with change_dir(operations_path):
            self.config = ConfigParser()
            self.config.read(config_variables)
            self.subscription_id = self.config["DEFAULT"]["azure_subscription_id"]
            self.tenant_id = self.config["DEFAULT"]["azure_management_group_id"]

    def get_at_management_group(
        self,
        policy_definition_name,
        credentials=None,
        management_group_id=None,
        subscription_id=None,
        raw=False,
    ):
        if credentials is None:
            credentials = AzureIdentityCredentialAdapter()

        if subscription_id is None:
            subscription_id = self.subscription_id

        #     Defaults to the root management group unless specified in the parameter list
        if management_group_id is None:
            management_group_id = self.tenant_id

        policy_client = PolicyClient(
            credentials=credentials, subscription_id=subscription_id
        )

        policy_definition = policy_client.policy_definitions.get_at_management_group(
            policy_definition_name=policy_definition_name,
            management_group_id=management_group_id,
            raw=raw,
        )

        return policy_definition

    def list_for_management_group(
        self, management_group_id, credentials=None, subscription_id=None
    ):
        if credentials is None:
            credentials = AzureIdentityCredentialAdapter()

        if subscription_id is None:
            subscription_id = self.subscription_id

        #     Defaults to the root management group unless specified in the parameter list
        if management_group_id is None:
            management_group_id = self.tenant_id

        policy_client = PolicyClient(
            credentials=credentials, subscription_id=subscription_id
        )

        policy_definition_list = policy_client.policy_definitions.list_by_management_group(
            management_group_id=management_group_id
        )

        return policy_definition_list

    def create(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

    def batch_create(self):
        raise NotImplementedError
