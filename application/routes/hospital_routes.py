from flask import render_template, flash, request, url_for, redirect, abort, session
from flask_login import login_user, current_user, logout_user, login_required
from application import app, bcrypt, db
from application.data_analysis import HomeDecision
from application.models import Hospital
from application.forms.hospital_forms import ResetPasswordForm, HospitalRegistrationForm, LoginForm, DataForm, UpdateAccountForm, HospitalRequestAccountForm, RequestPasswordResetForm
from datetime import datetime
from application.utils import send_hospital_request_email, send_password_reset_email
from application.utils import distance

import geocoder
import json
import operator
import random

# ROUTES 

# /hospitals
def update_address():
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

@app.route("/hospitals", methods=["GET"])
def hospitals():
    if 'UPDATE_NEEDED' not in session:
        session['UPDATE_NEEDED'] = True
        
    if 'ADDRESS' not in session:
        update_address()
    
    session['UPDATE_NEEDED'] = True
    if session['UPDATE_NEEDED'] or ('HOSPITALS' not in session or 'DATA' not in session or 'DISTANCES' not in session or 'TIMES' not in session):
        session['UPDATE_NEEDED'] = False
        hospitals = Hospital.query.all()
        hospitals = [x for x in hospitals if distance(session['LATITUDE'], session['LONGITUDE'], x.latitude, x.longitude) < 60]
        hospitals.sort(key=lambda x: distance(session['LATITUDE'], session['LONGITUDE'], x.latitude, x.longitude))
        session['ORIGINAL_LENGTH'] = len(hospitals)
        if len(hospitals) > 15:
            hospitals = hospitals[:15]
        session['LENGTH'] = len(hospitals)
        session['HOSPITALS'] = [hospital.id for hospital in hospitals]
        session['DATA'] = [hospital.data for hospital in hospitals]

        info = app.config['GOOGLE_MAPS'].distance_matrix(session['ADDRESS'], [hospital.address for hospital in hospitals], mode="driving", units="imperial")
        session['DISTANCES'] = {}
        session['TIMES'] = {}
        session['DISTANCE_STRINGS'] = {}
        session['TIME_STRINGS'] = {}
        # print(info)
        for i in range(len(info['rows'][0]['elements'])):
            if info['rows'][0]['elements'][i]['status'] == 'OK':
                session['DISTANCES'][str(session['HOSPITALS'][i])] = float(
                    info['rows'][0]['elements'][i]['distance']['text'].replace(",", "").split(" ")[0])

                arr = info['rows'][0]['elements'][i]['duration']['text'].replace(
                    ",", "").split(" ")
                if len(arr) == 2:
                    time = float(arr[0])
                elif len(arr) == 4 and arr[1].strip()[0:4] == "hour":
                    time = float(arr[0]) * 60 + float(arr[2])
                elif len(arr) == 4 and arr[1].strip()[0:3] == "day":
                    time = float(arr[0]) * 1440 + float(arr[2]) * 60
                session['TIMES'][str(session['HOSPITALS'][i])] = time

                session['DISTANCE_STRINGS'][str(
                    session['HOSPITALS'][i])] = info['rows'][0]['elements'][i]['distance']['text']
                session['TIME_STRINGS'][str(
                    session['HOSPITALS'][i])] = info['rows'][0]['elements'][i]['duration']['text']
            else:
                session['DISTANCES'][str(session['HOSPITALS'][i])] = 99999
                session['TIMES'][str(session['HOSPITALS'][i])] = 99999
                session['DISTANCE_STRINGS'][str(
                    session['HOSPITALS'][i])] = 'Error'
                session['TIME_STRINGS'][str(session['HOSPITALS'][i])] = 'Error'

    # print(session['HOSPITALS'], session['DATA'], sep="\n")

    no_data_hospitals = [session['HOSPITALS'][i] for i in range(len(session['HOSPITALS'])) if session['DATA'][i] is None]
    data_hospitals = [session['HOSPITALS'][i] for i in range(len(session['HOSPITALS'])) if session['DATA'][i] is not None]

    no_hospitals = False
    
    session['SPECIFIC_DATA'] = dict()
    results = dict()
    if len(data_hospitals) != 0:
        for hospital in data_hospitals:
            hospital = Hospital.query.get(hospital)
            if hospital.state == "FL":
                data = json.loads(hospital.data); data = data[max(data, key=float)]
                rating = data['Beds Available Percent']/15 + data['Adult ICUs Available Percent']/45 + data['Beds Available']/25
                session['SPECIFIC_DATA'][str(hospital.id)] = [data['Bed Capacity'], data['Beds Available'], data['Beds Available Percent'], data['Adult ICUs Available'], data['Adult ICUs Available Percent']]
                results[hospital] = rating
            else:
                results[hospital] = None
        results = sorted(results.items(), reverse=True, key=lambda info: info[1] - 0.1 * session['TIMES'][str(info[0].id)])
        results = {hospital[0]: hospital[1] for hospital in results}
    else:
        no_hospitals = True

    for hospital in no_data_hospitals:
        session['SPECIFIC_DATA'][str(hospital)] = None
        results[Hospital.query.get(hospital)] = None

    hospitals = []
    ratings = {}
    for hospital in results:
        hospitals.append(hospital)
        rating = results[hospital]
        if rating is None:
            rating = "No Data"
        elif rating > 7.5:
            rating = "Great"
        elif rating > 5:
            rating = "Good"
        elif rating > 2.5:
            rating = "OK"
        else:
            rating = "Low Availability"
        ratings[hospital] = rating

    map_list = [(session['ADDRESS'], session['LATITUDE'], session['LONGITUDE'])]

    results = [(hospitals[i], ratings[hospitals[i]], session['DISTANCE_STRINGS'][str(hospitals[i].id)], session['TIME_STRINGS'][str(hospitals[i].id)], session['SPECIFIC_DATA'][str(hospitals[i].id)]) for i in range(len(hospitals))]
    for i in range(len(results)):
        map_list.append((results[i][0].name, results[i][0].address, results[i][0].latitude, results[i][0].longitude, results[i][1]))
    # print(map_list)
    # print(results)
    time = float(max(json.loads(Hospital.query.get(2706).data), key=float))
    last_updated = datetime.fromtimestamp(time/1000.0)
    last_updated = last_updated.strftime('%H:%M, %m/%d')
    
    return render_template('hospitals.html', random=False, results=results, no_hospitals=no_hospitals, header="time & rating", address=session['ADDRESS'],  map_list=map_list, length=session['LENGTH'], original_length=session['ORIGINAL_LENGTH'], last_updated=last_updated, api_key=app.config['GOOGLE_MAPS_API_KEY_FRONTEND'])

