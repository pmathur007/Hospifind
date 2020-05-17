from flask import Flask
import os
from os import path
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import googlemaps

app = Flask(__name__)
# os.environ.get('FLASK_APP_SECRET_KEY')
app.config['SECRET_KEY'] = "5791628bb0b13ce0c676dfde280ba245"
# os.environ.get('FLASK_APP_SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

if path.exists(os.path.join('application', 'environment_variables.txt')):
    f = open(os.path.join('application', 'environment_variables.txt'), 'r')
    app.config['GOOGLE_MAPS_API_KEY_BACKEND'] = f.readline().strip()
    app.config['GOOGLE_MAPS_API_KEY_FRONTEND'] = f.readline().strip()
    app.config['GOOGLE_MAPS'] = googlemaps.Client(
        key=app.config['GOOGLE_MAPS_API_KEY_BACKEND'])
    app.config['MAIL_USERNAME'] = f.readline().strip()
    app.config['MAIL_PASSWORD'] = f.readline().strip()
else:
    app.config['GOOGLE_MAPS_API_KEY_BACKEND'] = None
    app.config['GOOGLE_MAPS_API_KEY_FRONTEND'] = None
    app.config['GOOGLE_MAPS'] = None
    app.config['MAIL_USERNAME'] = None
    app.config['MAIL_PASSWORD'] = None

mail = Mail(app)

app.config['TEMPLATES_AUTO_RELOAD'] = True

from application.main import routes
from application.patient import routes
from application.hospital import routes
from application.government import routes
from application.errors import handlers