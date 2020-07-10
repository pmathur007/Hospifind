from flask import render_template, request, session, redirect, url_for, flash
from application import app, db

@app.route('/testing_centers', methods=['GET'])
def testing_centers():
    return render_template('testing_centers.html')