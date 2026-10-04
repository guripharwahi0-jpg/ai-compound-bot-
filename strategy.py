import yfinance as yf

tickers = ["QQQ", "SPY", "XEQT.TO"]

print("\nAI Compound Bot\n")

for ticker in tickers:
    data = yf.download(ticker, period="3mo", progress=False)

    current_price = data["Close"].iloc[-1]
    moving_average = data["Close"].tail(50).mean()

    if current_price > moving_average:
        signal = "BUY/HOLD"
    else:
        signal = "SELL"

    print(f"{ticker}")
    print(f"Current Price: {current_price:.2f}")
    print(f"50-Day Average: {moving_average:.2f}")
    print(f"Signal: {signal}")
    print("-" * 30)
