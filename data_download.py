import yfinance as yf

symbols = [
    "AAPL",
    "MSFT",
    "GOOG",
    "AMZN",
    "SPY"
]

for symbol in symbols:

    data = yf.download(
        symbol,
        start="2023-01-01",
        end="2024-01-01",
        auto_adjust=False
    )
 
    # IMPORTANT FIX
    data.columns = data.columns.get_level_values(0)

    data.reset_index(inplace=True) 

    data.to_csv(
        f"data/{symbol}_data.csv",
        index=False
    )

    print(f"{symbol} downloaded successfully")