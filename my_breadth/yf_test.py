import sqlite3
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import pytz
import time


symbol = "NVDA"

start_date = "2023-07-10"
end_date = datetime.today().strftime('%Y-%m-%d')

# Fetch historical stock data
data = yf.download(symbol, start=start_date, end=end_date)
# Get yesterday's closing price
yesterday_closing_price = data['Close'].iloc[-1]
print(data)

ticker = yf.Ticker("AAPL")

print(ticker)


print(end_date)
print(yesterday_closing_price)


