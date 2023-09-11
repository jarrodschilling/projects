import sqlite3
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import pytz
import time


start_sma200 = time.time()
def api_call(symbol):
    symbol = symbol
    start_date = "2022-01-01"
    end_date = datetime.today().strftime('%Y-%m-%d')

    # Fetch historical stock data
    data = yf.download(symbol, start=start_date, end=end_date)

    return data





end_sma200 = time.time()
total_sma200 = (end_sma200 - start_sma200) * 10**3
print(total_sma200)