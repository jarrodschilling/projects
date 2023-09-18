import sqlite3
from functions import api_call, current_price, symbol_check, create_errors, get_port_name, ma_compute_yf
import yfinance as yf


name = "20"
portfolio = "ports 1"
portfolio_id = "portfolio1"


symbol1 = "XLB"
symbol2 = "XLK"
symbol3 = "adfasdf"
symbol_list = [symbol1, symbol2, symbol3]

name = 20
new_list = []
conn = sqlite3.connect('database.db')
cursor = conn.cursor()


cursor.execute("SELECT symbol FROM portfolios WHERE users_id = ? AND portfolio_id = ?", (name, portfolio_id))
stocks = cursor.fetchall()
for i in range(0, len(symbol_list)):
    for j in range(0, len(stocks)):
        if symbol_list[i] != stocks[j]:
            new_list.append(symbol_list[i])

print(stocks)
print(new_list)
conn.commit()
conn.close()

