from flask import render_template, flash, request, url_for, redirect, jsonify, session, abort
from flask_login import login_user, current_user, logout_user, login_required
from application import app, bcrypt, db
from application.models import Hospital, User, Data
from application.forms import RegistrationForm, LoginForm, DataForm, UpdateAccountForm
import geocoder, math, json
import numpy as np
from application.data_analysis import HomeDecision, PersonalDecision
from datetime import datetime
from sqlalchemy_json_querybuilder.querybuilder.search import Search


@app.route("/")
@app.route("/home", methods=['GET'])
def home():
    # print("IP:", request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
    ip = '71.191.46.159' # str(request.remote_addr)
    # g = geocoder.ip(ip)
    # print(g)
    state = 'VA' # g.state()
    session['latitude'] = 38.8809
    session['longitude'] = -77.3008 # g.latlng()
    # print(state, latitude, longitude)

    return redirect(url_for('home_state', state=state, sort="distance"))


def distance(lat1, lon1, lat2, lon2):
    R = 6373.0

    lat1 = np.deg2rad(lat1)
    lat2 = np.deg2rad(lat2)
    lon1 = np.deg2rad(lon1)
    lon2 = np.deg2rad(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

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


@app.route("/<string:state>/<string:sort>")
@app.route("/home/<string:state>/<string:sort>")
def home_state(state, sort):
    hospitals = Hospital.query.filter_by(state=state).all()
    hospitals.sort(key=lambda x: distance(session['latitude'], session['longitude'], x.latitude, x.longitude))
    hospitals = hospitals[:10]
    if sort == "rating":
        data = [Data.query.filter_by(hospital=hospital.id).order_by(Data.date.desc()).first() for hospital in hospitals]
        decision_maker = HomeDecision(hospitals, data)
        results = decision_maker.get_rating()
        hospitals = []
        ratings = []
        for hospital in results:
            hospitals.append(hospital)
            ratings.append(results[hospital])
            print(hospital, results[hospital])
        return render_template('home.html', hospitals=hospitals, ratings=ratings)
    elif sort == "distance_and_rating" or "rating_and_distance":
        data = [Data.query.filter_by(hospital=hospital.id).order_by(Data.date.desc()).first() for hospital in hospitals]
        decision_maker = HomeDecision(hospitals, data)
        distances_dict = {h: distance(session['latitude'], session['longitude'], h.latitude, h.longitude) for h in hospitals}
        results = decision_maker.get_rating_with_distance(distances_dict)
        hospitals = []
        ratings = []
        for hospital in results:
            hospitals.append(hospital)
            ratings.append(results[hospital])
            print(hospital, results[hospital], distances_dict[hospital])
        return render_template('home.html', hospitals=hospitals, ratings=ratings)
    else:
        return render_template('home.html', hospitals=hospitals, ratings=None)


@app.route("/hospital/register/admin/<string:admin_hex_id>", methods=['GET', 'POST'])
def hospital_admin_register(admin_hex_id):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    hospital = Hospital.query.filter_by(admin_hex_id=admin_hex_id).first_or_404()
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, username=form.username.data, email=form.email.data, password=hashed_password, hospital=hospital.id, is_admin=True)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', heading=hospital.name + " - Admin Registration", title="Admin Registration", form=form)


@app.route("/hospital/register/<string:normal_hex_id>", methods=['GET', 'POST'])
def hospital_normal_register(normal_hex_id):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    hospital = Hospital.query.filter_by(normal_hex_id=normal_hex_id).first_or_404()
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, username=form.username.data, email=form.email.data, password=hashed_password, hospital=hospital.id, is_admin=False)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', heading=hospital.name + " - Normal Registration", title="Normal Registration", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            hospital_name = Hospital.query.get(user.hospital).name
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Hello {user.name}! You are now logged in as {user.username} - {hospital_name}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    hospital = Hospital.query.get(current_user.hospital)
    print(hospital.id)
    form = UpdateAccountForm()

    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.username.data = current_user.username
        form.email.data = current_user.email

    if current_user.is_admin:
        users = User.query.filter_by(hospital=current_user.hospital).order_by(User.is_admin.desc()).all()
        data = Data.query.filter_by(hospital=current_user.hospital).order_by(Data.date.desc()).all()
        bed_capacity = []; beds_available = []; icus_available = []; ventilators_available = []
        coronavirus_tests_available = []; coronavirus_patients = []; coronavirus_patient_percent = []; dates = []
        for d in data:
            bed_capacity.append(d.bed_capacity); beds_available.append(d.beds_available)
            icus_available.append(d.icus_available); ventilators_available.append(d.ventilators_available)
            coronavirus_tests_available.append(d.coronavirus_tests_available); coronavirus_patients.append(d.coronavirus_patients)
            coronavirus_patient_percent.append(d.coronavirus_patient_percent*100); dates.append((d.date-datetime.utcfromtimestamp(0)).total_seconds())
        user_info = []
        for user in users:
            inputs = Data.query.filter_by(user=user.id).filter_by(hospital=hospital.id).all()
            num = len(inputs)
            if len(inputs) == 0:
                last = "N/A"
            else:
                last = Data.query.filter_by(user=user.id).filter_by(hospital=hospital.id).order_by(Data.date.desc()).first().date.strftime('%m/%d/%y')
            user_info.append((user, user.username, num, last))

        if hospital.system_open:
            admin_invite_link = "127.0.0.1:5000/hospital/register/admin/" + hospital.admin_hex_id
            user_invite_link = "127.0.0.1:5000/hospital/register/" + hospital.normal_hex_id
        else:
            admin_invite_link = ""
            user_invite_link = ""

        return render_template('admin_account.html', title='Account', form=form, hospital=hospital, data=data, users=users,
                               bed_capacity=bed_capacity, beds_available=beds_available, icus_available=icus_available,
                               ventilators_available=ventilators_available, coronavirus_tests_available=coronavirus_tests_available,
                               coronavirus_patients=coronavirus_patients, coronavirus_patient_percent=coronavirus_patient_percent,
                               dates=dates[::-1], user_info=user_info, admin_invite_link=admin_invite_link, user_invite_link=user_invite_link)
    else:
        return render_template('normal_account.html', title='Account', hospital_name=hospital.name, form=form)


