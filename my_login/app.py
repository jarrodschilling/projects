from flask import Flask, render_template, url_for, request, redirect
from werkzeug.security import generate_password_hash
from functions import register_errors, is_valid_password
import sqlite3
# flask --app example_app.py --debug run

app = Flask(__name__)

# ------ REGISTRATION PAGE [GET] ---------------------------------------------------------------

@app.route("/register")
def register():
    return render_template("register.html")


# ------ REGISTER USER [POST] ------------------------------------------------------------------

@app.route("/register", methods=["POST"])
def signup_post():
    username = request.form.get("username")
    password = request.form.get("password")
    confirm_password = request.form.get("confirmpassword")

    # Check if username already exists in database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users")
    usernames = cursor.fetchall()
    conn.commit()
    conn.close()

    for user in usernames:
        if user[0] == username:
            return register_errors("That username already exists, please choose another one")
       
    # Check that username and password are each between 5 and 25 characters long
    if len(username) < 5:
        return register_errors("Username must be atleast 5 characters long")
    if len(username) > 25:
        return register_errors("Username cannot be more than 25 characters long")
    if len(password) < 5:
        return register_errors("Password must be atleast 5 characters long")
    if len(username) > 25:
        return register_errors("Password cannot be more than 25 characters long") 

    # Check that password has one number and one special character
    password_check = password
    if not is_valid_password(password_check):
        return register_errors("Password must contain at least 1 number, 1 letter, and 1 special character")

    # Check that passwords match
    if password != confirm_password:
        return register_errors("Passwords do not match")

    # All checks complete, hash password
    hash = generate_password_hash(password)

    # INSERT USER INTO users database table
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users (username, hash) VALUES(?, ?)", (username, hash))
    
    conn.commit()
    conn.close()

    return redirect('/login')


# ------ LOGIN PAGE [GET] ------------------------------------------------------------------

@app.route("/login")
def login():
    return render_template("login.html")


# ------ LOGIN USER [POST] ------------------------------------------------------------------

@app.route("/login", methods=["POST"])
def login_post():
    username = request.form.get("username")
    password = request.form.get("password")




    print(username, password)

    return redirect('/profile')


# ------ LOGOUT USER -------------------------------------------------------------------------

@app.route("/logout")
def logout():
    return "use this to logout"


# ------ HOME PAGE ---------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")

# ------ USER HOME PAGE -----------------------------------------------------------------------
@app.route("/profile")
def profile():
    return render_template("profile.html")