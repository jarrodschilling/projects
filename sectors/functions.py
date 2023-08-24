import csv
import datetime
import pytz
import requests
import subprocess
import urllib
import uuid

from flask import redirect, render_template, session
from functools import wraps
from tradingview_ta import TA_Handler, Interval, Exchange


def moving_avgs(symbol, screener, exchange):
    stock = TA_Handler(
        symbol=symbol,
        screener=screener,
        exchange=exchange,
        interval=Interval.INTERVAL_1_DAY,
    )
    return stock.get_analysis().moving_averages


stock = TA_Handler(
    symbol="XLF",
    screener="america",
    exchange="AMEX",
    interval=Interval.INTERVAL_1_DAY,
    # proxies={'http': 'http://example.com:8080'} # Uncomment to enable proxy (replace the URL).
)
#print(stock.get_analysis().moving_averages)
# Example output: {"RECOMMENDATION": "BUY", "BUY": 8, "NEUTRAL": 6, "SELL": 3}

moving_avgs("XHB", "america", "AMEX")
