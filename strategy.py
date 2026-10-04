import yfinance as yf
import pandas as pd

portfolio = pd.read_csv("portfolio.csv")

with open("cash.txt", "r") as f:
    cash = float(f.read().strip())

report = []
rankings = []

total_value = cash

report.append("AI COMPOUND BOT REPORT\n")
report.append(f"Cash Available: ${cash:.2f}\n")

for _, row in portfolio.iterrows():

    ticker = row["ticker"]
    shares = row["shares"]
    buy_price = row["buy_price"]

    data = yf.download(
        ticker,
        period="3mo",
        auto_adjust=True,
        progress=False
    )

    close_prices = data["Close"].squeeze()

    current_price = float(close_prices.iloc[-1])

    ma50 = float(close_prices.tail(50).mean())

    score = ((current_price - ma50) / ma50) * 100

    signal = "BUY/HOLD" if current_price > ma50 else "SELL"

    value = shares * current_price

    gain_percent = (
        (current_price - buy_price)
        / buy_price
    ) * 100

    total_value += value

    rankings.append({
        "ticker": ticker,
        "score": score,
        "signal": signal
    })

    report.append(
        f"{ticker}\n"
        f"Shares: {shares}\n"
        f"Current Price: ${current_price:.2f}\n"
        f"50-Day Avg: ${ma50:.2f}\n"
        f"Signal: {signal}\n"
        f"Gain/Loss: {gain_percent:.2f}%\n"
    )

rankings.sort(
    key=lambda x: x["score"],
    reverse=True
)

top_pick = rankings[0]["ticker"]

report.append("\n==========")
report.append("TRADE RECOMMENDATIONS")
report.append("==========\n")

for item in rankings:

    if item["signal"] == "SELL":

        report.append(
 
