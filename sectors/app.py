import os

from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from functions import moving_avgs
from dictionaries import sectors, industries, sub_sectors, stocks

app = Flask(__name__)



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




@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/detail", methods=["POST", "GET"])
def detail():
    if request.method == "GET":
        return render_template("detail.html", sec_twenty_detail=sec_twenty_detail, sec_ten_detail=sec_ten_detail, sec_forty_detail=sec_forty_detail, ind_twenty_detail=ind_twenty_detail, ind_ten_detail=ind_ten_detail, ind_forty_detail=ind_forty_detail, sub_sec_twenty_detail=sub_sec_twenty_detail, sub_sec_ten_detail=sub_sec_ten_detail, sub_sec_forty_detail=sub_sec_forty_detail)



@app.route("/summary", methods=["POST", "GET"])
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