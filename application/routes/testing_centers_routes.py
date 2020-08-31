from flask import render_template, request, session, redirect, url_for, flash
from application import app, db
from application.models import TestingCenter, Submission
import time
import json 
from datetime import datetime
import random
from application.utils import distance
from application.forms.testing_centers_forms import ReportWaitTimeForm

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
        tc_objects = [x for x in TestingCenter.query.all() if x.latitude is not None and distance(session['LATITUDE'], session['LONGITUDE'], x.latitude, x.longitude) < 60]
        session['TESTING_CENTERS'] = []

        if len(tc_objects) > 0:
            tc_objects.sort(key=lambda x: distance(session['LATITUDE'], session['LONGITUDE'], x.latitude, x.longitude))
            info = app.config['GOOGLE_MAPS'].distance_matrix(session['ADDRESS'], [tc_object.address for tc_object in tc_objects], mode="driving", units="imperial")

            for i in range(len(tc_objects)):
                tc = {}
                tc["id"] = tc_objects[i].id
                tc["name"] = tc_objects[i].name
                tc["address"] = tc_objects[i].address
                tc["lat"] = tc_objects[i].latitude
                tc["lng"] = tc_objects[i].longitude

                if info['rows'][0]['elements'][i]['status'] == 'OK':
                    tc["distance_num"] = float(info['rows'][0]['elements'][i]['distance']['text'].replace(",", "").split(" ")[0])

                    arr = info['rows'][0]['elements'][i]['duration']['text'].replace(",", "").split(" ")
                    time = 99999
                    if len(arr) == 2:
                        time = float(arr[0])
                    elif len(arr) == 4 and arr[1].strip()[0:4] == "hour":
                        time = float(arr[0]) * 60 + float(arr[2])
                    elif len(arr) == 4 and arr[1].strip()[0:3] == "day":
                        time = float(arr[0]) * 1440 + float(arr[2]) * 60
                    tc["time_num"] = time

                    tc["distance"] = info['rows'][0]['elements'][i]['distance']['text']
                    tc["time"] = info['rows'][0]['elements'][i]['duration']['text']
                else:
                    tc["distance_num"] = 99999
                    tc["time_num"] = 99999
                    tc["distance"] = "Error"
                    tc["time"] = "Error"
                
                session["TESTING_CENTERS"].append(tc)
                
    return render_template('testing_centers.html', address=session['ADDRESS'], testing_centers=session["TESTING_CENTERS"], length=len(session['TESTING_CENTERS']), random=False, api_key=app.config['GOOGLE_MAPS_API_KEY_FRONTEND'])

@app.route('/testing_centers/random')
def testing_centers_random():
    addresses = [('323 Applegate Court, Miami, FL, USA 33135', 25.76193, -80.221183)]
    address, latitude, longitude = random.choice(addresses)
    
    tc_objects = [x for x in TestingCenter.query.all() if x.latitude is not None and distance(latitude, longitude, x.latitude, x.longitude) < 60]
    tcs = []

    if len(tc_objects) > 0:
        tc_objects.sort(key=lambda x: distance(latitude, longitude, x.latitude, x.longitude))
        info = app.config['GOOGLE_MAPS'].distance_matrix(address, [tc_object.address for tc_object in tc_objects], mode="driving", units="imperial")

        for i in range(len(tc_objects)):
            tc = {}
            tc["id"] = tc_objects[i].id
            tc["name"] = tc_objects[i].name
            tc["address"] = tc_objects[i].address
            tc["lat"] = tc_objects[i].latitude
            tc["lng"] = tc_objects[i].longitude
            tc["walkUp"] = tc_objects[i].walkUp
            tc["referral"] = tc_objects[i].referral if tc_objects[i].referral is not None else False
            tc["appointment"] = tc_objects[i].appointment

            if info['rows'][0]['elements'][i]['status'] == 'OK':
                tc["distance_num"] = float(info['rows'][0]['elements'][i]['distance']['text'].replace(",", "").split(" ")[0])

                arr = info['rows'][0]['elements'][i]['duration']['text'].replace(",", "").split(" ")
                time = 99999
                if len(arr) == 2:
                    time = float(arr[0])
                elif len(arr) == 4 and arr[1].strip()[0:4] == "hour":
                    time = float(arr[0]) * 60 + float(arr[2])
                elif len(arr) == 4 and arr[1].strip()[0:3] == "day":
                    time = float(arr[0]) * 1440 + float(arr[2]) * 60
                tc["time_num"] = time

                tc["distance"] = info['rows'][0]['elements'][i]['distance']['text']
                tc["time"] = info['rows'][0]['elements'][i]['duration']['text']
            else:
                tc["distance_num"] = 99999
                tc["time_num"] = 99999
                tc["distance"] = "Error"
                tc["time"] = "Error"
            
            tcs.append(tc)
    
    return render_template('testing_centers.html', address=address, testing_centers=tcs, length=len(tcs), random=True, api_key=app.config['GOOGLE_MAPS_API_KEY_FRONTEND'])

@app.route('/testing_centers/report_wait_time/', methods=["GET", "POST"])
def report_wait_time():
    tcs = TestingCenter.query.all()
    choices = [(0, "")]
    for tc in tcs:
        choices.append((tc.id, tc.name))
    
    form = ReportWaitTimeForm()
    form.testing_center.choices = choices

    if form.validate_on_submit():
        tc_id = form.testing_center.data
        hours = form.hours.data
        minutes = form.minutes.data

        print(tc_id)
        print(hours)
        print(minutes)
        
        report_time = 60 * hours + minutes
        
        current_ip = str(request.remote_addr)
        submissions = Submission.query.filter_by(ip=current_ip).order_by(Submission.submission_time.desc()).all()

        if len(submissions) > 0 and (datetime.now() - submissions[0].submission_time).days < 1:
            flash('You may only submit wait times once per day.', 'danger')
        else:
            testing_center = TestingCenter.query.get(tc_id)
            if testing_center.data is None:
                data = dict()
            else:
                data = json.loads(testing_center.data)
            
            data[time.time()] = [report_time, current_ip]
            testing_center.data = json.dumps(data)
            submission = Submission(ip=current_ip, testing_center_name=testing_center.name)
            db.session.add(submission)
            db.session.commit()
            flash('Wait time submission recieved!', 'success')
        return redirect(url_for('testing_centers'))

    return render_template('report_wait_time.html', form=form)

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
