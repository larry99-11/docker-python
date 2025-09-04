from flask import Blueprint, render_template

# this is the name of our blueprint, it will hold all of our routes
views = Blueprint('views', __name__)

@views.route("/")
@views.route("/home")
def home_page():
    return render_template('home.html')