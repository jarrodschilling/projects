from flask import Flask, render_template, url_for, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from functions import register_errors, is_valid_password
import sqlite3




username = "bradley"
password = "win12#"
confirm_password = "test2+"

print(f"ATTEMPT {username}, {password}")

# Forget any user_id


# Get user info from forms

# session["user"] = username


# Ensure username was submitted
if not username:
    print("Username not entered")

# Ensure password was submitted
if not password:
    print("Password not entered")

# Query database for username
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
rows = cursor.fetchall()
#print(rows[0][2])

# Ensure username exists and password is correct
if len(rows) != 1 or not check_password_hash(rows[0][2], password):
    print("invalid username and/or password", 403)

# Remember which user has logged in
conn.commit()
conn.close()


print(username, password)

