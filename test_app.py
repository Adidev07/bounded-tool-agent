import unittest
from app import *
class DomainTests(unittest.TestCase):
    def test_arithmetic(self):self.assertEqual(calculate('(12+3)*2'),30)
    def test_no_code_execution(self):
        with self.assertRaises(ValueError):calculate('__import__("os")')
    def test_tool_budget(self):
        with self.assertRaises(ValueError):execute([{'tool':'calculator','argument':'1'}]*5,[])
    def test_unknown_tool(self):
        with self.assertRaises(ValueError):execute([{'tool':'shell','argument':'whoami'}],[])
