import yfinance as yf
import pandas as pd

from datetime import datetime
import os

portfolio = pd.read_csv("portfolio.csv")

history_file = "trade_history.csv"

if os.path.exists(history_file):
    history = pd.read_csv(history_file)
else:
    history = pd.DataFrame(
        columns=["date", "action", "ticker", "reason"]
    )

portfolio_history_file = "portfolio_history.csv"

if os.path.exists(portfolio_history_file):
    portfolio_history = pd.read_csv(
        portfolio_history_file
    )
else:
    portfolio_history = pd.DataFrame(
        columns=[
            "date",
            "portfolio_value",
            "cash",
            "profit"
        ]
    )

benchmark_file = "benchmark.csv"

if os.path.exists(benchmark_file):
    benchmark = pd.read_csv(benchmark_file)
else:
    benchmark = pd.DataFrame(
        columns=[
            "date",
            "qqq_price",
            "benchmark_value"
        ]
    )

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

today = datetime.now().strftime("%Y-%m-%d")

new_trade = pd.DataFrame([
    {
        "date": today,
        "action": "RECOMMEND_BUY",
        "ticker": top_pick,
        "reason": "Top ranked ETF"
    }
])

history = pd.concat(
    [history, new_trade],
    ignore_index=True
)

history.to_csv(
    history_file,
    index=False
)

report.append("\n==========")
report.append("TRADE RECOMMENDATIONS")
report.append("==========\n")

for item in rankings:

    if item["signal"] == "SELL":

        report.append(
            f"SELL {item['ticker']} "
            f"(below 50-day average)"
        )

report.append(
    f"TOP PICK FOR NEXT WEEK: {top_pick}"
)

report.append(
    f"BUY MORE OF: {top_pick}"
)

starting_capital = 10000

profit = total_value - starting_capital

qqq_data = yf.download(
    "QQQ",
    period="3mo",
    auto_adjust=True,
    progress=False
)

qqq_close = qqq_data["Close"].squeeze()

current_qqq_price = float(qqq_close.iloc[-1])

if len(benchmark) > 0:

    initial_price = benchmark.iloc[0]["qqq_price"]

else:

    initial_price = current_qqq_price

benchmark_value = (
    current_qqq_price
    / initial_price
) * 10000

benchmark_snapshot = pd.DataFrame([
    {
        "date": today,
        "qqq_price": round(current_qqq_price, 2),
        "benchmark_value": round(benchmark_value, 2)
    }
])

benchmark = pd.concat(
    [benchmark, benchmark_snapshot],
    ignore_index=True
)

benchmark.to_csv(
    benchmark_file,
    index=False
)

snapshot = pd.DataFrame([
    {
        "date": today,
        "portfolio_value": round(total_value, 2),
        "cash": round(cash, 2),
        "profit": round(profit, 2)
    }
])

portfolio_history = pd.concat(
    [portfolio_history, snapshot],
    ignore_index=True
)

portfolio_history.to_csv(
    portfolio_history_file,
    index=False
)

report.append("\n==========")
report.append("QQQ BENCHMARK")
report.append("==========")

report.append(
    f"QQQ Buy & Hold Value: ${benchmark_value:.2f}"
)

difference = total_value - benchmark_value

report.append(
    f"Bot Advantage: ${difference:.2f}"
)

report.append(
    f"\nPortfolio Value: ${total_value:.2f}"
)

report.append(
    f"Total Profit: ${profit:.2f}"
)

report.append("\n==========")
report.append("TRADE HISTORY")
report.append("==========")

report.append(
    f"Total Recorded Trades: {len(history)}"
)

report.append(
    f"Latest Recommendation: {top_pick}"
)

report.append("\n==========")
report.append("PORTFOLIO HISTORY")
report.append("==========")

report.append(
    f"Snapshots Recorded: "
    f"{len(portfolio_history)}"
)

if len(portfolio_history) >= 2:

    previous_value = (
        portfolio_history.iloc[-2]
        ["portfolio_value"]
    )

    change = total_value - previous_value

    report.append(
        f"Change Since Last Snapshot: "
        f"${change:.2f}"
    )


final_report = "\n".join(report)

print(final_report)

with open("report.txt", "w") as f:
    f.write(final_report)
