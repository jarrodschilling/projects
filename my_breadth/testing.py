import sqlite3
from functions import moving_avgs, login_required, symbol_check, create_errors
from tradingview_ta import TA_Handler, TradingView, Exchange, Interval, get_multiple_analysis




name = "12"
portfolio = "port"
portfolio_id = "portfolio2"
screener = "america"

symbol1 = "JPM"
exchange1 = "NYSE"

symbol2 = "asdf"
exchange2 = ""

symbol3 = "XLF"
exchange3 = "AMEX"

symbols_list = [symbol1, symbol2, symbol3]
#exchanges = [exchange1, exchange2, exchange3]



symbols = []
for i in range(0, len(symbols_list)):
    if symbols_list[i] != "":
        symbols.append(symbols_list[i])

# Make symbols uppercase
symbols_upper = [symbol.upper() for symbol in symbols]
print(symbols_upper)

# Find exchanges for symbols from tradingview.db
conn = sqlite3.connect('tradingview.db')
cursor = conn.cursor()


exchanges = []
symbols_upper_list = []
for i in range(0, len(symbols_upper)):

    cursor.execute("SELECT exchange FROM tv WHERE symbol = ?", (symbols_upper[i],))
    rows = cursor.fetchall()
    
    for row in range(0, len(rows)):
        if rows[0][0] != "":
            print(rows[0][0])
            exchanges.append(rows[0][0])
            symbols_upper_list.append(symbols_upper[i])

        elif rows[0][0] == None:
            print(rows[0][0])
            print(f"{symbols_upper[i]} does not exist, all other symbols entered successfully")

print(symbols_upper_list)
print(exchanges)
conn.commit()
conn.close()