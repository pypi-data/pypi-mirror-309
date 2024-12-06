import unittest
from crdclib import cleanString


class TestCleanString(unittest.TestCase):


    def test_fullClean(self):
        teststring = "This is # Test\t\r\n!@#$%^&*()"
        self.assertEqual(cleanString(teststring), "ThisisTest")
        self.assertEqual(cleanString(teststring, False), "ThisisTest")
        self.assertEqual(cleanString(teststring, True), "This is # Test!@#$%^&*()")

if __name__ == "__main__":

    unittest.main(verbosity=2)
