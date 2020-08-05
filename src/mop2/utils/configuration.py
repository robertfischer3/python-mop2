from configparser import ConfigParser
from contextlib import contextmanager
import os

from dotenv import load_dotenv

from mop2.utils.atomic_writes import atomic_write
from mop2.utils.files import change_dir

CONFVARIABLES = "app.config.ini"
OPERATIONSPATH = "../../../data"
TESTVARIABLES = "test.app.config.ini"
TESTINGPATH = "../../../data"


def create_baseline_configuration(configuration_file):
    """
        The method creates the api configuration file for Azure API calls.  As Microsoft changes the API, the
        methods can change with the API by altering the signatures in this generated method or in the resulting
        configuration files.

    :return:
    """
    load_dotenv()
    config = ConfigParser()
    # AZURE_SUBSCRIPTION_ID, AZURE_TENANT_ID, etc attempt to align with environment variable names found in most
    # Microsoft Examples.

    config["DEFAULT"] = {
        "subscription_id": os.environ["AZURE_SUBSCRIPTION_ID"],
        "management_grp_id": os.environ["AZURE_MANAGEMENT_GROUP_ID"],
        "tenant_id": os.environ["AZURE_TENANT_ID"],
        "organization": os.environ["ORGANIZATION"],
        # Migrating OS evironment variables to Microsoft common naming standards for MS related technologies only
        "AZURE_SUBSCRIPTION_ID": os.environ["AZURE_SUBSCRIPTION_ID"],
        "AZURE_MANAGEMENT_GROUP_ID": os.environ["AZURE_MANAGEMENT_GROUP_ID"],
        "AZURE_TENANT_ID": os.environ["AZURE_TENANT_ID"],
        "plugin_root_path": "src/mop/azure/plugins/",
        "activeDirectoryEndpointUrl": "https://login.microsoftonline.com",
        "resourceManagerEndpointUrl": "https://management.azure.com/",
        "activeDirectoryGraphResourceId": "https://graph.windows.net/",
        "sqlManagementEndpointUrl": "https://management.core.windows.net:8443/",
        "galleryEndpointUrl": "https://gallery.azure.com/",
        "managementEndpointUrl": "https://management.core.windows.net/",
        "scope": "User.ReadBasic.All",
        "test_data_file": "test_data.ini",
    }
    """
    The configuration file supports multiple database instances
    """
    config["SQLSERVER"] = {
        "instance01": {
            "server": "tcp:172.17.0.1",
            "database": "sqlmopbucket",
            "username": "robert",
            "db_driver": "{ODBC Driver 17 for SQL Server}",
            "dialect": "mssql",
        }
    }

    config["LOG_ANALYTICS"] = {
        "instance01": {"workspace_id": os.environ["LOG_ANALYTICS_WORKSPACE_ID"]}
    }

    config["FILTERS"] = {
        "policy_definition_category": "Security",
        "policy_definition_name_01": "",
    }
    config["LOGGING"] = {"level": "10"}
    config["AZURESDK"] = {
        "management_group_scope_policy_assignment": "/providers/Microsoft.Management/managementGroups/{managementGroup}"
    }
    config["PRISMACLOUD"] = {
        "api2_eu_login": "https://api2.eu.prismacloud.io/login",
        "api2_eu": "https://api2.eu.prismacloud.io",
        "policy": "{cloud_api}/policy",
        "compliance": "{cloud_api}/compliance",
        "filter_policy_suggest": "{cloud_api}/filter/policy/suggest",
    }

    config["COSMOSDB"] = {"URI_01": os.environ["COSMODB_URI"]}

    config["PLUGINS"] = {
        "plugin_python_policies": "pypolicy/glbl_pr_sec*.py",
        "plugin_database": "test_db_plugin",
    }
    config["GIT"] = {
        "azure_project_01": "testproject",
        "azure_repository_id_01": "b3e721c7-0a2a-4712-b37a-2df3ce32f4cf",
        "azure_repository_name_01": "testrepo",
        "azure_scope_path_01": "/cloud/azure/policy/security",
        "azure_devops_organization_url": "",
        "azure_devops_repositories_list": "https://dev.azure.com/{organization}/{project}/_apis/git/repositories?api-version=5.1",
        "azure_devops_repository_get": "https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{repositoryId}?api-version=5.1",
        "azure_devops_refs_list": "https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{repositoryId}/refs?filter=heads/&filterContains={filterValue}&api-version=5.1",
        "azure_devops_items_list": "https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{repositoryId}/items?scopePath={scopePath}&recursionLevel={recursionLevel}&includeLinks={includeLinks}&versionDescriptor.version={versionDescriptor_version}&api-version=5.1",
    }

    with atomic_write(configuration_file, "w") as configfile:
        config.write(configfile)


def main():
    with change_dir(OPERATIONSPATH):
        create_baseline_configuration(CONFVARIABLES)

    with change_dir(TESTINGPATH):
        create_baseline_configuration(TESTVARIABLES)


if __name__ == "__main__":
    main()
