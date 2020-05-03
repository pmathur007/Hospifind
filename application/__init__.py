from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = "5791628bb0b13ce0c676dfde280ba245"  # os.environ.get('FLASK_APP_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # os.environ.get('FLASK_APP_SQLALCHEMY_DATABASE_URI')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('HOSPIFIND_EMAIL_USER')
print(os.environ.get('HOSPIFIND_EMAIL_USER'))
app.config['MAIL_PASSWORD'] = os.environ.get('HOSPIFIND_EMAIL_PASS')
mail = Mail(app)

app.config['TEMPLATES_AUTO_RELOAD'] = True

from application.main import routes
from application.patient import routes
from application.hospital import routes
from application.errors import handlers
