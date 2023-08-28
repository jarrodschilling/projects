from flask import Blueprint, render_template, url_for, request, redirect

auth = Blueprint("auth", __name__)

@auth.route("/register")
def register():
    return render_template("register.html")


@auth.route("/register", methods=["POST"])
def signup_post():
    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")

    print(email, name, password)

    return redirect(url_for("auth.login"))

@auth.route("/login")
def login():
    return render_template("login.html")


@auth.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")

    print(email, password)

    return redirect(url_for("main.profile"))



@auth.route("/logout")
def logout():
    return "use this to logout"