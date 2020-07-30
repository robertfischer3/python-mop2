import os
from azure.mgmt.resource import PolicyClient
from azure.common.credentials import ServicePrincipalCredentials


class Identity:
    def __init__(self, **kwargs):
        if "subscription_id" in kwargs:
            self.subscription_id = kwargs["subscription_id"]
        if "tenant_id" in kwargs:
            self.tenant_id = kwargs["tenant_id"]
        if "client_id" in kwargs:
            self.client_id = kwargs["client_id"]
        if "client_secret" in kwargs:
            self.__client_secret = kwargs["client_secret"]

    def get_service_principal_credential(self, **kwargs):
        credential = ServicePrincipalCredentials(
            tenant=self.tenant_id, client_id=self.client_id, secret=self.__client_secret
        )
