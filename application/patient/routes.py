from flask import render_template, request, url_for, redirect, session, flash
from application import app
from application.models import Hospital, Data
from application.data_analysis import PersonalDecision
from application.utils import distance
from application.patient.forms import InputLocationForm
import geocoder
import os


class Patient:
    def __init__(self, age, symptoms, conditions, near_covid):
        self.age = int(age)
        self.symptoms = symptoms
        self.conditions = len(conditions)
        self.near_covid = 1 if near_covid == 'y' else 0


@app.route("/patient_form", methods=["GET", "POST"])
def patient_form():
    if 'HOSPITALS' not in session:
        return redirect(url_for('home'))

    print(session['HOSPITALS'])
    if request.method == "POST":
        emergency = request.form.get("emergency")
        patient = Patient(int(request.form.get("age")), request.form.getlist("symptoms"), request.form.getlist("conditions"), request.form.get("near_covid"))
        decision_maker = PersonalDecision([Hospital.query.get(hospital) for hospital in session['HOSPITALS']], [Data.query.get(d) for d in session['DATA']], patient)
        distances = [distance(session['LATITUDE'], session['LONGITUDE'], Hospital.query.get(hosp).latitude, Hospital.query.get(hosp).longitude) for hosp in session['HOSPITALS']]
        results = decision_maker.get_rating(distances)
        session['PERSONALIZED_HOSPITALS'] = [hospital.id for hospital in results]
        session['PERSONALIZED_RATINGS'] = [results[hospital] for hospital in results]
        if emergency == "y":
            return redirect(url_for('call_911'))
        print('here')
        return redirect(url_for('patient_results'))
    return render_template('patient_form.html', title='Patient Form')


@app.route("/patient_results")
def patient_results():
    if 'PERSONALIZED_HOSPITALS' not in session or 'PERSONALIZED_RATINGS' not in session:
        return redirect(url_for('home'))
    hospitals = [Hospital.query.get(hospital) for hospital in session['PERSONALIZED_HOSPITALS']]
    ratings = []
    for rating in session['PERSONALIZED_RATINGS']:
        if rating > 8:
            rating = "Great"
        elif rating > 5:
            rating = "Good"
        elif rating > 1:
            rating = "OK"
        else:
            rating = "Low Availability"
        ratings.append(rating)
    results = {hospitals[i]: ratings[i] for i in range(len(hospitals))}
    return render_template('patient_results.html', title='Personalized Results', results=results)


@app.route("/input_location", methods=['GET', 'POST'])
def input_location():
    form = InputLocationForm()
    if form.validate_on_submit():
        address = form.street_address.data + ", " + form.city.data + ", " + form.state.data + ", " + form.country.data + " " + form.zip_code.data
        print(address)
        g = geocoder.google(address, key=os.environ.get('GOOGLE_API_KEY'))
        print(g)
        if g.ok and len(g.latlng) == 2 and g.latlng[0] is not None and g.latlng[1] is not None:
            session['ADDRESS'] = address
            session['STREET_ADDRESS'] = form.street_address.data
            session['CITY'] = form.city.data
            session['STATE'] = form.state.data
            session['COUNTRY'] = form.country.data
            session['ZIP_CODE'] = form.zip_code.data
            session['LATITUDE'] = g.latlng[0]
            session['LONGITUDE'] = g.latlng[1]
            flash('Your location has been updated!', 'success')
            return redirect(url_for('home'))
        else:
            flash("We couldn't find the address you entered! Please try again." + " - " + str(g), 'danger')
            return redirect(url_for('input_location'))
    elif request.method == 'GET':
        if 'STREET_ADDRESS' in session:
            form.street_address.data = session['STREET_ADDRESS']
        if 'CITY' in session:
            form.city.data = session['CITY']
        if 'STATE' in session:
            form.state.data = session['STATE']
        if 'COUNTRY' in session:
            form.country.data = session['COUNTRY']
        if 'ZIP_CODE' in session:
            form.zip_code.data = session['ZIP_CODE']
    return render_template('input_location.html', form=form)


@app.route("/call_911")
def call_911():
    return render_template("call_911.html")
