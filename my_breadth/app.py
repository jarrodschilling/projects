import os

import csv
import sqlite3
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from functions import moving_avgs, login_required, portfolio_names, ma_compute, symbol_check
from dictionaries import sectors, industries, sub_sectors, stocks

app = Flask(__name__)

# flask --app example_app.py --debug run


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
        name = session.get("user_id")

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM portfolios WHERE users_id = ?", (name,))
        stocks = cursor.fetchall()

        cursor.execute("SELECT * FROM portfolios WHERE portfolio_id = 'portfolio1' AND users_id = ?", (name,))
        portfolio1 = cursor.fetchall()
        
        cursor.execute("SELECT * FROM portfolios WHERE portfolio_id = 'portfolio2' AND users_id = ?", (name,))
        portfolio2 = cursor.fetchall()
        
        cursor.execute("SELECT * FROM portfolios WHERE portfolio_id = 'portfolio3' AND users_id = ?", (name,))
        portfolio3 = cursor.fetchall()
        
        portfolio1_name = portfolio_names(portfolio1)
        portfolio2_name = portfolio_names(portfolio2)
        portfolio3_name = portfolio_names(portfolio3)

        portfolio1_ema20 = ma_compute(stocks, "portfolio1", "ema20")
        portfolio1_sma50 = ma_compute(stocks, "portfolio1", "sma50")
        portfolio1_sma200 = ma_compute(stocks, "portfolio1", "sma200")
        portfolio2_ema20 = ma_compute(stocks, "portfolio2", "ema20")
        portfolio2_sma50 = ma_compute(stocks, "portfolio2", "sma50")
        portfolio2_sma200 = ma_compute(stocks, "portfolio2", "sma200")
        portfolio3_ema20 = ma_compute(stocks, "portfolio3", "ema20")
        portfolio3_sma50 = ma_compute(stocks, "portfolio3", "sma50")
        portfolio3_sma200 = ma_compute(stocks, "portfolio3", "sma200")

        
        conn.commit()
        conn.close()

        return render_template("detail.html", portfolio1_name=portfolio1_name, portfolio1_ema20=portfolio1_ema20, portfolio1_sma50=portfolio1_sma50, portfolio1_sma200=portfolio1_sma200, portfolio2_name=portfolio2_name, portfolio2_ema20=portfolio2_ema20, portfolio2_sma50=portfolio2_sma50, portfolio2_sma200=portfolio2_sma200, portfolio3_name=portfolio3_name, portfolio3_ema20=portfolio3_ema20, portfolio3_sma50=portfolio3_sma50, portfolio3_sma200=portfolio3_sma200)


@app.route("/create-portfolio", methods=["GET", "POST"])
@login_required
def create_portfolio():
    if request.method == "GET":
        return render_template("create-portfolio.html")
    else:
        # Pull data from user form
        name = session.get("user_id")
        portfolio = request.form.get("portfolio")
        portfolio_id = request.form.get("portfolio_id")
        symbols = request.form.getlist("symbols[]")
        exchanges = request.form.getlist("exchanges[]")
        screener = "america"

        stock_data = list(zip(symbols, exchanges))
        stock_data_upper = [(symbol.upper(), exchange.upper()) for symbol, exchange in stock_data]
        
        # check to make sure symbol + exchange are correct
        for i in range(0, len(stock_data_upper)):
            symbol_check(stock_data_upper[i][0], stock_data_upper[i][1])

        # INSERT stocks into database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        insert_data = [(symbol, screener, exchange, portfolio, portfolio_id, name) for symbol, exchange in stock_data_upper]
        cursor.executemany("INSERT INTO portfolios (symbol, screener, exchange, portfolio, portfolio_id, users_id) VALUES(?, ?, ?, ?, ?, ?)", insert_data)
        
        conn.commit()
        conn.close()
        return redirect("/portfolio")

@app.route("/error-page", methods=["GET"])
@login_required
def error_page():
    return render_template("/error-page")

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
    
    
    portfolio1_name = portfolio_names(portfolio1)
    portfolio2_name = portfolio_names(portfolio2)
    portfolio3_name = portfolio_names(portfolio3)

    conn.commit()
    conn.close()

    return render_template("portfolio.html", investments=investments, portfolio1=portfolio1, portfolio2=portfolio2, portfolio3=portfolio3, portfolio1_name=portfolio1_name, portfolio2_name=portfolio2_name, portfolio3_name=portfolio3_name)



