import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
from functions import ema, sma, price
import pytz


# Define the stock symbol (NVDA) and today's date
symbol = "NVDA"
today_date = datetime.today().strftime('%Y-%m-%d')

# Calculate yesterday's date by subtracting one day from today
yesterday_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')

# Fetch historical stock data for yesterday
data = yf.download(symbol, start=yesterday_date, end=today_date)

# Get yesterday's closing price
yesterday_closing_price = data['Close'].iloc[0]

# Print yesterday's closing price
print(f"Yesterday's closing price for {symbol} was: {yesterday_closing_price:.2f}")

ticker = "ELF"
period = 200

#p = price(ticker)

check20 = ema(ticker, 20)
print(check20)

check50 = sma(ticker, 50)
print(check50)

check200 = sma(ticker, 200)
print(check200)

if check20 > check50 and check50 > check200:
    print("TRENDING")
else:
    print("not so fast")




#ADD if statement for current time to create moving average based on yesterday close or today's close