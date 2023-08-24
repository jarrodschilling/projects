import sqlite3

conn = sqlite3.connect('test.db')
cursor = conn.cursor()

cursor.execute("INSERT INTO tests VALUES (1, 'BAC', 'banks');")

print("success")

conn.commit()
conn.close()


