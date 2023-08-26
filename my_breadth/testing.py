import sqlite3
from functions import moving_avgs, login_required, symbol_check
from tradingview_ta import TA_Handler, TradingView, Exchange, Interval, get_multiple_analysis
from yahooquery import Ticker


symbol1 = "XAR"
exchange1 = "AMEX"

symbol2 = "JPM"
exchange2 = "NYSE"

symbol3 = "XLF"
exchange3 = "AMEX"

symbols = [
    ["XAR", "NYSE"],
    ["JPM", "NYSE"],
    ["XLF", "AMEX"],
]





for i in range(0, len(symbols)):
    symbol_check(symbols[i][0], symbols[i][1])

