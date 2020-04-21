from flask import render_template, flash, request, url_for, redirect
from flask_login import login_user, current_user, logout_user, login_required
from application import app, bcrypt, db
from application.models import Hospital, User, Data
from application.forms import RegistrationForm, LoginForm, DataForm


@app.route("/")
@app.route("/home")
def home():
    hospitals = Hospital.query.all()
    return render_template('home.html', hospitals=hospitals)


@app.route("/home/<string:state>")
def home_state(state):
    hospitals = Hospital.query.filter_by(state=state).all()
    return render_template('home.html', hospitals=hospitals)


@app.route("/hospital/register/admin/<string:admin_hex_id>", methods=['GET', 'POST'])
def hospital_admin_register(admin_hex_id):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    hospital = Hospital.query.filter_by(admin_hex_id=admin_hex_id).first_or_404()
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, hospital=hospital.id, is_admin=True)
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
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, hospital=hospital.id, is_admin=False)
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
            flash(f'You are now logged in as {user.username} - {hospital_name}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@login_required
@app.route("/account")
def account():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    hospital_name = Hospital.query.get(current_user.hospital).name
    if current_user.is_admin:
        return render_template('admin_account.html', title='Account', hospital_name=hospital_name)
    else:
        return render_template('normal_account.html', title='Account', hospital_name=hospital_name)


@app.route("/hospital/data/<int:hospital_id>")
def hospital_data(hospital_id):
    data = Data.query.filter_by(hospital=hospital_id).order_by(Data.date.desc()).all()
    return render_template('hospital_data.html', title='Hospital Data', heading='Hospital Data - ' + Hospital.query.get(hospital_id).name, data=data)


@login_required
@app.route("/hospital/data_input", methods=["GET", "POST"])
def data_input():
    form = DataForm()
    if form.validate_on_submit():
        data = Data(bed_capacity=form.bed_capacity.data, beds_available=form.beds_available.data, icus_available=form.icus_available.data, ventilators_available=form.ventilators_available.data, coronavirus_tests_available=form.coronavirus_tests_available.data, coronavirus_patients=form.coronavirus_patients.data, hospital=current_user.hospital)
        db.session.add(data)
        db.session.commit()
        flash('Your data has been successfully uploaded to the server!', 'success')
        return redirect(url_for('home'))
    return render_template('data_input.html', title='Data Input', heading='Data Input - ' + Hospital.query.get(current_user.hospital).name, form=form)
