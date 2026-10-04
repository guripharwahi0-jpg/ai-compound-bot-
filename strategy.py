import yfinance as yf
import pandas as pd

portfolio = pd.read_csv("portfolio.csv")

with open("cash.txt", "r") as f:
    cash = float(f.read().strip())

report = []
total_value = cash

report.append("AI COMPOUND BOT REPORT\n")
report.append(f"Cash: ${cash:.2f}\n")

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
    value = shares * current_price

    gain_percent = (
        (current_price - buy_price)
        / buy_price
    ) * 100

    total_value += value

    report.append(
        f"{ticker}\n"
        f"Shares: {shares}\n"
        f"Buy Price: ${buy_price:.2f}\n"
        f"Current Price: ${current_price:.2f}\n"
        f"Position Value: ${value:.2f}\n"
        f"Gain/Loss: {gain_percent:.2f}%\n"
    )

starting_capital = 10000
profit = total_value - starting_capital

report.append(f"\nPortfolio Value: ${total_value:.2f}")
report.append(f"\nTotal Profit: ${profit:.2f}")

final_report = "\n".join(report)

print(final_report)

with open("report.txt", "w") as f:
    f.write(final_report)
