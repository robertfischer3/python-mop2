import json
from configparser import ConfigParser

from azure.mgmt.resource import PolicyClient
from tenacity import retry, wait_random, stop_after_attempt

from mop2.comprehension.azure.identity.azure_identity_credential_adapter import (
    AzureIdentityCredentialAdapter, )

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

    def batch_create_at_mangement_group(self, management_group_id, policy_definition_files):
        """
        policy_definition_files is a list with a dictonary that contains the policy_definition_path
        and policy_defintion_name and processes them synchronously

        :param management_group_id:
        :param policy_definition_files:
        :return:
        """

        for policy_definition_file in policy_definition_files:
            with open(policy_definition_file['policy_definition_path']) as definition:
                try:
                    policy_definition_file_contents = json.load(definition)
                except:
                    print("Creation failed for ", policy_definition_file['policy_defintion_name'])
                    continue

                if 'name' in policy_definition_file_contents:
                    policyDefinitionName = policy_definition_file_contents['name']

                    if policyDefinitionName:
                        # policy_definition_file_contents = json.dumps(policy_definition_file_contents)
                        policy_definition_body = policy_definition_file_contents['properties']

                        policy_result = self.create_at_management_group_scope(
                            policy_definition_name=policyDefinitionName, policy_definition_body=policy_definition_body,
                            management_group_id=management_group_id)

    def create_at_management_group_scope(self,
                                         policy_definition_name,
                                         policy_definition_body,
                                         credentials=None,
                                         management_group_id=None,
                                         subscription_id=None,
                                         ):

        """
        This method has the benefit of specifying the the internal name of the policy. The policy_definition_name given
        in this method will set the unique name for the Azure Tenant.  Creating a policy this way offers more control, but
        can also yield name collisions.  If a policy with the same internal name is found, this method WILL OVERWRITE that
        policy.

        :param policy_definition_name:
        :param policy_definition_body:
        :param credentials:
        :param management_group_id:
        :param subscription_id:
        :return:
        """

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

        policy_definition = policy_client.policy_definitions.create_or_update_at_management_group(
            policy_definition_name=policy_definition_name, parameters=policy_definition_body,
            management_group_id=management_group_id)

        return policy_definition

    def delete(self):
        raise NotImplementedError

    def batch_create(self):
        raise NotImplementedError
