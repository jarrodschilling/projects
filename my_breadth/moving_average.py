import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime
from functions import ema, sma
import pytz

# Define the stock symbol (NVDA) and date range
symbol = "NVDA"
start_date = "2022-01-01"
end_date = datetime.today().strftime('%Y-%m-%d')

# Fetch historical stock data
data = yf.download(symbol, start=start_date, end=end_date)

# Calculate the 20-day EMA
ema_period = 20
data[f'EMA_{ema_period}'] = data['Close'].ewm(span=ema_period, adjust=False).mean()

# Print the DataFrame with EMA values
print(data[['Close', 'EMA_20']])

# Get the most recent day's closing 20 EMA
most_recent_20_ema = data['EMA_20'].iloc[-1]

# Print the most recent day's closing 20 EMA
print(f"The most recent day's closing 20 EMA for {symbol} is: {most_recent_20_ema:.2f}")

ticker = "ELF"
period = 200

check = ema(ticker, period)
print(check)

ready = sma(ticker, period)
print(ready)

print(end_date)
# Set the time zone to Eastern Standard Time (EST)
est_timezone = pytz.timezone("US/Eastern")

# Get the current time in EST
current_time_est = datetime.now(est_timezone).time()
formatted_time = current_time_est.strftime("%H:%M")

# Print the current time in EST
print("Current time in EST:", formatted_time)

#ADD if statement for current time to create moving average based on yesterday close or today's close