import unittest
from unittest.mock import patch

import calculate


FAKE_URL = 'http://localhost:8001/file.csv'
TEST_DATA = '''id,some_date,some_bool,tip_amount,some_int
1,2018-01-01 00:00:00,Y,6.99,10
1,2018-01-01 00:00:00,Y,-3.0,10
1,2018-01-01 00:00:00,Y,0.0,10
1,2018-01-01 00:00:00,Y,1.99,10
'''


class CalculateAverageTest(unittest.TestCase):
    @patch('calculate.urlopen')
    def test_calculate_average(self, urlopen_mock):
        mock_response = urlopen_mock.return_value
        mock_context_manager = mock_response.__enter__.return_value
        mock_context_manager.read.side_effect = [TEST_DATA.encode('ascii'), None]

        expected_result = 5, 1.495,
        result = calculate.calculate_average(FAKE_URL, 'tip_amount')

        urlopen_mock.assert_called_once_with(FAKE_URL)
        self.assertEqual(result, expected_result)
