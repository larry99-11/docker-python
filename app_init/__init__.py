import os
from dotenv import load_dotenv
from flask import Flask
from .db_instance import database as db
from flask_login import LoginManager
from .views import views
from .auth import auth

load_dotenv()

# Get all necessary environment variables
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
KEY = os.getenv('SECRET_KEY')

print(f'our port num is: {DB_PORT}')
def create_app():
    
    app = Flask(__name__)
    # this encrypts our session data
    app.config['SECRET_KEY'] = KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}' #path to database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)



    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    from .models_db import User, Post

    create_database(app)

    # this object will allow us to log users in and out
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login_page'
    login_manager.init_app(app)

    # allows access to info related to the user from the database when an ID is passed in
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))



    return app

# function to create a database tables
def create_database(app):
    with app.app_context():
        # In a Docker environment, the database is a separate service.
        # We should always call create_all() to ensure tables are created
        # without checking for a local file.
        db.create_all()
        print("created database!")


#@app.route('/info/<name>')
#def info(name):
#    return render_template('page.html', name=name)
