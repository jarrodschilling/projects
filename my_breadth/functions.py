from tradingview_ta import TA_Handler, Exchange, Interval
from functools import wraps
from flask import session, redirect


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