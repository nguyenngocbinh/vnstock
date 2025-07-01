import unittest
from vnstock.vnstock import VNStockData

class TestVNStockData(unittest.TestCase):
    def test_init(self):
        tickers = ['AAA', 'BBB']
        vns = VNStockData(tickers)
        self.assertEqual(vns.tickers, tickers)
        self.assertEqual(vns.size, 125)

    def test_get_data_invalid_tickers(self):
        vns = VNStockData([])
        with self.assertRaises(ValueError):
            vns.get_data()
        vns = VNStockData([''])
        # Should not raise, but will skip invalid ticker
        vns.size = 1
        vns.get_data()

if __name__ == '__main__':
    unittest.main() 