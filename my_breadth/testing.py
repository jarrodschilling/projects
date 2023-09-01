import sqlite3
from functions import moving_avgs, login_required, symbol_check
from tradingview_ta import TA_Handler, TradingView, Exchange, Interval, get_multiple_analysis
from yahooquery import Ticker


name = "12"
portfolio = "port"
portfolio_id = "portfolio2"
screener = "america"

symbol1 = "XAR"
exchange1 = "NYSE"

symbol2 = "jpm"
exchange2 = ""

symbol3 = "XLF"
exchange3 = "AMEX"

symbols = [symbol1, symbol2, symbol3]
exchanges = [exchange1, exchange2, exchange3]


# INSERT Stocks into database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Check to see if portfolio_id already exists for user
cursor.execute("SELECT portfolio FROM portfolios WHERE users_id = ? AND portfolio_id = ?", (name, portfolio_id,))
rows = cursor.fetchall()

print(rows[0][0])

conn.commit()
conn.close()
