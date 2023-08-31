import sqlite3
from functions import moving_avgs, login_required, symbol_check
from tradingview_ta import TA_Handler, TradingView, Exchange, Interval, get_multiple_analysis
from yahooquery import Ticker


name = "10"
portfolio = "port"
portfolio_id = "portfolio1"
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
cursor.execute("SELECT portfolio_id FROM portfolios WHERE users_id = ?", (name,))
rows = cursor.fetchall()

port1 = ''
port2 = ''
port3 = ''

for row in range(0, len(rows)):
    if rows[row][0] == 'portfolio1':
        port1 = True
    elif rows[row][0] == "portfolio2":
        port2 = True
    elif rows[row][0] == "portfolio3":
        port3 = True

if port1 == True:
    print("Portfolio 1 already created")
elif port2 == True:
    print("Portfolio 2 already created")
elif port3 == True:
    print("Portfolio 3 already created")

conn.commit()
conn.close()
