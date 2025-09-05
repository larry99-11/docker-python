import os
from dotenv import load_dotenv
from flask import Flask
from .db_instance import database as db
from flask_login import LoginManager
from .views import views
from .auth import auth

load_dotenv()

database = db
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_PORT = os.getenv('DB_PORT')
KEY= os.getenv('SECRET_KEY')

# Add this line to check if the variables are loaded
print(f"DB_PORT is set to: {os.getenv('DB_PORT')}")

def create_app():
    
    app = Flask(__name__)
    # this encrypts our session data
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASS}@localhost:{DB_PORT}/{DB_NAME}' #path to database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    database.init_app(app)



    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    from .models_db import User

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

# function to create a database
def create_database(app):
    with app.app_context():
        # check if the database already exists
        if not os.path.exists("app_init/" + DB_NAME):
            database.create_all()
            print("created database!")


#@app.route('/info/<name>')
#def info(name):
#    return render_template('page.html', name=name)