@app.route("/summary", methods=["POST", "GET"])
@login_required
def summary():
    name = session.get("user_id")

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM portfolios WHERE users_id = ?", (name,))
    stocks = cursor.fetchall()

    cursor.execute("SELECT * FROM portfolios WHERE portfolio_id = 'portfolio1' AND users_id = ?", (name,))
    portfolio1 = cursor.fetchall()
    
    cursor.execute("SELECT * FROM portfolios WHERE portfolio_id = 'portfolio2' AND users_id = ?", (name,))
    portfolio2 = cursor.fetchall()
    
    cursor.execute("SELECT * FROM portfolios WHERE portfolio_id = 'portfolio3' AND users_id = ?", (name,))
    portfolio3 = cursor.fetchall()
    
    portfolio1_name = portfolio_names(portfolio1)
    portfolio2_name = portfolio_names(portfolio2)
    portfolio3_name = portfolio_names(portfolio3)

    portfolio1_ema20 = ma_compute(stocks, "portfolio1", "ema20")
    portfolio1_sma50 = ma_compute(stocks, "portfolio1", "sma50")
    portfolio1_sma200 = ma_compute(stocks, "portfolio1", "sma200")
    portfolio2_ema20 = ma_compute(stocks, "portfolio2", "ema20")
    portfolio2_sma50 = ma_compute(stocks, "portfolio2", "sma50")
    portfolio2_sma200 = ma_compute(stocks, "portfolio2", "sma200")
    portfolio3_ema20 = ma_compute(stocks, "portfolio3", "ema20")
    portfolio3_sma50 = ma_compute(stocks, "portfolio3", "sma50")
    portfolio3_sma200 = ma_compute(stocks, "portfolio3", "sma200")

    conn.commit()
    conn.close()

    total_ema20_list = portfolio1_ema20 + portfolio2_ema20 + portfolio3_ema20
    total_sma50_list = portfolio1_sma50 + portfolio2_sma50 + portfolio3_sma50
    total_sma200_list = portfolio1_sma200 + portfolio2_sma200 + portfolio3_sma200
    total_length = len(portfolio1) + len(portfolio2) + len(portfolio3)
    

    while True:
        try:
            total_ema20 = len(total_ema20_list) / total_length
            total_ema20 = "{:.2%}".format(total_ema20)

            total_sma50 = len(total_sma50_list) / total_length
            total_sma50 = "{:.2%}".format(total_sma50)

            total_sma200 = len(total_sma200_list) / total_length
            total_sma200 = "{:.2%}".format(total_sma200)
            break
        except ZeroDivisionError:
            total_ema20 = "none"
            total_sma50 = "none"
            total_sma200 = "none" 
            break

    while True:
        try:
            portfolio1_ema20_summary = len(portfolio1_ema20) / len(portfolio1)
            portfolio1_ema20_summary = "{:.2%}".format(portfolio1_ema20_summary)

            portfolio1_sma50_summary = len(portfolio1_sma50) / len(portfolio1)
            portfolio1_sma50_summary = "{:.2%}".format(portfolio1_sma50_summary)

            portfolio1_sma200_summary = len(portfolio1_sma200) / len(portfolio1)
            portfolio1_sma200_summary = "{:.2%}".format(portfolio1_sma200_summary)
            break
        except ZeroDivisionError:
            portfolio1_ema20_summary = "none"
            portfolio1_sma50_summary = "none"
            portfolio1_sma200_summary = "none" 
            break

    while True:
        try:
            portfolio2_ema20_summary = len(portfolio2_ema20) / len(portfolio2)
            portfolio2_ema20_summary = "{:.2%}".format(portfolio2_ema20_summary)

            portfolio2_sma50_summary = len(portfolio2_sma50) / len(portfolio2)
            portfolio2_sma50_summary = "{:.2%}".format(portfolio2_sma50_summary)

            portfolio2_sma200_summary = len(portfolio2_sma200) / len(portfolio2)
            portfolio2_sma200_summary = "{:.2%}".format(portfolio2_sma200_summary)
            break
        except ZeroDivisionError:
            portfolio2_ema20_summary = "none"
            portfolio2_sma50_summary = "none"
            portfolio2_sma200_summary = "none" 
            break
    
    while True:
        try:
            portfolio3_ema20_summary = len(portfolio3_ema20) / len(portfolio3)
            portfolio3_ema20_summary = "{:.2%}".format(portfolio3_ema20_summary)

            portfolio3_sma50_summary = len(portfolio3_sma50) / len(portfolio3)
            portfolio3_sma50_summary = "{:.2%}".format(portfolio3_sma50_summary)

            portfolio3_sma200_summary = len(portfolio3_sma200) / len(portfolio3)
            portfolio3_sma200_summary = "{:.2%}".format(portfolio3_sma200_summary)
            break
        except ZeroDivisionError:
            portfolio3_ema20_summary = "none"
            portfolio3_sma50_summary = "none"
            portfolio3_sma200_summary = "none" 
            break
    

    if request.method == "GET":
        return render_template("summary.html", total_ema20=total_ema20, total_sma50=total_sma50, total_sma200=total_sma200, portfolio1_ema20_summary=portfolio1_ema20_summary, portfolio1_sma50_summary=portfolio1_sma50_summary, portfolio1_sma200_summary=portfolio1_sma200_summary, portfolio2_ema20_summary=portfolio2_ema20_summary, portfolio2_sma50_summary=portfolio2_sma50_summary, portfolio2_sma200_summary=portfolio2_sma200_summary, portfolio3_ema20_summary=portfolio3_ema20_summary, portfolio3_sma50_summary=portfolio3_sma50_summary, portfolio3_sma200_summary=portfolio3_sma200_summary, portfolio1_name=portfolio1_name, portfolio2_name=portfolio2_name, portfolio3_name=portfolio3_name)