import sqlite3
from functions import moving_avgs, login_required

name = 2

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM portfolios WHERE users_id = ?", (name,))
stocks = cursor.fetchall()

portfolio1 = []
portfolio1_ema20 = []
portfolio1_sma50 = []
portfolio1_sma200 = []
portfolio2 = []
portfolio2_ema20 = []
portfolio2_sma50 = []
portfolio2_sma200 = []
portfolio3 = []
portfolio3_ema20 = []
portfolio3_sma50 = []
portfolio3_sma200 = []


for stock in stocks:
    symbol = stock[1]
    screener = stock[2]
    exchange = stock[3]
    portfolio = stock[5]
    ma = moving_avgs(symbol, screener, exchange)
    ema20 = ma["COMPUTE"]["EMA20"]
    sma50 = ma["COMPUTE"]["SMA50"]
    sma200 = ma["COMPUTE"]["SMA200"]
    
    if portfolio == "portfolio1":
        portfolio1.append(symbol)
        if ema20 == "BUY":
            portfolio1_ema20.append(symbol)
        if sma50 == "BUY":
            portfolio1_sma50.append(symbol)
        if sma200 == "BUY":
            portfolio1_sma200.append(symbol)
    
    if portfolio == "portfolio3":
        portfolio2.append(symbol)
        if ema20 == "BUY":
            portfolio2_ema20.append(symbol)
        if sma50 == "BUY":
            portfolio2_sma50.append(symbol)
        if sma200 == "BUY":
            portfolio2_sma200.append(symbol)
    
    if portfolio == "portfolio3":
        portfolio3.append(symbol)
        if ema20 == "BUY":
            portfolio3_ema20.append(symbol)
        if sma50 == "BUY":
            portfolio3_sma50.append(symbol)
        if sma200 == "BUY":
            portfolio3_sma200.append(symbol)



#print(stocks)


conn.commit()
conn.close()

