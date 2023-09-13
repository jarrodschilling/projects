from tradingview_ta import TA_Handler, Exchange, Interval
from functools import wraps
from flask import session, redirect, render_template
import requests
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import pytz

def current_price(data):
    data = data
    # Get yesterday's closing price
    yesterday_closing_price = data['Close'].iloc[-1]

    return yesterday_closing_price

def ema(data, ema_period):
    data = data
    ema_period = ema_period
    
    data[f'EMA_{ema_period}'] = data['Close'].ewm(span=ema_period, adjust=False).mean()

    # Get the most recent day's closing 20 EMA
    most_recent_20_ema = data[f'EMA_{ema_period}'].iloc[-1]

    return most_recent_20_ema

def sma(data, sma_period):
    data = data
    sma_period = sma_period
    data[f'SMA_{sma_period}'] = data['Close'].rolling(window=sma_period).mean()

    most_recent_50_sma = data[f'SMA_{sma_period}'].iloc[-1]

    return most_recent_50_sma


def ma_compute_yf(stocks, portfolio_id, ma_avg):
    portfolio_ma = []

    for stock in stocks:
        symbol = stock[1]
        portfolio = stock[3]
        data = api_call(symbol)
        current = current_price(data)
        ema20 = ema(data, 20)
        sma50 = sma(data, 50)
        sma200 = sma(data, 200)
        

        if portfolio == portfolio_id:
            if (ma_avg == "ema20") and current > ema20 and ema20 > sma50 and sma50 > sma200:
                portfolio_ma.append(symbol)
            elif (ma_avg == "sma50") and current > sma50 and sma50 > sma200:
                portfolio_ma.append(symbol)
            elif (ma_avg == "sma200") and current > sma200:
                portfolio_ma.append(symbol)

    return portfolio_ma


def api_call(symbol):
    symbol = symbol
    start_date = "2022-01-01"
    end_date = datetime.today().strftime('%Y-%m-%d')

    # Fetch historical stock data
    data = yf.download(symbol, start=start_date, end=end_date)

    return data


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def portfolio_names(port):
    while True:
        try:
            port_name = port[0][2]
            break
        except IndexError:
            port_name = "none"
            break

    return port_name


def symbol_check(symbol):
    try:
        api_call(symbol)
        return True
    except Exception as e:
        return False

def register_errors(problem):
    return render_template('register.html', problem=problem)

def login_errors(problem):
    return render_template('login.html', problem=problem)

def create_errors(problem):
    return render_template('create-portfolio.html', problem=problem)


def is_valid_password(password):
    # Check for at least one digit, one letter, and one special character
    has_digit = any(char.isdigit() for char in password)
    has_letter = any(char.isalpha() for char in password)
    has_special = any(char for char in password if not char.isalnum())

    return has_digit and has_letter and has_special