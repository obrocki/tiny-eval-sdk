import unittest
from cloud_evaluation_sdk.utils import load_config, format_response

class TestUtils(unittest.TestCase):

    def test_load_config(self):
        config = load_config('config.yaml')
        self.assertIsInstance(config, dict)
        self.assertIn('key', config)

    def test_format_response(self):
        response = {'status': 'success', 'data': {'value': 42}}
        formatted = format_response(response)
        self.assertEqual(formatted, 'Status: success, Data: 42')

if __name__ == '__main__':
    unittest.main()