from flask import render_template, request, url_for, redirect, session
from application import app
from application.models import Hospital, Data
from application.data_analysis import PersonalDecision
from application.main.routes import distance


class Patient:
    def __init__(self, age, symptoms, conditions, near_covid):
        self.age = int(age)
        self.symptoms = symptoms
        self.conditions = len(conditions)
        self.near_covid = 1 if near_covid == 'y' else 0


@app.route("/patient_form", methods=["GET", "POST"])
def patient_form():
    if session.get('HOSPITALS') is None:
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
    if session.get('PERSONALIZED_HOSPITALS') is None or session.get('PERSONALIZED_RATINGS') is None:
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


@app.route("/call_911")
def call_911():
    return render_template("call_911.html")
