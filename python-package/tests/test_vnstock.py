import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from vnstock.vnstock import VNStockData

class TestVNStockData(unittest.TestCase):
    def test_init(self):
        tickers = ['AAA', 'BBB']
        vns = VNStockData(tickers)
        self.assertEqual(vns.tickers, tickers)
        self.assertEqual(vns.size, 125)

    def test_init_custom_size(self):
        vns = VNStockData(['AAA'], size=50)
        self.assertEqual(vns.size, 50)

    def test_get_data_invalid_tickers(self):
        vns = VNStockData([])
        with self.assertRaises(ValueError):
            vns.get_data()
        vns = VNStockData([''])
        # Should not raise, but will skip invalid ticker
        vns.size = 1
        vns.get_data()

    def test_get_data_invalid_size(self):
        vns = VNStockData(['AAA'])
        vns.size = 0
        with self.assertRaises(ValueError):
            vns.get_data()

    @patch('vnstock.vnstock.requests.get')
    def test_get_data_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"date": "2024-01-01", "code": "AAA", "open": 10, "high": 12,
                 "low": 9, "close": 11, "adClose": 11, "nmVolume": 1000}
            ]
        }
        mock_get.return_value = mock_response
        vns = VNStockData(['AAA'], size=1)
        df = vns.get_data()
        self.assertFalse(df.empty)
        self.assertIn('code', df.columns)
        mock_get.assert_called_once()
        # Verify timeout is passed
        _, kwargs = mock_get.call_args
        self.assertEqual(kwargs['timeout'], VNStockData.DEFAULT_TIMEOUT)

    @patch('vnstock.vnstock.requests.get')
    def test_get_data_non_200(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response
        vns = VNStockData(['AAA'], size=1)
        df = vns.get_data()
        self.assertTrue(df.empty)

    @patch('vnstock.vnstock.requests.get')
    def test_get_data_request_exception(self, mock_get):
        import requests
        mock_get.side_effect = requests.RequestException("timeout")
        vns = VNStockData(['AAA'], size=1)
        df = vns.get_data()
        self.assertTrue(df.empty)

    def test_ohlcv_before_get_data(self):
        vns = VNStockData(['AAA'])
        with self.assertRaises(ValueError):
            vns.ohlcv()

    def test_ohlcv_missing_column(self):
        vns = VNStockData(['AAA'])
        vns.raw_data = pd.DataFrame({'date': ['2024-01-01'], 'code': ['AAA']})
        with self.assertRaises(ValueError):
            vns.ohlcv()

    def test_ohlcv_success(self):
        vns = VNStockData(['AAA'])
        vns.raw_data = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-01']),
            'code': ['AAA'],
            'open': [10], 'high': [12], 'low': [9],
            'close': [11], 'adClose': [11], 'nmVolume': [1000],
        })
        ohlcv = vns.ohlcv()
        self.assertIn('Open', ohlcv.columns)
        self.assertIn('Volume', ohlcv.columns)
        self.assertEqual(ohlcv.index.names, ['Symbol', 'Date'])

    def test_resample_before_ohlcv(self):
        vns = VNStockData(['AAA'])
        with self.assertRaises(ValueError):
            vns.resample('M')

    def test_calculate_returns_before_ohlcv(self):
        vns = VNStockData(['AAA'])
        with self.assertRaises(ValueError):
            vns.calculate_returns()

if __name__ == '__main__':
    unittest.main() 