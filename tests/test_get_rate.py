import unittest
from unittest.mock import patch
from fixercise.get_rates import get_current_rates

import tests.testutils as testutils


class TestGetRates(unittest.TestCase):

    @patch('fixercise.get_rates.requests.get')
    def test_get_rates_happy(self, mock_response):
        """Check a response with status 200 and body returns happily."""
        mock_response.return_value = testutils.mock_api_response(200)
        response = get_current_rates()
        self.assertEqual(200,
                         response.status_code,
                         "Happy status code comes back 200")

        self.assertTrue(response.json(), "Happy response has a body")

    def test_get_rates_bad_api_call(self, mock_response):
        pass

    def test_get_rates_bad_status(self, mock_response):
        pass

if __name__ == '__main__':
    unittest.main()