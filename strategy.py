import yfinance as yf

tickers = ["QQQ", "SPY", "XEQT.TO"]

results = []

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

    score = ((current_price - moving_average) / moving_average) * 100

    results.append({
        "ticker": ticker,
        "price": current_price,
        "ma50": moving_average,
        "signal": signal,
        "score": score
    })

results.sort(key=lambda x: x["score"], reverse=True)

report = "\nAI COMPOUND BOT REPORT\n\n"

for r in results:
    report += (
        f"{r['ticker']}\n"
        f"Price: ${r['price']:.2f}\n"
        f"50-Day Avg: ${r['ma50']:.2f}\n"
        f"Signal: {r['signal']}\n"
        f"Score: {r['score']:.2f}%\n\n"
    )

report += f"TOP PICK: {results[0]['ticker']}\n"

print(report)

with open("report.txt", "w") as f:
    f.write(report)
