import unittest
from alexa_tools.json_intent_to_constant import intent_samples_to_comment, intent_name_to_constant


class TestJsonIntentToPython(unittest.TestCase):
    def test_get_sample_as_comment__no_sample(self):
        samples = []  # No sample attaches to intent
        result = intent_samples_to_comment(samples)

        expected = '# Samples phrases : '

        self.assertEqual(expected, result)

    def test_get_sample_as_comment__one_sample(self):
        samples = ['test']  # No sample attaches to intent
        result = intent_samples_to_comment(samples)

        expected = "# Samples phrases : 'test'"

        self.assertEqual(expected, result)

    def test_get_sample_as_comment__multiple_samples(self):
        samples = ['test one', 'test two', 'test three']  # No sample attaches to intent
        result = intent_samples_to_comment(samples)

        expected = "# Samples phrases : 'test one', 'test two', 'test three'"

        self.assertEqual(expected, result)

    def test_intent_name_to_constant__custom_intent(self):
        intent_name = 'StartSpeedDateIntent'
        result = intent_name_to_constant(intent_name)

        expected = "START_SPEED_DATE = 'StartSpeedDateIntent'"

        self.assertEqual(expected, result)

    def test_intent_name_to_constant__amazon_intent(self):
        intent_name = 'AMAZON.StopIntent'
        result = intent_name_to_constant(intent_name)

        expected = "STOP = 'AMAZON.StopIntent'"

        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
