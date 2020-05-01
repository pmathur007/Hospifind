from flask import render_template, request, url_for, redirect
from application import app


@app.route("/patient_form", methods=["GET", "POST"])
def patient_form():
    if request.method == "POST":
        # handle form data
        return redirect(url_for('home'))
    return render_template('patient_form.html', title='Personalized Results')
