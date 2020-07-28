from flask import render_template, request, session, redirect, url_for, flash
from application import app, db

@app.route('/testing_centers', methods=['GET'])
def testing_centers():
    centers = [
    {
        "name": "name1",
        "address": "6840 Lady Adelaide Court, Centreville, VA",
        "lat": 77,
        "long": -38,
        "walkUp": False,
        "referral": True,
        "appointment": True
    },
    {
        "name": "name2",
        "address": "6560 Braddock Road, Alexandria, VA",
        "lat": 77.169,
        "long": -38.819,
        "walkUp": True,
        "referral": False,
        "appointment": False
    }]
    return render_template('testing_centers.html', testing_centers=centers, api_key=app.config['GOOGLE_MAPS_API_KEY_FRONTEND'])