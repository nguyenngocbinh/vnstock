import pandas as pd
import requests

# Define the HEADERS dictionary
HEADERS = {
    'content-type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla'
}

def get_data(tickers, size=100):
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

    # Define the base URL
    base = "https://finfo-api.vndirect.com.vn/v4/stock_prices/"

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
        res = requests.get(base, params=params, headers=HEADERS)

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


import pandas as pd

def ohlcv(df):
    """
    Calculate OHLCV (Open, High, Low, Close, and Volume) from a DataFrame of stock prices.

    :param df: A DataFrame containing stock price data with columns ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'].
    :return: A DataFrame containing OHLCV data with 'Date' as the index.
    """
    ohlcv_df = df[['date', 'open', 'high', 'low', 'close', 'adClose', 'nmVolume']]
    ohlcv_df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    ohlcv_df.index = pd.to_datetime(ohlcv_df['Date'])
    return ohlcv_df

