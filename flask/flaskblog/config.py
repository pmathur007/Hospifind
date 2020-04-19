import os


class Config:
    SECRET_KEY = "5791628bb0b13ce0c676dfde280ba245" # os.environ.get('FLASK_APP_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db' # os.environ.get('FLASK_APP_SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