@app.route("/hospital/data/<int:hospital_id>")
def hospital_data(hospital_id):
    data = Data.query.filter_by(hospital=hospital_id).order_by(Data.date.desc()).all()
    return render_template('hospital_data.html', title='Hospital Data', heading='Hospital Data - ' + Hospital.query.get(hospital_id).name, data=data)


@login_required
@app.route("/hospital/data_input", methods=["GET", "POST"])
def data_input():
    form = DataForm()
    if form.validate_on_submit():
        data = Data(bed_capacity=form.bed_capacity.data, beds_available=form.beds_available.data, icus_available=form.icus_available.data, ventilators_available=form.ventilators_available.data, coronavirus_tests_available=form.coronavirus_tests_available.data, coronavirus_patients=form.coronavirus_patients.data, coronavirus_patient_percent=form.coronavirus_patients.data/(form.bed_capacity.data-form.beds_available.data), user=current_user, hospital=current_user.hospital)
        db.session.add(data)
        db.session.commit()
        flash('Your data has been successfully uploaded to the server!', 'success')
        return redirect(url_for('account'))
    return render_template('data_input.html', title='Data Input', heading='Data Input - ' + Hospital.query.get(current_user.hospital).name, form=form)


@app.route("/patient_form", methods=["GET", "POST"])
def patient_form():
    if request.method == "POST":
        # handle form data
        return redirect(url_for('home'))
    return render_template('patient_form.html', title='Personalized Results')


@app.route("/users/<int:user_id>")
def view_user(user_id):
    requested_user = User.query.filter_by(id=user_id).first_or_404()
    if not current_user is None and (requested_user.id == current_user.id or (current_user.is_admin and requested_user.hospital == current_user.hospital)):
        return render_template('user.html', user=requested_user)
    else:
        flash('You are not authorized to access that user.', 'danger')
        return redirect(url_for('home'))


@app.route("/hospital/data/<int:data_id>/delete", methods=['POST', 'GET'])
@login_required
def delete_data(data_id):
    data = Data.query.get_or_404(data_id)
    if (current_user is None) or (current_user != User.query.get(data.user) and not (current_user.is_admin and data.hospital == current_user.hospital)):
        abort(403)
    date = data.date
    user = User.query.get(data.user).name
    db.session.delete(data)
    db.session.commit()
    flash(f'Your data submitted on {date.strftime("%m/%d")} by {user} has been deleted!', 'success')
    return redirect(url_for('account'))


@app.route("/hospital/regenerate/<int:hospital_id>", methods=["GET", "POST"])
@login_required
def regenerate_links(hospital_id):
    print('here')
    hospital = Hospital.query.get_or_404(hospital_id)
    if current_user is None or not current_user.is_admin or current_user.hospital != hospital.id:
        abort(403)
    hospital.regenerate_hex_ids()
    db.session.commit()
    flash('Your links have been regenerated! Your previous links are now inactive.', 'success')
    return redirect(url_for('account'))


@app.route("/hospital/close/<int:hospital_id>", methods=["GET", "POST"])
@login_required
def close_system(hospital_id):
    print('here')
    hospital = Hospital.query.get_or_404(hospital_id)
    if current_user is None or not current_user.is_admin or current_user.hospital != hospital.id:
        abort(403)
    hospital.close_system()
    db.session.commit()
    flash('Your hospital system is now closed! Your previous links are now inactive and no new users can join.', 'success')
    return redirect(url_for('account'))


@app.route("/hospital/open/<int:hospital_id>", methods=["GET", "POST"])
@login_required
def open_system(hospital_id):
    print('here')
    hospital = Hospital.query.get_or_404(hospital_id)
    if current_user is None or not current_user.is_admin or current_user.hospital != hospital.id:
        abort(403)
    hospital.open_system()
    db.session.commit()
    flash('Your hospital system is now open! Your most recent invitation links have been reactivated and new users can now join.', 'success')
    return redirect(url_for('account'))

@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403


@app.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500
