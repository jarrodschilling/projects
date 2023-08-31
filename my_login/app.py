from flask import Flask, render_template, url_for, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from functions import register_errors, is_valid_password, login_errors, login_required
import sqlite3
from flask_session import Session

# flask --app example_app.py --debug run

app = Flask(__name__)

# ------ Setup Sessions/cache ------------------------------------------------------------------

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

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

    # Forget any user_id
    session.clear()

    # Get user info from forms
    username = request.form.get("username")
    password = request.form.get("password")
    # session["user"] = username


    # Ensure username was submitted
    if not username:
        login_errors("Username not entered")

    # Ensure password was submitted
    if not password:
        login_errors("Password not entered")

    # Query database for username
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    rows = cursor.fetchall()

    # Ensure username exists and password is correct
    if len(rows) != 1 or not check_password_hash(rows[0][2], password):
        return login_errors("Invalid username and/or password")

    # Remember which user has logged in
    session["user_id"] = rows[0][0]
    conn.commit()
    conn.close()


    print(username, password)

    return redirect('/profile')


# ------ LOGOUT USER -------------------------------------------------------------------------

@app.route("/logout")
@login_required
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


# ------ HOME PAGE ---------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")

# ------ USER HOME PAGE -----------------------------------------------------------------------
@app.route("/profile")
@login_required
def profile():
    name = session.get("user_id")
    return render_template("profile.html")