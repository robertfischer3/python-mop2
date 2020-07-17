from unittest import TestCase
from mop2.broken.brokenpipe import BrokenPipe

class TestBrokenPipe(TestCase):

    def test_leak(self):
        bp = BrokenPipe()
        leaks = bp.leak("Bob was here")
        self.assertIsNotNone(leaks)

    def test_dictionary(self):
        my_dict = {"properties":"vacation home"}

        if "properties" in my_dict:
            value = my_dict['properties']
            print(value)
        else:
            print("Bye")

