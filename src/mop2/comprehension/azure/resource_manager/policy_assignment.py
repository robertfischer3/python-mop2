from configparser import ConfigParser

import jmespath
import json

from azure.mgmt.resource import PolicyClient

from mop2.comprehension.azure.identity.azure_identity_credential_adapter import (
    AzureIdentityCredentialAdapter,
)
from mop2.utils.configuration import OPERATIONSPATH, CONFVARIABLES
from mop2.utils.files import change_dir
from mop2.comprehension.azure.resource_manager.policy_definition import (
    PolicyDefinition as MopPolicyDefinition,
)


class PolicyAssignment:
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

    def get(self):
        raise NotImplementedError

    def list(self):
        raise NotImplementedError

    def list_for_management_group(
        self,
        credentials=None,
        management_group_id=None,
        subscription_id=None,
        filter="atScope()",
    ):
        if credentials is None:
            credentials = AzureIdentityCredentialAdapter()

        if subscription_id is None:
            subscription_id = self.subscription_id
        #     Defaults to the root management group unless specified in the parameter list
        if management_group_id is None:
            management_group_id = self.management_group_id

        policy_client = PolicyClient(
            credentials=credentials, subscription_id=subscription_id
        )

        policy_assignments = list(
            policy_client.policy_assignments.list_for_management_group(
                management_group_id=management_group_id, filter=filter
            )
        )
        return policy_assignments

    def create_manage_group_assignment(
        self,
        policy_defintion_name,
        policy_assignment_name,
        credentials=None,
        management_group_id=None,
        subscription_id=None,
    ):
        """
        Create a policy assignment at the specified management group level
        :param policy_assignment_name:
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
            management_group_id = self.management_group_id

        policy_defintion_client = MopPolicyDefinition(
            operations_path=self.operations_path, config_variables=self.config_variables
        )
        policy_definition = policy_defintion_client.get_at_management_group(
            policy_definition_name=policy_defintion_name, raw=True
        )

        # Cannot assignment a policy for a policy that doesn't exist yet
        if not policy_definition:
            raise KeyError

        assignment_scope = self.config["AZURESDK"][
            "management_group_scope_policy_assignment"
        ]
        assignment_scope = assignment_scope.format(managementGroup=management_group_id)

        parameters = self.create_assignment_body(policy_definition)
        print(parameters)
        policy_client = PolicyClient(
            credentials=credentials, subscription_id=subscription_id
        )

        mgmnt_group_policy_assingment = policy_client.policy_assignments.create(
            scope=assignment_scope,
            policy_assignment_name=policy_assignment_name,
            parameters=parameters,
        )
        print(mgmnt_group_policy_assingment)

    def create_from_policy_defintion(self):
        credentials = None
        raise NotImplementedError

    def create_policy_assignment_parameters(self, policy_definition):

        description = policy_definition.description
        display_name = policy_definition.display_name
        parameters = policy_definition.parameters
        policy_name = policy_definition.name
        policy_id = policy_definition.id

        policy_assignment_request_body = {
            "properties": {
                "displayName": display_name,
                "description": description,
                "policyDefinitionId": policy_id,
                "parameters": parameters,
            }
        }

        return policy_assignment_request_body

    def create_assignment_body(self, policy_definition, metadata_category=None):

        if type(policy_definition) is dict:
            policy_definition_json = policy_definition
        elif type(policy_definition) is str:
            policy_definition_json = json.loads(policy_definition)
        elif (
            "ClientRawResponse" in str(type(policy_definition))
            and policy_definition.response.status_code == 200
        ):
            policy_definition_json = json.loads(policy_definition.response.text)
        else:
            return None

        if policy_definition_json["name"]:
            id = policy_definition_json["id"]
            displayName = policy_definition_json["name"]
            description = policy_definition_json["name"]
            createdBy = ""
            category = None
            parameters = {}

            if policy_definition_json["properties"]:
                if policy_definition_json["properties"]["displayName"]:
                    displayName = policy_definition_json["properties"]["displayName"]
                if "description" in policy_definition_json["properties"]:
                    description = policy_definition_json["properties"]["description"]
                else:
                    print("No decription, using policy name: {}".format(displayName))
                if "parameters" in policy_definition_json["properties"]:
                    parameter_dict = policy_definition_json["properties"]["parameters"]
                    defaultValues = jmespath.search(
                        "*.defaultValue", data=parameter_dict
                    )
                    for key in parameter_dict.keys():
                        if "defaultValue" in parameter_dict[key]:
                            value = parameter_dict[key]["defaultValue"]
                            parameters[key] = {"value": value}

                if policy_definition_json["properties"]["metadata"]:
                    createdBy = policy_definition_json["properties"]["metadata"][
                        "createdBy"
                    ]
                    if (
                        "metadata" in policy_definition_json["properties"]
                        and "category"
                        in policy_definition_json["properties"]["metadata"]
                    ):
                        category = policy_definition_json["properties"]["metadata"][
                            "category"
                        ]

                policy_assignment_request_body = {
                    "properties": {
                        "displayName": displayName,
                        "description": description,
                        "metadata": {"assignedBy": createdBy},
                        "policyDefinitionId": id,
                        "parameters": parameters,
                    }
                }
                if metadata_category:
                    policy_assignment_request_body["properties"]["metadata"][
                        "category"
                    ] = metadata_category

                if category:
                    policy_assignment_request_body["properties"]["metadata"][
                        "category"
                    ] = category

                return policy_assignment_request_body
