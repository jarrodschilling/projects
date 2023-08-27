import sqlite3
from functions import moving_avgs, login_required, symbol_check, apology
from tradingview_ta import TA_Handler, TradingView, Exchange, Interval, get_multiple_analysis
from yahooquery import Ticker


name = "check"
portfolio = "port"
portfolio_id = 1
screener = "america"

symbol1 = "XAR"
exchange1 = "AMEX"

symbol2 = "jpm"
exchange2 = ""

symbol3 = "XLF"
exchange3 = "AMEX"

symbols = [symbol1, symbol2, symbol3]
print(symbols)
exchanges = [exchange1, exchange2, exchange3]



stock_data = list(zip(symbols, exchanges))

stock_data_upper = [(symbol.upper(), exchange.upper()) for symbol, exchange in stock_data]

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

for i in range(0, len(stock_data_upper)):
    if stock_data_upper[i][0] != "" or stock_data_upper[i][1] != "":
        if (symbol_check(stock_data_upper[i][0], stock_data_upper[i][1])) == True:
            cursor.execute("INSERT INTO portfolios (symbol, screener, exchange, portfolio, portfolio_id, users_id) VALUES(?, ?, ?, ?, ?, ?)", (stock_data_upper[i][0], screener, stock_data_upper[i][1], portfolio, portfolio_id, name))
        else:
            print("Symbol or Exchange Incorrect")

conn.commit()
conn.close()
