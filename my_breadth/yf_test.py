import sqlite3
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import pytz
import time


start_sma200 = time.time()
sma_period_1 = 50
sma_period_2 = 200
symbol = "NVDA"
start_date = "2022-01-01"
end_date = datetime.today().strftime('%Y-%m-%d')

# Fetch historical stock data
data = yf.download(symbol, start=start_date, end=end_date)

# Calculate the 50-day SMA
data[f'SMA_{sma_period_1}'] = data['Close'].rolling(window=sma_period_1).mean()

most_recent_50_sma = data[f'SMA_{sma_period_1}'].iloc[-1]
print(most_recent_50_sma)

# Calculate the 200-day SMA
# Calculate the 50-day SMA
data[f'SMA_{sma_period_2}'] = data['Close'].rolling(window=sma_period_2).mean()

most_recent_200_sma = data[f'SMA_{sma_period_2}'].iloc[-1]
print(most_recent_200_sma)

end_sma200 = time.time()

total_sma200 = (end_sma200 - start_sma200) * 10**3
print(f"Total SMA200: {total_sma200}")