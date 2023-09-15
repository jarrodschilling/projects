import sqlite3
from functions import api_call, current_price, symbol_check
import yfinance as yf

def checker(ticker):
    data = yf.download(ticker)
    if data.empty:
        return False
    else:
        return True


name = "12"
portfolio = "port"
portfolio_id = "portfolio2"


symbol1 = "JPM"
symbol2 = "XLF"
symbol3 = "adfasdf"

symbols_upper = [symbol1, symbol2, symbol3]

correct_list = []
error_symbol_list = []
for i in range(0, len(symbols_upper)):
    # check to make sure symbol is correct for yfinance
    if (checker(symbols_upper[i]) == True):
        correct_list.append(symbols_upper[i])
    else:
        error_symbol_list.append(symbols_upper[i])

print(correct_list)
print(error_symbol_list)

#msft = yf.Ticker("adfasd")

#msft.info