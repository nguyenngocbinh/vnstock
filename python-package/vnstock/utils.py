import pandas as pd

def format_up_down_percent(val):
    color = 'red' if val < 0 else 'green'
    return f'color: {color}'

def format_million(val):
    return f"${val:.1f}M"

def format_thousand(val):
    return f"${val:.1f}K"

def transform_returns_df(returns_data):
    required_columns = {"Volume", "Adj Close", "Symbol"}
    missing = required_columns - set(returns_data.columns)
    if missing:
        raise ValueError(f"Missing columns in DataFrame: {missing}")
    df = returns_data.copy()
    df.rename(columns={"1d": "1d%", "1w": "1w%", "1m": "1m%", "6m": "6m%"}, inplace=True)
    df['Volume'] = (df['Volume'] / 1e6).apply(format_million)
    df['Price'] = (df['Adj Close']).apply(format_thousand)
    df = df.groupby('Symbol').tail(1)
    df = df[['Price', 'Volume', '1d%', "1w%", "1m%", "6m%"]]
    return df

def style_returns_df(df):
    percent_cols = ['1d%', "1w%", "1m%", "6m%"]
    for col in percent_cols:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")
    styled_df = df.style.applymap(format_up_down_percent, subset=pd.IndexSlice[:, percent_cols])
    styled_df.format(subset=pd.IndexSlice[:, percent_cols], formatter="{:.2%}")
    return styled_df