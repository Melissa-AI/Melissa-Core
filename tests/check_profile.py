import os
import unittest


class PlaceholderTest(unittest.TestCase):

    def test(self):
        self.assertFalse(os.path.isfile('profile.json'))

if __name__ == '__main__':
    unittest.main()
