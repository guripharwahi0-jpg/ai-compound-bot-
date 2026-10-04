import yfinance as yf

tickers = ["QQQ", "SPY", "XEQT.TO"]

print("\nAI Compound Bot\n")

for ticker in tickers:

    data = yf.download(
        ticker,
        period="3mo",
        auto_adjust=True,
        progress=False
    )

    close_prices = data["Close"].squeeze()

    current_price = close_prices.iloc[-1]
    moving_average = close_prices.tail(50).mean()

    signal = "BUY/HOLD" if current_price > moving_average else "SELL"

    print(f"\n{ticker}")
    print(f"Current Price: ${current_price:.2f}")
    print(f"50-Day Average: ${moving_average:.2f}")
    print(f"Signal: {signal}")
    print("-" * 30)
