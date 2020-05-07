import json
import geocoder
from flask import render_template, request, session, redirect, url_for, flash
from sqlalchemy_json_querybuilder.querybuilder.search import Search
from application import app, db
from application.data_analysis import HomeDecision
from application.models import User, Hospital, Data
from application.utils import distance
from application.main.forms import ContactForm
from application.utils import send_contact_email
import numpy as np


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    if 'UPDATE_NEEDED' not in session:
        session['UPDATE_NEEDED'] = False

    form = ContactForm()
    if form.validate_on_submit():
        print('here')
        send_contact_email(form.name.data, form.email.data, form.subject.data, form.message.data)
        flash('Your contact email has been sent to the Hospifind team!', 'success')
        return redirect(url_for('home'))

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
            session['ADDRESS'] = "FAILURE"
            latlng = [38.8809, -77.3008]
        session['LATITUDE'] = latlng[0]
        session['LONGITUDE'] = latlng[1]
    # print(session['ADDRESS'])
    # print(state, latitude, longitude)

    if session['UPDATE_NEEDED'] or ('HOSPITALS' not in session or 'DATA' not in session or 'DISTANCES' not in session or 'TIMES' not in session):
        session['UPDATE_NEEDED'] = False
        hospitals = Hospital.query.all()
        # hospitals = hospitals[:10]
        hospitals = [x for x in hospitals if distance(session['LATITUDE'], session['LONGITUDE'], x.latitude, x.longitude) < 60]
        hospitals.sort(key=lambda x: distance(session['LATITUDE'], session['LONGITUDE'], x.latitude, x.longitude))
        session['ORIGINAL_LENGTH'] = len(hospitals)
        if len(hospitals) > 15:
            hospitals = hospitals[:15]
        session['LENGTH'] = len(hospitals)
        session['HOSPITALS'] = [hospital.id for hospital in hospitals]
        data = [Data.query.filter_by(hospital=hospital.id).order_by(Data.date.desc()).first() for hospital in hospitals]
        session['DATA'] = [d.id for d in data]
        info = app.config['GOOGLE_MAPS'].distance_matrix(session['ADDRESS'], [hospital.address for hospital in hospitals], mode="driving", units="imperial")
        session['DISTANCES'] = {}; session['TIMES'] = {}
        session['DISTANCE_STRINGS'] = {}; session['TIME_STRINGS'] = {}
        print(info)
        for i in range(len(info['rows'][0]['elements'])):
            if info['rows'][0]['elements'][i]['status'] == 'OK':
                session['DISTANCES'][str(session['HOSPITALS'][i])] = float(info['rows'][0]['elements'][i]['distance']['text'].replace(",", "").split(" ")[0])

                arr = info['rows'][0]['elements'][i]['duration']['text'].replace(",", "").split(" ")
                if len(arr) == 2:
                    time = float(arr[0])
                elif len(arr) == 4 and arr[1].strip()[0:4] == "hour":
                    time = float(arr[0]) * 60 + float(arr[2])
                elif len(arr) == 4 and arr[1].strip()[0:3] == "day":
                    time = float(arr[0]) * 1440 + float(arr[2]) * 60
                session['TIMES'][str(session['HOSPITALS'][i])] = time

                session['DISTANCE_STRINGS'][str(session['HOSPITALS'][i])] = info['rows'][0]['elements'][i]['distance']['text']
                session['TIME_STRINGS'][str(session['HOSPITALS'][i])] = info['rows'][0]['elements'][i]['duration']['text']
            else:
                session['DISTANCES'][str(session['HOSPITALS'][i])] = 99999
                session['TIMES'][str(session['HOSPITALS'][i])] = 99999
                session['DISTANCE_STRINGS'][str(session['HOSPITALS'][i])] = 'Error'
                session['TIME_STRINGS'][str(session['HOSPITALS'][i])] = 'Error'

    print(session['HOSPITALS'], session['DISTANCES'], session['TIMES'], sep="\n")

    decision_maker = HomeDecision([Hospital.query.get(hospital) for hospital in session['HOSPITALS']], [Data.query.get(data) for data in session['DATA']])
    results = decision_maker.get_rating()

    print(results)

    hospitals = []
    ratings = {}
    for hospital in results:
        hospitals.append(hospital)
        rating = results[hospital]
        if rating > 8:
            rating = "Great"
        elif rating > 5:
            rating = "Good"
        elif rating > 1:
            rating = "OK"
        else:
            rating = "Low Availability"
        ratings[hospital] = rating

    map_list = [(session['ADDRESS'], session['LATITUDE'], session['LONGITUDE'])]

    sort = "time_and_rating"
    if sort == "rating":
        new_ratings = [ratings[hospital] for hospital in ratings]
        results = [(session['HOSPITALS'][i], new_ratings[i], session['DISTANCES'][hospitals[i].id], session['TIMES'][hospitals[i].id]) for i in range(len(hospitals))]
        for i in range(len(hospitals)):
            map_list.append((hospitals[i].name, hospitals[i].address, hospitals[i].latitude, hospitals[i].longitude, results[hospitals[i]]))
        return render_template('home.html', results=results, header="Hospitals Sorted by Rating",  map_list=map_list, form=form, original_length=session['ORIGINAL_LENGTH'], length=session['LENGTH'], api_key=app.config['GOOGLE_MAPS_API_KEY_FRONTEND'])
    elif sort == "time_and_rating" or sort == "rating_and_time":
        results_with_dist = decision_maker.get_rating_with_distance(session['TIMES'])
        print(results_with_dist)
        hospitals = []
        new_ratings = []
        for hospital in results_with_dist:
            hospitals.append(hospital)
            new_ratings.append(ratings[hospital])
        results = [(hospitals[i], new_ratings[i], session['DISTANCE_STRINGS'][str(hospitals[i].id)], session['TIME_STRINGS'][str(hospitals[i].id)]) for i in range(len(hospitals))]
        # print(results)
        for i in range(len(results)):
            map_list.append((results[i][0].name, results[i][0].address, results[i][0].latitude, results[i][0].longitude, results[i][1]))
        # print(map_list)
        # print(results)
        return render_template('home.html', results=results, header="Hospitals Sorted by Time & Rating", address=session['ADDRESS'],  map_list=map_list, form=form, length=session['LENGTH'], original_length=session['ORIGINAL_LENGTH'], api_key=app.config['GOOGLE_MAPS_API_KEY_FRONTEND'])
    else:
        hospitals = [Hospital.query.get(hospital) for hospital in session['HOSPITALS']]
        new_ratings = [ratings[hospital] for hospital in hospitals]
        results = [(hospitals[i], new_ratings[i], session['DISTANCE_STRINGS'][str(hospitals[i].id)], session['TIME_STRINGS'][str(hospitals[i].id)]) for i in range(len(hospitals))]
        for i in range(len(hospitals)):
            map_list.append((hospitals[i].name, hospitals[i].address, hospitals[i].latitude, hospitals[i].longitude, results[hospitals[i]]))
        return render_template('home.html', results=results, header="Hospitals Sorted by Distance", map_list=map_list, form=form, length=session['LENGTH'], original_length=session['ORIGINAL_LENGTH'], api_key=app.config['GOOGLE_MAPS_API_KEY_FRONTEND'])


@app.route("/db", methods=['POST'])
def query_db():
    tables = {
        'Hospital': Hospital,
        'User': User,
        'Data': Data
    }

    req_data = request.get_json()
    filter_by = req_data['filter_by']
    raw_results = Search(db.session, 'application.models', (tables[req_data['table_name']],), filter_by=filter_by, all=True).results['data']
    dict_results = [{c.name: str(getattr(result, c.name)) for c in result.__table__.columns} for result in raw_results]

    return json.dumps(dict_results)
