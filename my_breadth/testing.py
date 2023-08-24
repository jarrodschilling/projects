import sqlite3

name = 2

conn = sqlite3.connect('database.db')
cursor = conn.cursor()


cursor.execute("SELECT * FROM portfolios WHERE portfolio_id = 'portfolio1' AND users_id = ?", (name,))
portfolio1 = cursor.fetchall()

cursor.execute("SELECT * FROM portfolios WHERE portfolio_id = 'portfolio2' AND users_id = ?", (name,))
portfolio2 = cursor.fetchall()

cursor.execute("SELECT * FROM portfolios WHERE portfolio_id = 'portfolio3' AND users_id = ?", (name,))
portfolio3 = cursor.fetchall()

while True:
    try:
        portfolio_1_name = portfolio1[0][4]
        break
    except IndexError:
        portfolio_1_name = "none"
        break

while True:
    try:
        portfolio_2_name = portfolio2[0][4]
        break
    except IndexError:
        portfolio_2_name = "none"
        break

while True:
    try:
        portfolio_3_name = portfolio3[0][4]
        break
    except IndexError:
        portfolio_3_name = "none"
        break


#print(portfolio1)



conn.commit()
conn.close()