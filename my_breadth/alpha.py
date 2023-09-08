from alpha_vantage.foreignexchange import ForeignExchange
from pprint import pprint
import requests
import pandas as pd
import json

ALPHAVANTAGE_API_KEY = "L2PXBUL4LIYTG2UZ"

api_key = ALPHAVANTAGE_API_KEY
symbol = "NVDA"  # Example stock symbol
sma_period = "200"  # 200-day SMA
desired_date = "2006-01-19"  # Replace with the specific date you want
endpoint = f"https://www.alphavantage.co/query?function=SMA&symbol={symbol}&interval=daily&time_period={sma_period}&series_type=close&apikey={api_key}"


response = requests.get(endpoint)

# Check if the request was successful
if response.status_code == 200:
    json_data = response.json()
    #print(json_data)
else:
    print("Error: Unable to fetch data from Alpha Vantage API")
    json_data = None

# Check if the response contains SMA data
if "Technical Analysis: SMA" in json_data:
    sma_data = json_data["Technical Analysis: SMA"]
    
    # Get the most recent 200-day SMA value
    latest_date = max(sma_data.keys())
    print(latest_date)
    latest_sma_value = float(sma_data[latest_date]["SMA"])
    print(f"Most recent {sma_period}-day SMA for {symbol}: {latest_sma_value:.2f}")
else:
    print(f"SMA ({sma_period}-day) data not found in the response.")




def alpha(symbol, period, ma):
    api_key = ALPHAVANTAGE_API_KEY
    endpoint = f"https://www.alphavantage.co/query?function={ma}&symbol={symbol}&interval=daily&time_period={period}&series_type=close&apikey={api_key}"


    response = requests.get(endpoint)
    json_data = response.json()
    ma_data = json_data[f"Technical Analysis: {ma}"]
    
    # Get the most recent 200-day SMA value
    latest_date = max(ma_data.keys())
    latest_sma_value = float(ma_data[latest_date][f"{ma}"])
    return (latest_sma_value)

