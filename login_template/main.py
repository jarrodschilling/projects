from flask import Blueprint, render_template
# flask --app example_app.py --debug run


main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/profile")
def profile():
    return render_template("profile.html")