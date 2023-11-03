import pandas as pd

def format_up_down_percent(val):
    color = 'red' if val < 0 else 'green'
    return f'color: {color}'

def format_milion(val):
    return f"${val:.1f}M"

def format_thousand(val):
    return f"${val:.1f}K"

def format_df(returns_data):
    returns_data = returns_data.copy()
    # Rename columns
    returns_data.rename(columns={"1d": "1d%", "1w": "1w%", "1m": "1m%", "6m": "6m%"}, inplace=True)
    returns_data['Volume'] = (returns_data['Volume'] / 1e6).apply(format_milion)
    returns_data['Price'] = (returns_data['Adj Close']).apply(format_thousand)
    returns_data = returns_data.groupby('Symbol').tail(1)
    returns_data = returns_data[['Price', 'Volume', '1d%', "1w%", "1m%", "6m%"]]

    # Apply styling to the specified columns
    styled_df = returns_data.style.applymap(format_up_down_percent, subset=pd.IndexSlice[:, ['1d%', "1w%", "1m%", "6m%"]])
    styled_df.format(subset=pd.IndexSlice[:, ['1d%', "1w%", "1m%", "6m%"]], formatter="{:.2%}")

    return styled_df