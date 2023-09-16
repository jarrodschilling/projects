import sqlite3
from functions import api_call, current_price, symbol_check, create_errors
import yfinance as yf

def checker(ticker):
    data = yf.download(ticker)
    if data.empty:
        return False
    else:
        return True


name = "14"
portfolio = "okay"
portfolio_id = "portfolio1"


symbol1 = "XLE"
symbol2 = "XLF"
symbol3 = "adfasdf"

symbol_list = [symbol1, symbol2, symbol3]
error_symbol_list = []


def add_symbols(symbols_list, name, portfolio, portfolio_id, error_symbol_list):
    # Remove empty symbols from array
    symbols = []
    for i in range(0, len(symbols_list)):
        if symbols_list[i] != "":
            symbols.append(symbols_list[i])
    
    # Make symbols uppercase
    symbols_upper = [symbol.upper() for symbol in symbols]

    
    # INSERT Stocks into database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Check that symbol and exchange are correct
    error_symbol_list = error_symbol_list
    for i in range(0, len(symbols_upper)):
        # check to make sure symbol is correct for yfinance
        if (symbol_check(symbols_upper[i]) == True):
            cursor.execute("INSERT INTO portfolios (symbol, portfolio, portfolio_id, users_id) VALUES(?, ?, ?, ?)", (symbols_upper[i], portfolio, portfolio_id, name))
        else:
            error_symbol_list.append(symbols_upper[i])
    
    conn.commit()
    conn.close()

    # if errors in symbol, let the user know what they are
    return error_symbol_list

add_symbols(symbol_list, name, portfolio, portfolio_id, error_symbol_list)


if len(error_symbol_list) != 0:
        print(error_symbol_list)