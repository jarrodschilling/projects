import sqlite3
from functions import moving_avgs, login_required, symbol_check, apology
from tradingview_ta import TA_Handler, TradingView, Exchange, Interval, get_multiple_analysis
from yahooquery import Ticker


name = "6"
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



conn = sqlite3.connect('database.db')
cursor = conn.cursor()

##try:
cursor.execute("SELECT portfolio_id FROM portfolios WHERE users_id = ? GROUP BY portfolio_id", (name))
test = cursor.fetchall()
for i in test:
   print(i)


#except Exception as e:
    #print("False")




conn.commit()
conn.close()
