import os

import csv
import sqlite3
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from functions import moving_avgs, login_required
from dictionaries import sectors, industries, sub_sectors, stocks

app = Flask(__name__)

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


sec_twenty_list = 0
sec_ten_list = 0
sec_forty_list = 0
sec_length = 0
sec_twenty_detail = []
sec_ten_detail = []
sec_forty_detail = []

ind_twenty_list = 0
ind_ten_list = 0
ind_forty_list = 0
ind_length = 0
ind_twenty_detail = []
ind_ten_detail = []
ind_forty_detail = []

sub_sec_twenty_list = 0
sub_sec_ten_list = 0
sub_sec_forty_list = 0
sub_sec_length = 0
sub_sec_twenty_detail = []
sub_sec_ten_detail = []
sub_sec_forty_detail = []

for stock in stocks:
    symbol = stocks[stock]["symbol"]
    screener = stocks[stock]["screener"]
    exchange = stocks[stock]["exchange"]
    portfolio = stocks[stock]["portfolio"]
    ma = moving_avgs(symbol, screener, exchange)
    twenty = ma["COMPUTE"]["EMA20"]
    ten = ma["COMPUTE"]["SMA50"]
    forty = ma["COMPUTE"]["SMA200"]

    if portfolio == "sectors":
        sec_length += 1
        if twenty == "BUY":
            sec_twenty_list += 1
            sec_twenty_detail.append(stock)
        if ten == "BUY":
            sec_ten_list += 1
            sec_ten_detail.append(stock)
        if forty == "BUY":
            sec_forty_list += 1
            sec_forty_detail.append(stock)

    elif portfolio == "industries":
        ind_length += 1
        if twenty == "BUY":
            ind_twenty_list += 1
            ind_twenty_detail.append(stock)
        if ten == "BUY":
            ind_ten_list += 1
            ind_ten_detail.append(stock)
        if forty == "BUY":
            ind_forty_list += 1
            ind_forty_detail.append(stock)

    elif portfolio == "sub_sectors":
        sub_sec_length += 1
        if twenty == "BUY":
            sub_sec_twenty_list += 1
            sub_sec_twenty_detail.append(stock)
        if ten == "BUY":
            sub_sec_ten_list += 1
            sub_sec_ten_detail.append(stock)
        if forty == "BUY":
            sub_sec_forty_list += 1
            sub_sec_forty_detail.append(stock)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted

        # Ensure password was submitted

        # Query database for username USER/PASS ARE "test"
        username = request.form.get("username")
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        rows = cursor.fetchall()

        # Ensure username exists and password is correct

        # Remember which user has logged in
        session["user_id"] = rows[0][0]
        conn.commit()
        conn.close()

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")

        hash = generate_password_hash(password)
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, hash) VALUES(?, ?)", (username, hash))
        conn.commit()
        conn.close()
        return redirect("/")


@app.route("/", methods=["GET"])
@login_required
def index():
    return render_template("index.html")




@app.route("/detail", methods=["POST", "GET"])
@login_required
def detail():
    if request.method == "GET":
        return render_template("detail.html", sec_twenty_detail=sec_twenty_detail, sec_ten_detail=sec_ten_detail, sec_forty_detail=sec_forty_detail, ind_twenty_detail=ind_twenty_detail, ind_ten_detail=ind_ten_detail, ind_forty_detail=ind_forty_detail, sub_sec_twenty_detail=sub_sec_twenty_detail, sub_sec_ten_detail=sub_sec_ten_detail, sub_sec_forty_detail=sub_sec_forty_detail)


