import os
import unittest

class PlaceholderTest(unittest.TestCase):
    def test(self):
        self.assertTrue(os.path.isfile('../profile.yaml'))

if __name__ == '__main__':
    unittest.main()