@app.route("/hospitals/random", methods=["GET"])
def hospitals_address():
    addresses = [('323 Applegate Court, Miami, FL, USA 33135', 25.76193, -80.221183)]
    address, latitude, longitude = random.choice(addresses)

    hospital_list = Hospital.query.all()
    hospital_list = [x for x in hospital_list if distance(latitude, longitude, x.latitude, x.longitude) < 60]
    hospital_list.sort(key=lambda x: distance(latitude, longitude, x.latitude, x.longitude))
    original_length = len(hospital_list)
    if len(hospital_list) > 15:
        hospital_list = hospital_list[:15]
    length = len(hospital_list)
    hospitals = [hospital.id for hospital in hospital_list]
    data = [hospital.data for hospital in hospital_list]

    info = app.config['GOOGLE_MAPS'].distance_matrix(address, [hospital.address for hospital in hospital_list], mode="driving", units="imperial")
    distances = {}
    times = {}
    distance_strings = {}
    time_strings = {}
    # print(info)
    for i in range(len(info['rows'][0]['elements'])):
        if info['rows'][0]['elements'][i]['status'] == 'OK':
            distances[str(hospitals[i])] = float(info['rows'][0]['elements'][i]['distance']['text'].replace(",", "").split(" ")[0])

            arr = info['rows'][0]['elements'][i]['duration']['text'].replace(",", "").split(" ")
            if len(arr) == 2:
                time = float(arr[0])
            elif len(arr) == 4 and arr[1].strip()[0:4] == "hour":
                time = float(arr[0]) * 60 + float(arr[2])
            elif len(arr) == 4 and arr[1].strip()[0:3] == "day":
                time = float(arr[0]) * 1440 + float(arr[2]) * 60
            times[str(hospitals[i])] = time

            distance_strings[str(hospitals[i])] = info['rows'][0]['elements'][i]['distance']['text']
            time_strings[str(hospitals[i])] = info['rows'][0]['elements'][i]['duration']['text']
        else:
            distances[str(hospitals[i])] = 99999
            times[str(hospitals[i])] = 99999
            distance_strings[str(hospitals[i])] = 'Error'
            time_strings[str(hospitals[i])] = 'Error'

    # print(session['HOSPITALS'], session['DATA'], sep="\n")

    no_data_hospitals = [hospitals[i] for i in range(len(hospitals)) if data[i] is None]
    data_hospitals = [hospitals[i] for i in range(len(hospitals)) if data[i] is not None]

    no_hospitals = False

    specific_data = dict()
    results = dict()
    if len(data_hospitals) != 0:
        for hospital in data_hospitals:
            hospital = Hospital.query.get(hospital)
            if hospital.state == "FL":
                data = json.loads(hospital.data); data = data[max(data, key=float)]
                rating = data['Beds Available Percent']/15 + data['Adult ICUs Available Percent']/45 + data['Beds Available']/25
                specific_data[str(hospital.id)] = [data['Bed Capacity'], data['Beds Available'], data['Beds Available Percent'], data['Adult ICUs Available'], data['Adult ICUs Available Percent']]
                results[hospital] = rating
            else:
                results[hospital] = None
        print(results.items())
        results = sorted(results.items(), reverse=True, key=lambda info: info[1] - 0.1 * times[str(info[0].id)])
        results = {hospital[0]: hospital[1] for hospital in results}
        print(results)
    else:
        no_hospitals = True

    for hospital in no_data_hospitals:
        specific_data[str(hospital)] = None
        results[Hospital.query.get(hospital)] = None

    hospitals = []
    ratings = {}
    for hospital in results:
        hospitals.append(hospital)
        rating = results[hospital]
        if rating is None:
            rating = "No Data"
        elif rating > 7.5:
            rating = "Great"
        elif rating > 5:
            rating = "Good"
        elif rating > 2.5:
            rating = "OK"
        else:
            rating = "Low Availability"
        ratings[hospital] = rating

    map_list = [(address, latitude, longitude)]

    results = [(hospitals[i], ratings[hospitals[i]], distance_strings[str(hospitals[i].id)], time_strings[str(hospitals[i].id)], specific_data[str(hospitals[i].id)]) for i in range(len(hospitals))]
    for i in range(len(results)):
        map_list.append((results[i][0].name, results[i][0].address, results[i][0].latitude, results[i][0].longitude, results[i][1]))
    # print(map_list)
    # print(results)
    time = float(max(json.loads(Hospital.query.get(2706).data), key=float))
    last_updated = datetime.fromtimestamp(time/1000.0)
    last_updated = last_updated.strftime('%H:%M, %m/%d')

    return render_template('hospitals.html', random=True, results=results, no_hospitals=no_hospitals, header="time & rating", address=address,  map_list=map_list, length=length, original_length=original_length, last_updated=last_updated, api_key=app.config['GOOGLE_MAPS_API_KEY_FRONTEND'])