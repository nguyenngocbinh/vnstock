import pandas as pd
import requests

class VNStockData:
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

    def get_data(self):
        """
        Retrieves historical stock data from the VNDIRECT API for multiple tickers.

        :param tickers: A list of stock symbols.
        :param size: Length of historical data.
        :return: A DataFrame containing historical stock data for all tickers.
        """

        # Check if tickers and size are valid
        if not self.tickers:
            raise ValueError("tickers is not set")

        if self.size <= 0:
            raise ValueError("size must be > 0")

        # Initialize an empty DataFrame to store the results
        df = pd.DataFrame()

        for ticker in self.tickers:
            # Check if the ticker is valid
            if not isinstance(ticker, str) or len(ticker) != 3:
                raise ValueError(f"Invalid ticker: {ticker}")

            # Define the endpoint for each ticker
            endpoint = f"code:{ticker}"
            print(f"Retrieving data for ticker: {ticker}")
 
            # Set query parameters, including the HEADERS
            params = {
                "sort": "date",
                "size": self.size,
                "page": 1,
                "q": endpoint,
            }

            # Send the HTTP request with the HEADERS
            res = requests.get(self.base_url, params=params, headers=self.HEADERS)

            # Check if the HTTP request was successful
            if res.status_code != 200:
                print(f"Failed to retrieve data for ticker: {ticker}")
                continue  # Skip to the next ticker on error

            # Extract and process the data
            data = res.json().get("data", [])

            # Convert to a DataFrame
            if data:
                df_ticker = pd.DataFrame(data)
                df_ticker["date"] = pd.to_datetime(df_ticker["date"])
                df = pd.concat([df, df_ticker], ignore_index=True)
            else:
                print(f"No data available for ticker: {ticker}")

            self.raw_data = df            
        return self.raw_data

    def ohlcv(self):
        ohlcv_df = self.raw_data[['date', 'code', 'open', 'high', 'low', 'close', 'adClose', 'nmVolume']]
        ohlcv_df.columns = ['Date', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
        ohlcv_df.set_index(['Symbol', 'Date'], inplace = True)
        self.ohlcv_df = ohlcv_df
        return self.ohlcv_df
    
    def resample(self, rule, col_list=None):
        """
        Resamples the OHLCV data based on the specified rule.

        :param rule: The resampling rule (e.g., 'M' for monthly, 'W' for weekly).
        :param col_list: List of columns to resample. Default is None (resample all columns).
        :return: A DataFrame containing the resampled data.
        """
        if col_list is None:
            col_list = self.ohlcv_df.columns

        # Group by 'Symbol' and apply resampling to the specified columns
        resampled_data = self.ohlcv_df.groupby('Symbol')[col_list].resample(rule).last()
        return resampled_data
    
    def calculate_returns(self):
        """
        Calculate returns for yesterday, last week, last month and last 6 month grouped by Symbol.

        :return: DataFrame containing returns for yesterday, last week, last month and last 6 month grouped by Symbol.
        """
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