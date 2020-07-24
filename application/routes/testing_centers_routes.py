from flask import render_template, request, session, redirect, url_for, flash
from application import app, db
from application.models import TestingCenter, Submission
import time
import json 
from datetime import datetime

@app.route('/testing_centers', methods=['GET'])
def testing_centers():
    return render_template('testing_centers.html')

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
