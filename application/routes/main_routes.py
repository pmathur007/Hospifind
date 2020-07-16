import json
import geocoder
from flask import render_template, request, session, redirect, url_for, flash
from sqlalchemy_json_querybuilder.querybuilder.search import Search
from application import app, db
from application.data_analysis import HomeDecision
from application.models import User, Hospital, Data
from application.utils import distance
from application.forms.main_forms import ContactForm
from application.utils import send_contact_email
import numpy as np

# ROUTES
# /
# /home
# /request_account
# /db

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    if 'ADDRESS' not in session:
        session['IP'] = str(request.remote_addr)
        g = geocoder.ip(session['IP'])
        if g.ok and len(g.latlng) == 2 and g.latlng[0] is not None and g.latlng[1] is not None:
            session['ADDRESS'] = g.city + ", " + g.state + ", " + g.country
            session['CITY'] = g.city
            session['STATE'] = g.state
            session['COUNTRY'] = g.country
            latlng = g.latlng
        else:
            session['ADDRESS'] = "6560 Braddock Rd, Alexandria, VA 22312"
            latlng = [38.819, -77.169]
        session['LATITUDE'] = latlng[0]
        session['LONGITUDE'] = latlng[1]

    form = ContactForm()
    if form.validate_on_submit():
        print('here')
        send_contact_email(form.name.data, form.email.data, form.subject.data, form.message.data)
        flash('Your contact email has been sent to the Hospifind team!', 'success')
        return redirect(url_for('home'))

    return render_template('home.html', form=form, address=session['ADDRESS'])


@app.route("/request_account")
def request_account():
    return render_template("request_account.html")


@app.route("/db", methods=['POST', 'DELETE'])
def query_db():
    tables = {
        'Hospital': Hospital,
        'User': User,
        'Data': Data
    }

    req_data = request.get_json()
    filter_by = req_data['filter_by']
    raw_results = Search(db.session, 'application.models', (
        tables[req_data['table_name']],), filter_by=filter_by, all=True).results['data']
    dict_results = [{c.name: str(getattr(result, c.name))
                     for c in result.__table__.columns} for result in raw_results]

    if request.method == 'POST':
        dict_results = [{c.name: str(getattr(result, c.name))
                         for c in result.__table__.columns} for result in raw_results]
        return json.dumps(dict_results)
    elif request.method == 'DELETE':
        for result in raw_results:
            db.session.delete(result)
        db.session.commit()
        return 'delete successful'