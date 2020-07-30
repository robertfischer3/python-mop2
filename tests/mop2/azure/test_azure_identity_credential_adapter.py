# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
import pytest
from unittest import TestCase
import os
from dotenv import load_dotenv
from mop2.comprehension.azure.identity.azure_identity_credential_adapter import AzureIdentityCredentialAdapter

class TestAzureIdentityCredentialAdapterTestCase(TestCase):
    def setUp(self) -> None:
        load_dotenv()
        self.subscription_id = os.environ["SUB"]
    def test_list_resource_group(self):

        subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")

        credentials = AzureIdentityCredentialAdapter()

        from azure.mgmt.resource import ResourceManagementClient
        client = ResourceManagementClient(credentials, self.subscription_id)
        # Not raising any exception means we were able to do it
        rg_list = list(client.resource_groups.list())
        self.assertGreater(len(rg_list), 0)
        print(rg_list)