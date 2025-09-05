import re
from flask import Blueprint, render_template, redirect, url_for, request, flash
from .db_instance import database as db
from .models_db import User

#current user variable from 'flask login' allows us to access this variable once loged in and get the: username, password, email of the loggedin user
from flask_login import login_user, logout_user, login_required, current_user

#need to hash passwords so its not stored in clear text
from werkzeug.security import generate_password_hash, check_password_hash

# this is the name of our blueprint, it will hold all of our routes
auth = Blueprint('auth', __name__)

@auth.route("/login", methods=['GET','POST'])
def login_page():

    if request.method == 'POST':

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        # if the user exists we are going to check the hash the password aginst the user input pasword
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in!', category='success')
                # using flask login method
                login_user(user,remember=True)
            else:
                flash('Password inorrect!', category='error')
                return redirect(url_for('views.home'))
        else:
            flash('Email does\'t exist!', category='error')
    
    return render_template("login.html")

@auth.route("/sign-up", methods=['GET','POST'])
def signup_page():

    EMAIL_ADDR_REGEX = re.compile(r'^[\w\-\.]+@([\w-]+\.)+[\w-]{2,4}$')

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
        elif not re.match(EMAIL_ADDR_REGEX, email_address):
            flash('Email format incorrect!', category='error')
        
        else:
            # if all the checks are valid create the new user account, also hashing the password so it not in clear text
            new_user = User(email=email_address, username=username, password=generate_password_hash(password, method='sha256'))

            # send user to the database
            db.session.add(new_user)
            # this line acutually puts it into the database
            db.session.commit()
            login_user(new_user,remember=True)

            flash('User sucessfully created!')
            return redirect(url_for('views.home'))

        print(email_address)
    return render_template("signup.html")

# just redirect the user to a diffrent endpoint i.e our home function in views.py
@auth.route("/sign-out")
@login_required # this decorator only allows users to access the page only if you are logged in 
def signout_page():

    logout_user()
    return redirect(url_for("views.home"))