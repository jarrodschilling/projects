from functions import ema, sma, current_price
import sqlite3

def ma_compute_yf(stocks, portfolio_id, ma_avg):
    portfolio_ma = []

    for stock in stocks:
        symbol = stock[1]
        portfolio = stock[3]
        current = current_price(symbol)
        ema20 = ema(symbol, 20)
        sma50 = sma(symbol, 50)
        sma200 = sma(symbol, 200)
        

        if portfolio == portfolio_id:
            if (ma_avg == "ema20") and current > ema20 and ema20 > sma50 and sma50 > sma200:
                portfolio_ma.append(symbol)
            elif (ma_avg == "sma50") and current > sma50 and sma50 > sma200:
                portfolio_ma.append(symbol)
            elif (ma_avg == "sma200") and current > sma200:
                portfolio_ma.append(symbol)

    return portfolio_ma


conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM finance WHERE users_id = '1'")
stocks = cursor.fetchall()
print(stocks)


portfolio2_ema20 = ma_compute_yf(stocks, "portfolio2", "ema20")
portfolio2_sma50 = ma_compute_yf(stocks, "portfolio2", "sma50")
portfolio2_sma200 = ma_compute_yf(stocks, "portfolio2", "sma200")

print(portfolio2_ema20)
print(portfolio2_sma50)
print(portfolio2_sma200)

conn.commit()
conn.close()