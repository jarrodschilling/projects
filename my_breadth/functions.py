from tradingview_ta import TA_Handler, Exchange, Interval
from functools import wraps
from flask import session, redirect, render_template


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
            port_name = port[0][4]
            break
        except IndexError:
            port_name = "none"
            break

    return port_name


def ma_compute(stocks, portfolio_id, ma_avg):
    portfolio_ma = []

    for stock in stocks:
        symbol = stock[1]
        screener = stock[2]
        exchange = stock[3]
        portfolio = stock[5]
        ma = moving_avgs(symbol, screener, exchange)
        ema20 = ma["COMPUTE"]["EMA20"]
        sma50 = ma["COMPUTE"]["SMA50"]
        sma200 = ma["COMPUTE"]["SMA200"]
        

        if portfolio == portfolio_id:
            if (ma_avg == "ema20") and (ema20 == "BUY"):
                portfolio_ma.append(symbol)
            elif (ma_avg == "sma50") and (sma50 == "BUY"):
                portfolio_ma.append(symbol)
            elif (ma_avg == "sma200") and (sma200 == "BUY"):
                portfolio_ma.append(symbol)

    return portfolio_ma
        

def symbol_check(symbol, exchange):
    try:
        moving_avgs(symbol, "america", exchange)
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