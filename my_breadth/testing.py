import sqlite3
from functions import api_call, current_price, symbol_check, create_errors, get_port_name, ma_compute_yf
import yfinance as yf


name = "20"
portfolio = "ports 1"
portfolio_id = "portfolio1"


symbol1 = "XLB"
symbol2 = "XLK"
symbol3 = "adfasdf"
#symbol_list = [symbol1, symbol2, symbol3]

name = 20

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM portfolios WHERE users_id = ?", (name,))
stocks = cursor.fetchall()

conn.commit()
conn.close()

tickers, names = ma_compute_yf(stocks, portfolio_id, "sma200")

result = []

for x, y in zip(tickers, names):
    result.append([x, y])

print(result)
print(result[0][0], result[0][1])