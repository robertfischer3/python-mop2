import os
from dotenv import load_dotenv

from azure.common.client_factory import get_client_from_json_dict
from azure.mgmt.resource.policy import PolicyClient

from unittest import TestCase

# Retrieve the IDs and secret to use in the JSON dictionary

class TestIdentity(TestCase):
    def setUp(self) -> None:
        load_dotenv()
        subscription_id = os.environ["SUB"]
        tenant_id = os.environ["TENANT"]
        client_id = os.environ["CLIENT"]
        client_secret = os.environ["KEY"]

        self.config_dict = {
           "subscriptionId": subscription_id,
            "tenantId": tenant_id,
           "clientId": client_id,
           "clientSecret": client_secret,
           "activeDirectoryEndpointUrl": "https://login.microsoftonline.com",
           "resourceManagerEndpointUrl": "https://management.azure.com/",
           "activeDirectoryGraphResourceId": "https://graph.windows.net/",
           "sqlManagementEndpointUrl": "https://management.core.windows.net:8443/",
           "galleryEndpointUrl": "https://gallery.azure.com/",
           "managementEndpointUrl": "https://management.core.windows.net/"
        }

    def test_policy_client_with_spn(self):
        policy_client = get_client_from_json_dict(PolicyClient, self.config_dict)
        print(policy_client)


