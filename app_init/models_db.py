from .db_instance import database as db
from flask_login import UserMixin
from sqlalchemy.sql import func 

# db.Model is a base class
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    posts = db.relationship('Post', backref='user', passive_deletes=True)

# creating a model to store all the posts 
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    
    #Foreign keys
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False) # this represents the ID of the user and find the results of the ID, Also 'casdade' paramter when the user is deleted will delete the post related to the user
