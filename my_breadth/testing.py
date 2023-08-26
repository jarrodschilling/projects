import sqlite3
from functions import moving_avgs, login_required
from tradingview_ta import TA_Handler, TradingView, Exchange, Interval, get_multiple_analysis
from yahooquery import Ticker


symbol1 = "XAR"
exchange1 = "AMEX"

symbol2 = "JPM"
exchange2 = "NYSE"

symbol3 = "XLF"
exchange3 = "AMEX"

symbols = [
    ["XAR", "AMEX"],
    ["JPM", "NYSE"],
    ["XLF", "AMEX"],
]

#symbol1 = Ticker(symbol1)

#print(symbol1.price)

def symbol_check(symbol, exchange):
    try:
        print(moving_avgs(symbol, "america", exchange))
    except Exception as e:
        print(f"Symbol: {symbol} or Exchange: {exchange} not found")


#for i in symbols:
    #print(symbols[i][0], symbols[i][1])

print(symbols[0][0], symbols[0][1])


