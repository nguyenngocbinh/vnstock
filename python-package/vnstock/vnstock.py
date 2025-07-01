import pandas as pd
import requests
import logging

class VNStockData:
    """
    Class for retrieving and processing stock data from the VNDIRECT API.
    """
    HEADERS = {
        'content-type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla'
    }

    def __init__(self, tickers, size=125):
        self.base_url = "https://finfo-api.vndirect.com.vn/v4/stock_prices/"
        self.tickers = tickers
        self.size = size
        self.raw_data = None
        self.ohlcv_df = None
        self.returns_data = None
        logging.basicConfig(level=logging.INFO)

    def get_data(self):
        """
        Retrieves historical stock data from the VNDIRECT API for multiple tickers.
        :return: A DataFrame containing historical stock data for all tickers.
        """
        if not self.tickers:
            raise ValueError("tickers is not set")
        if self.size <= 0:
            raise ValueError("size must be > 0")
        df = pd.DataFrame()
        for ticker in self.tickers:
            if not isinstance(ticker, str) or not ticker:
                logging.warning(f"Invalid ticker: {ticker}")
                continue
            endpoint = f"code:{ticker}"
            logging.info(f"Retrieving data for ticker: {ticker}")
            params = {
                "sort": "date",
                "size": self.size,
                "page": 1,
                "q": endpoint,
            }
            try:
                res = requests.get(self.base_url, params=params, headers=self.HEADERS)
                if res.status_code != 200:
                    logging.warning(f"Failed to retrieve data for ticker: {ticker}")
                    continue
                data = res.json().get("data", [])
                if data:
                    df_ticker = pd.DataFrame(data)
                    if 'date' in df_ticker:
                        df_ticker["date"] = pd.to_datetime(df_ticker["date"])
                    df = pd.concat([df, df_ticker], ignore_index=True)
                else:
                    logging.info(f"No data available for ticker: {ticker}")
            except Exception as e:
                logging.error(f"Error retrieving data for ticker {ticker}: {e}")
                continue
        self.raw_data = df
        return self.raw_data

    def ohlcv(self):
        """
        Extracts OHLCV data from the raw data.
        :return: DataFrame with OHLCV columns.
        """
        if self.raw_data is None:
            raise ValueError("raw_data is not set. Please call get_data() first.")
        required_cols = ['date', 'code', 'open', 'high', 'low', 'close', 'adClose', 'nmVolume']
        for col in required_cols:
            if col not in self.raw_data.columns:
                raise ValueError(f"Missing column: {col}")
        ohlcv_df = self.raw_data[required_cols]
        ohlcv_df.columns = ['Date', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
        ohlcv_df.set_index(['Symbol', 'Date'], inplace=True)
        self.ohlcv_df = ohlcv_df
        return self.ohlcv_df

    def resample(self, rule, col_list=None):
        """
        Resamples the OHLCV data based on the specified rule.
        :param rule: The resampling rule (e.g., 'M' for monthly, 'W' for weekly).
        :param col_list: List of columns to resample. Default is None (resample all columns).
        :return: A DataFrame containing the resampled data.
        """
        if self.ohlcv_df is None:
            raise ValueError("ohlcv_df is not set. Please call ohlcv() first.")
        if col_list is None:
            col_list = self.ohlcv_df.columns
        resampled_data = self.ohlcv_df.groupby('Symbol')[col_list].resample(rule).last()
        return resampled_data

    def calculate_returns(self):
        """
        Calculate returns for yesterday, last week, last month and last 6 month grouped by Symbol.
        :return: DataFrame containing returns for yesterday, last week, last month and last 6 month grouped by Symbol.
        """
        if self.ohlcv_df is None:
            raise ValueError("ohlcv_df is not set. Please call ohlcv() first.")
        returns_data = self.ohlcv_df.copy()
        returns_data.sort_index(inplace=True)
        # Calculate returns for yesterday
        returns_data['1d'] = returns_data.groupby('Symbol')['Adj Close'].pct_change()
        # Calculate returns for last week
        returns_data['1w'] = returns_data.groupby('Symbol')['Adj Close'].pct_change(periods=5)
        # Calculate returns for last month
        returns_data['1m'] = returns_data.groupby('Symbol')['Adj Close'].pct_change(periods=20)
        # Calculate returns for last 6 month
        returns_data['6m'] = returns_data.groupby('Symbol')['Adj Close'].pct_change(periods=120)
        self.returns_data = returns_data
        return self.returns_data