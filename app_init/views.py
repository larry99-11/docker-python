from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models_db import Post
from . import db

# this is the name of our blueprint, it will hold all of our routes
views = Blueprint('views', __name__)

@views.route("/")
@views.route("/home")
@login_required
def home_page():
    return render_template('login.html', user=current_user)

@views.route("/create-post", methods=['GET','POST'])
@login_required
def create_post():

    if request.method == 'POST':
        text = request.form.get('text')

        if text == None:
            flash('posts cannot be empty!', category='error')
        else:
            post = Post(text=text, author=current_user.id)

            # add the post to the db session
            db.session.add(post)
            db.session.commit()

            flash('post created!', category='success')
    return render_template('create_post.html', user=current_user)