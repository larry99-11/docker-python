from app_init import database as db
from flask_login import UserMixin
from sqlalchemy.sql import func 

# db.Model is a base class
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    