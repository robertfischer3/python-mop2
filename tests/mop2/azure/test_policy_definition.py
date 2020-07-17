from unittest import TestCase
from mop2.comprehension.azure.resource_manager.policy_definition import PolicyDefinition

class TestPolicyDefinition(TestCase):
    def test_get(self):
        policy_definition = PolicyDefinition()
        assert policy_definition.get()

    def test_list(self):
        policy_definition = PolicyDefinition()
        assert policy_definition.list()

    def test_create(self):
        policy_definition = PolicyDefinition()
        assert policy_definition.create()

    def test_delete(self):
        policy_definition = PolicyDefinition()
        assert policy_definition.delete()

    def test_batch_create(self):
        policy_definition = PolicyDefinition()
        assert policy_definition.batch_create()

