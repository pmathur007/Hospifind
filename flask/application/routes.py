from flask import render_template, request
from application import app
from application.models import Hospital


@app.route("/")
@app.route("/home")
def home():
    hospitals = Hospital.query.filter_by(state="VA")
    return render_template('home.html', hospitals=hospitals)
