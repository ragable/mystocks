import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import pytz

# Parameters
symbol = "NVDA"
timezone = "US/Central"
date = pd.Timestamp.now(tz=timezone).strftime('%Y-%m-%d')  # Today

# Download 1-minute intraday data
data = yf.download(tickers=symbol, period="1d", interval="1m", prepost=True)

# Convert to CDT and extract the hour
data.index = data.index.tz_localize('UTC').tz_convert(timezone)
data['Hour'] = data.index.hour
data['Minute'] = data.index.minute
data['TimeStr'] = data.index.strftime('%H:%M')

# Filter for pre-market (e.g., 3 AM–8:30 AM CDT)
premarket = data.between_time("03:00", "08:29")

# Group by hour
hourly_volume = premarket.groupby(premarket.index.hour)['Volume'].sum()

# Plot
plt.figure(figsize=(10, 5))
hourly_volume.plot(kind='bar')
plt.title(f'NVDA Pre-Market Volume by Hour (CDT) – {date}')
plt.xlabel("Hour (CDT)")
plt.ylabel("Total Volume")
plt.xticks(rotation=0)
plt.grid(True)
plt.tight_layout()
plt.show()
