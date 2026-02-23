import unittest
import pandas as pd
from vnstock import utils

class TestUtils(unittest.TestCase):
    def test_format_up_down_percent(self):
        self.assertEqual(utils.format_up_down_percent(-1), 'color: red')
        self.assertEqual(utils.format_up_down_percent(1), 'color: green')

    def test_format_up_down_percent_zero(self):
        self.assertEqual(utils.format_up_down_percent(0), 'color: green')

    def test_format_million(self):
        self.assertEqual(utils.format_million(2.5), "$2.5M")

    def test_format_thousand(self):
        self.assertEqual(utils.format_thousand(3.2), "$3.2K")

    def test_transform_returns_df_missing_columns(self):
        df = pd.DataFrame({'Volume': [1], 'Adj Close': [2]})
        with self.assertRaises(ValueError):
            utils.transform_returns_df(df)

    def test_transform_returns_df_success(self):
        df = pd.DataFrame({
            'Volume': [1000000],
            'Adj Close': [50.0],
            'Symbol': ['AAA'],
            '1d': [0.01], '1w': [0.02], '1m': [0.05], '6m': [0.10],
        })
        result = utils.transform_returns_df(df)
        self.assertIn('Price', result.columns)
        self.assertIn('Volume', result.columns)
        self.assertIn('1d%', result.columns)

    def test_style_returns_df_missing_column(self):
        df = pd.DataFrame({'Price': [1]})
        with self.assertRaises(ValueError):
            utils.style_returns_df(df)

if __name__ == '__main__':
    unittest.main() 