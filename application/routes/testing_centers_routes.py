from flask import render_template, request, session, redirect, url_for, flash
from application import app, db
from application.models import TestingCenter, Submission
import time
import json 
from datetime import datetime
from application.utils import distance

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

@app.route('/testing_centers', methods=['GET'])
def testing_centers():
    if 'UPDATE_NEEDED' not in session:
        session['UPDATE_NEEDED'] = True
        
    if 'ADDRESS' not in session:
        update_address()
    
    session['UPDATE_NEEDED'] = True
    if session['UPDATE_NEEDED'] or 'TESTING_CENTERS' not in session:
        session['UPDATE_NEEDED'] = False
        testing_centers = TestingCenter.query.all()
        testing_centers = [x for x in testing_centers if distance(session['LATITUDE'], session['LONGITUDE'], x.latitude, x.longitude) < 60]
        testing_centers.sort(key=lambda x: distance(session['LATITUDE'], session['LONGITUDE'], x.latitude, x.longitude))
        session['TESTING_CENTERS'] = [testing_center.id for testing_center in testing_centers]
        session['TESTING_CENTERS_MAP_LIST'] = [[t.address, t.latitude, t.longitude] for t in testing_centers]

        info = app.config['GOOGLE_MAPS'].distance_matrix(session['ADDRESS'], [testing_center.address for testing_center in testing_centers], mode="driving", units="imperial")
        session['TESTING_CENTERS_DISTANCES'] = []
        session['TESTING_CENTERS_TIMES'] = []
        session['TESTING_CENTERS_DISTANCE_STRINGS'] = []
        session['TESTING_CENTERS_TIME_STRINGS'] = []

        for i in range(len(info['rows'][0]['elements'])):
            if info['rows'][0]['elements'][i]['status'] == 'OK':
                session['TESTING_CENTER_DISTANCES'].append(float(info['rows'][0]['elements'][i]['distance']['text'].replace(",", "").split(" ")[0]))
                arr = info['rows'][0]['elements'][i]['duration']['text'].replace(",", "").split(" ")
                if len(arr) == 2:
                    time = float(arr[0])
                elif len(arr) == 4 and arr[1].strip()[0:4] == "hour":
                    time = float(arr[0]) * 60 + float(arr[2])
                elif len(arr) == 4 and arr[1].strip()[0:3] == "day":
                    time = float(arr[0]) * 1440 + float(arr[2]) * 60
                session['TESTING_CENTER_TIMES'].append(time)

                session['TESTING_CENTER_DISTANCE_STRINGS'].append(info['rows'][0]['elements'][i]['distance']['text'])
                session['TESTING_CENTER_TIME_STRINGS'].append(info['rows'][0]['elements'][i]['duration']['text'])
            else:
                session['TESTING_CENTER_DISTANCES'].append(99999)
                session['TESTING_CENTER_TIMES'].append(99999)
                session['TESTING_CENTER_DISTANCE_STRINGS'].append('Error')
                session['TESTING_CENTER_TIME_STRINGS'].append('Error')

    testing_centers = [TestingCenter.query.get(i) for i in session['TESTING_CENTERS']]
    return render_template('testing_centers.html', address=session['ADDRESS'], testing_centers=testing_centers, distances=session['TESTING_CENTER_DISTANCES'], times=session['TESTING_CENTER_TIMES'], distance_strings=session['TESTING_CENTER_DISTANCE_STRINGS'], time_strings=session['TESTING_CENTER_TIME_STRINGS'], map_list=session['TESTING_CENTERS_MAP_LIST'], api_key=app.config['GOOGLE_MAPS_API_KEY_FRONTEND'])

@app.route('/testing_centers/report_wait_time/<int:id>/<int:report>')
def wait_time_submission(id, report):
    current_ip = str(request.remote_addr)
    submissions = Submission.query.filter_by(ip=current_ip).order_by(Submission.submission_time.desc()).all()

    if len(submissions) > 0 and (datetime.now() - submissions[0].submission_time).days < 1:
        flash('You may only submit wait times once per day.', 'danger')
    else:
        testing_center = TestingCenter.query.get(id)
        if testing_center.data is None:
            data = dict()
        else:
            data = json.loads(testing_center.data)
        data[time.time()] = [report, current_ip]
        testing_center.data = json.dumps(data)
        submission = Submission(ip=current_ip, testing_center_name=testing_center.name)
        db.session.add(submission)
        db.session.commit()
        flash('Wait time submission recieved!', 'success')
    return render_template('testing_centers.html')
