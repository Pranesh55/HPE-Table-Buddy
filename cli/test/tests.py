import sys
# Hack to get the correct path working
sys.path.append("/cli/")
import unittest
import subprocess
import logging

LOG = logging.getLogger(__name__)

class InvalidArgTest(unittest.TestCase):
    def setUp(self):
       pass
    
    def test_invalid_arg(self):
        result = subprocess.check_output(["tablebuddy", "teacher", "--generate"], shell=True)
        self.assertEqual(result, b"Invalid arguments\r\n")

    def student_std_sec(self):
        result = subprocess.check_output(["tablebuddy", "student", "--standard", "X","--sec","C"], shell=True)
        print(result)
         