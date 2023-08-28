from flask import Blueprint, render_template, url_for, request, redirect

auth = Blueprint("auth", __name__)

@auth.route("/register")
def register():
    return render_template("register.html")


@auth.route("/register", methods=["POST"])
def signup_post():
    return True


@auth.route("/login")
def login():
    return render_template("login.html")



@auth.route("/logout")
def logout():
    return "use this to logout"