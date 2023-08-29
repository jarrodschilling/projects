from flask import Flask, render_template, url_for, request, redirect
from werkzeug.security import generate_password_hash
from functions import register_errors, contains_number
import string

app = Flask(__name__)

@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def signup_post():
    username = request.form.get("username")
    password = request.form.get("password")
    confirm_password = request.form.get("confirmpassword")

    print(f"ATTEMPT {username}, {password}, {confirm_password}")

    # check if username already in database
    # query database for all usernames and iterate results to see if new username matches
    #for i in user_names:
        #if username == i:
            #return error("Username already exists")
        
    if len(username) < 5:
        return register_errors("Username must be atleast 5 characters long")
    if len(username) > 25:
        return register_errors("Username cannot be more than 25 characters long")
    
    if len(password) < 5:
        return register_errors("Password must be atleast 5 characters long")
    if len(username) > 25:
        return register_errors("Password cannot be more than 25 characters long") 

    # Make sure password has one number and one special character
    numbers_count = 0
    input_str = password
    if contains_number(input_str):
        numbers_count += numbers_count
    if numbers_count == 0:
        return register_errors("Password must include atleast 1 number")
    
        
    specials_ch = ["!", "@", "#", "$", "%"]
    special_count = 0
    for i in password:
        for j in specials_ch:
            if i == j:
                special_count += special_count

    if special_count == 0:
        return register_errors("Password must contain atleast 1 special character !, @, #, $, %")



    
    if password != confirm_password:
        return register_errors("Passwords do not match")
    

    
    print(f"INPUT {username}, {password}, {confirm_password}")

    return redirect('/login')



@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    username = request.form.get("username")
    password = request.form.get("password")




    print(username, password)

    return redirect('/profile')



@app.route("/logout")
def logout():
    return "use this to logout"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")