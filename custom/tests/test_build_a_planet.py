import unittest


class IntegrationTests(unittest.TestCase):
    def test__dummy(self):
        self.assertEqual(True, True, 'True should be True')


if __name__ == '__main__':
    unittest.main()
