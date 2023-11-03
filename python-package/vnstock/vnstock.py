import pandas as pd
import requests

class VNStockData:
    HEADERS = {
        'content-type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla'
    }

    def __init__(self):
        self.base_url = "https://finfo-api.vndirect.com.vn/v4/stock_prices/"

    def get_data(self, tickers, size=100):
        """
        Retrieves historical stock data from the VNDIRECT API for multiple tickers.

        :param tickers: A list of stock symbols.
        :param size: Length of historical data.
        :return: A DataFrame containing historical stock data for all tickers.
        """

        # Check if tickers and size are valid
        if not tickers:
            raise ValueError("tickers is not set")

        if size <= 0:
            raise ValueError("size must be > 0")

        # Initialize an empty DataFrame to store the results
        df = pd.DataFrame()

        for ticker in tickers:
            # Check if the ticker is valid
            if not isinstance(ticker, str) or len(ticker) != 3:
                raise ValueError(f"Invalid ticker: {ticker}")

            # Define the endpoint for each ticker
            endpoint = f"code:{ticker}"
            print(endpoint)

            # Set query parameters, including the HEADERS
            params = {
                "sort": "date",
                "size": size,
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

        return df

    def ohlcv(self, tickers, size=100):
        df = self.get_data(tickers=tickers, size=size)
        ohlcv_df = df[['date', 'open', 'high', 'low', 'close', 'adClose', 'nmVolume']]
        ohlcv_df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
        ohlcv_df.index = pd.to_datetime(ohlcv_df['Date'])
        return ohlcv_df