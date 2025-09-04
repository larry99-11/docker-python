
from flask import Blueprint, render_template, redirect, url_for, request, flash
from app_init import database as db
from models_db import User
from flask_login import login_user, logout_user, login_required

#need to hash passwords so its not stored in clear text
from werkzeug.security import generate_password_hash, check_password_hash

# this is the name of our blueprint, it will hold all of our routes
auth = Blueprint('auth', __name__)

@auth.route("/login", methods=['GET','POST'])
def login_page():
    username = request.form.get("username")
    password = request.form.get("password")

    return render_template("login.html")

@auth.route("/sign-up", methods=['GET','POST'])
def signup_page():

    if  request.method =='POST':

        # getting our data from the signup form
        email_address = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        passwordAgain = request.form.get("passwordAgain")

        # check to see if user email.exist by filtering for it and obtaing the first result
        email_exist = User.query.filter_by(email=email_address).first()
        user_exist = User.query.filter_by(username=username).first()

        if email_exist:
            flash('Email already exists!', category='error')
        elif user_exist:
            flash('User already exists!', category='error')
        # password checking
        elif password != passwordAgain:
            flash('Password doesn\'t match!', category='error')
        elif len(username) > 2:
            flash('Username is too short!', category='error')
        elif len(password) > 6:
            flash('Password is too short!', category='error')
        
        #NOTE: write some regex to verify the email
        elif re.match(email_address):
            flash('Email format incorrect!', category='error')
        
        else:
            # if all the checks are valid create the new user account
            new_user = User(email=email_address, username=username, password=password)

            # send user to the database
            db.session.add(new_user)
            # this line acutually puts it into the database
            db.session.commit()

            flash('User sucessfully created!')
            return redirect(url_for('views.home'))

        print(email_address)
    return render_template("signup.html")

# just redirect the user to a diffrent endpoint i.e our home function in views.py
@auth.route("/sign-out")
def signout_page():
    return redirect(url_for("views.home"))