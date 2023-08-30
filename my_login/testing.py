from flask import Flask, render_template, url_for, request, redirect
from werkzeug.security import generate_password_hash
from functions import register_errors, is_valid_password
import sqlite3




username = "obin"
password = "test2+"
confirm_password = "test2+"



print(f"ATTEMPT {username}, {password}, {confirm_password}")

# Check if username already exists in database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute("SELECT username FROM users")
usernames = cursor.fetchall()

for user in usernames:
    if user[0] == username:
        print("That username already exists, please choose another one")

conn.commit()
conn.close()
    
# Check that username and password are each between 5 and 25 characters long
if len(username) < 5:
    print("Username must be atleast 5 characters long")
if len(username) > 25:
    print("Username cannot be more than 25 characters long")

if len(password) < 5:
    print("Password must be atleast 5 characters long")
if len(username) > 25:
    print("Password cannot be more than 25 characters long") 

# Check that password has one number and one special character
password_check = password
if not is_valid_password(password_check):
    print("invalid password.")

# Check that passwords match
if password != confirm_password:
    print("Passwords do not match")

hash = generate_password_hash(password)

# INSERT USER INTO users database table
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute("INSERT INTO users (username, password) VALUES(?, ?)", (username, hash))

conn.commit()
conn.close()

print(f"INPUT {username}, {password}, {confirm_password}")