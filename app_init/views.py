from flask import Blueprint, render_template
from flask_login import login_required, current_user

# this is the name of our blueprint, it will hold all of our routes
views = Blueprint('views', __name__)

@views.route("/")
@views.route("/home")
@login_required
def home_page():
    return render_template('home.html', name=current_user.username)