
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

symbol = "NVDA"

# Download 2 days of 1-minute data
data = yf.download(tickers=symbol, period="2d", interval="1m", prepost=True)

# Drop MultiIndex (ticker level)
data.columns = data.columns.droplevel(1)

# Convert index to America/Chicago (CDT)
if data.index.tz is None:
    data.index = data.index.tz_localize("UTC").tz_convert("America/Chicago")
else:
    data.index = data.index.tz_convert("America/Chicago")

# Split data into separate days
data["Date"] = data.index.date
dates = sorted(data["Date"].unique())
if len(dates) < 2:
    print("Not enough days of data for gap analysis.")
    exit()

yesterday = dates[-2]
today = dates[-1]

# Extract last value from yesterday and first from today
yesterday_close = data[data["Date"] == yesterday]["Close"].between_time("14:59", "15:00").iloc[-1]
today_open = data[data["Date"] == today]["Close"].between_time("08:30", "08:31").iloc[0]
gap = today_open - yesterday_close

# Plot
plt.figure(figsize=(12, 6))
plt.plot(data.index, data["Close"], label=f"{symbol} Close Price", color="blue")
plt.axhline(y=yesterday_close, color="red", linestyle="--", label=f"Yesterday Close ({yesterday_close:.2f})")
plt.axhline(y=today_open, color="green", linestyle="--", label=f"Today Open ({today_open:.2f})")
plt.title(f"{symbol} Price with Overnight Gap: {gap:.2f}")
plt.xlabel("Time (CDT)")
plt.ylabel("Price")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()