@app.route("/create-portfolio", methods=["GET", "POST"])
@login_required
def create_portfolio():
    if request.method == "GET":
        return render_template("create-portfolio.html")
    else:
        name = session.get("user_id")
        portfolio = request.form.get("portfolio")
        portfolio_id = request.form.get("portfolio_id")
        symbol1 = request.form.get("symbol1").upper()
        exchange1 = request.form.get("exchange1").upper()
        symbol2 = request.form.get("symbol2").upper()
        exchange2 = request.form.get("exchange2").upper()
        symbol3 = request.form.get("symbol3").upper()
        exchange3 = request.form.get("exchange3").upper()
        symbol4 = request.form.get("symbol4").upper()
        exchange4 = request.form.get("exchange4").upper()
        symbol5 = request.form.get("symbol5").upper()
        exchange5 = request.form.get("exchange5").upper()

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("INSERT INTO portfolios (symbol, screener, exchange, portfolio, portfolio_id, users_id) VALUES(?, ?, ?, ?, ?, ?)", (symbol1, 'america', exchange1, portfolio, portfolio_id, name))
        cursor.execute("INSERT INTO portfolios (symbol, screener, exchange, portfolio, portfolio_id, users_id) VALUES(?, ?, ?, ?, ?, ?)", (symbol2, 'america', exchange2, portfolio, portfolio_id, name))
        cursor.execute("INSERT INTO portfolios (symbol, screener, exchange, portfolio, portfolio_id, users_id) VALUES(?, ?, ?, ?, ?, ?)", (symbol3, 'america', exchange3, portfolio, portfolio_id, name))
        cursor.execute("INSERT INTO portfolios (symbol, screener, exchange, portfolio, portfolio_id, users_id) VALUES(?, ?, ?, ?, ?, ?)", (symbol4, 'america', exchange4, portfolio, portfolio_id, name))
        cursor.execute("INSERT INTO portfolios (symbol, screener, exchange, portfolio, portfolio_id, users_id) VALUES(?, ?, ?, ?, ?, ?)", (symbol5, 'america', exchange5, portfolio, portfolio_id, name))

        conn.commit()
        conn.close()
        return redirect("/portfolio")


@app.route("/portfolio", methods=["GET"])
@login_required
def portfolio_page():
    name = session.get("user_id")

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM portfolios WHERE users_id = ?", (name,))
    investments = cursor.fetchall()
    
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

    conn.commit()
    conn.close()

    return render_template("portfolio.html", investments=investments, portfolio1=portfolio1, portfolio2=portfolio2, portfolio3=portfolio3, portfolio_1_name=portfolio_1_name, portfolio_2_name=portfolio_2_name, portfolio_3_name=portfolio_3_name)



@app.route("/summary", methods=["POST", "GET"])
@login_required
def summary():
    total_twenty_list = sec_twenty_list + ind_twenty_list + sub_sec_twenty_list
    total_ten_list = sec_ten_list + ind_ten_list + sub_sec_ten_list
    total_forty_list = sec_forty_list + ind_forty_list + sub_sec_forty_list
    total_length = sec_length + ind_length + sub_sec_length
    total_twenty = total_twenty_list / total_length
    total_twenty = "{:.2%}".format(total_twenty)
    total_ten = total_ten_list / total_length
    total_ten = "{:.2%}".format(total_ten)
    total_forty = total_forty_list / total_length
    total_forty = "{:.2%}".format(total_forty)

    sec_twenty = sec_twenty_list / sec_length
    sec_twenty = "{:.2%}".format(sec_twenty)

    sec_ten = sec_ten_list / sec_length
    sec_ten = "{:.2%}".format(sec_ten)

    sec_forty = sec_forty_list / sec_length
    sec_forty = "{:.2%}".format(sec_forty)

    ind_twenty = ind_twenty_list / ind_length
    ind_twenty = "{:.2%}".format(ind_twenty)

    ind_ten = ind_ten_list / ind_length
    ind_ten = "{:.2%}".format(ind_ten)

    ind_forty = ind_forty_list / ind_length
    ind_forty = "{:.2%}".format(ind_forty)

    sub_sec_twenty = sub_sec_twenty_list / sub_sec_length
    sub_sec_twenty = "{:.2%}".format(sub_sec_twenty)

    sub_sec_ten = sub_sec_ten_list / sub_sec_length
    sub_sec_ten = "{:.2%}".format(sub_sec_ten)

    sub_sec_forty = sub_sec_forty_list / sub_sec_length
    sub_sec_forty = "{:.2%}".format(sub_sec_forty)

    if request.method == "GET":
        return render_template("summary.html", total_twenty=total_twenty, total_ten=total_ten, total_forty=total_forty, sec_twenty=sec_twenty, sec_ten=sec_ten, sec_forty=sec_forty, ind_twenty=ind_twenty, ind_ten=ind_ten, ind_forty=ind_forty, sub_sec_twenty=sub_sec_twenty, sub_sec_ten=sub_sec_ten, sub_sec_forty=sub_sec_forty)