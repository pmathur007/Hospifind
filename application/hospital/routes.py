from flask import render_template, flash, request, url_for, redirect, abort
from flask_login import login_user, current_user, logout_user, login_required
from application import app, bcrypt, db
from application.models import Hospital, User, Data, Government
from application.hospital.forms import ResetPasswordForm, HospitalRegistrationForm, LoginForm, DataForm, UpdateAccountForm, HospitalRequestAccountForm, RequestPasswordResetForm
from datetime import datetime
from application.utils import send_hospital_request_email, send_password_reset_email


@app.route("/hospital/request_account", methods=["GET", "POST"])
def hospital_request_account():
    form = HospitalRequestAccountForm()
    if form.validate_on_submit():
        send_hospital_request_email(form.hospital.data, form.name.data, form.title.data,
                                    form.email.data, form.phone.data, form.message.data)
        flash("An email has been sent to the Hospifind team for review. We will be in contact with you shortly.", 'success')
        return redirect(url_for('home'))
    return render_template('hospital_request_account.html', form=form)


@app.route("/hospital/register/admin/<string:admin_hex_id>", methods=['GET', 'POST'])
def hospital_admin_register(admin_hex_id):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    hospital = Hospital.query.filter_by(
        admin_hex_id=admin_hex_id).first_or_404()
    form = HospitalRegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(name=form.name.data, username=form.username.data, email=form.email.data,
                    password=hashed_password, association=hospital.id, user_type="Admin")
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', heading=hospital.name + " - Admin Registration", title="Admin Registration", form=form)


@app.route("/hospital/register/<string:normal_hex_id>", methods=['GET', 'POST'])
def hospital_normal_register(normal_hex_id):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    hospital = Hospital.query.filter_by(
        normal_hex_id=normal_hex_id).first_or_404()
    form = HospitalRegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(name=form.name.data, username=form.username.data, email=form.email.data,
                    password=hashed_password, association=hospital.id, user_type="Normal")
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('login'))
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
            if user.user_type == "Government":
                assocation = Government.query.get(user.association).name
            else:
                assocation = Hospital.query.get(user.association).name
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Hello ' + user.name + '! You are now logged in as ' +
                  user.username + ' - ' + assocation + '!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('account'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    if current_user.user_type == "Government":
        return render_template('government_account.html')
    else:
        hospital = Hospital.query.get(current_user.association)
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

        if current_user.user_type == "Admin":
            users = User.query.filter_by(association=current_user.association).order_by(
                User.user_type.desc()).all()
            data = Data.query.filter_by(
                hospital=current_user.association).order_by(Data.date.desc()).all()
            bed_capacity = []
            beds_available = []
            icus_available = []
            ventilators_available = []
            coronavirus_tests_available = []
            coronavirus_patients = []
            coronavirus_patient_percent = []
            dates = []
            for d in data:
                bed_capacity.append(d.bed_capacity)
                beds_available.append(d.beds_available)
                icus_available.append(d.icus_available)
                ventilators_available.append(d.ventilators_available)
                coronavirus_tests_available.append(
                    d.coronavirus_tests_available)
                coronavirus_patients.append(d.coronavirus_patients)
                coronavirus_patient_percent.append(
                    d.coronavirus_patient_percent*100)
                dates.append(
                    (d.date-datetime.utcfromtimestamp(0)).total_seconds())
            user_info = []
            for user in users:
                inputs = Data.query.filter_by(user=user.id).all()
                num = len(inputs)
                if len(inputs) == 0:
                    last = "N/A"
                else:
                    last = Data.query.filter_by(user=user.id).filter_by(hospital=hospital.id).order_by(
                        Data.date.desc()).first().date.strftime('%m/%d/%y')
                user_info.append((user, user.username, num, last))

            if hospital.system_open:
                admin_invite_link = url_for(
                    'hospital_admin_register', admin_hex_id=hospital.admin_hex_id, _external=True)
                user_invite_link = url_for(
                    'hospital_normal_register', normal_hex_id=hospital.normal_hex_id, _external=True)
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
    data = Data.query.filter_by(
        hospital=hospital_id).order_by(Data.date.desc()).all()
    return render_template('hospital_data.html', title='Hospital Data', heading='Hospital Data - ' + Hospital.query.get(hospital_id).name, data=data)


@login_required
@app.route("/hospital/data_input", methods=["GET", "POST"])
def data_input():
    form = DataForm()
    if form.validate_on_submit():
        data = Data(bed_capacity=form.bed_capacity.data, beds_available=form.beds_available.data, icus_available=form.icus_available.data, ventilators_available=form.ventilators_available.data, coronavirus_tests_available=form.coronavirus_tests_available.data,
                    coronavirus_patients=form.coronavirus_patients.data, coronavirus_patient_percent=form.coronavirus_patients.data/(form.bed_capacity.data-form.beds_available.data), user=current_user, hospital=current_user.association)
        db.session.add(data)
        db.session.commit()
        flash('Your data has been successfully uploaded to the server!', 'success')
        return redirect(url_for('account'))
    return render_template('data_input.html', title='Data Input', heading='Data Input - ' + Hospital.query.get(current_user.association).name, form=form)


@app.route("/users/<int:user_id>")
def view_user(user_id):
    requested_user = User.query.filter_by(id=user_id).first_or_404()
    if not current_user is None and (requested_user.id == current_user.id or (current_user.user_type == "Admin" and requset_user.user_type != "Government" and requested_user.association == current_user.association)):
        return render_template('user.html', user=requested_user)
    else:
        flash('You are not authorized to access that user.', 'danger')
        return redirect(url_for('home'))


@app.route("/hospital/data/<int:data_id>/delete", methods=['POST', 'GET'])
@login_required
def delete_data(data_id):
    data = Data.query.get_or_404(data_id)
    if (current_user is None) or (current_user != User.query.get(data.user) and not (current_user.user_type == "Admin" and data.hospital == current_user.hospital)):
        abort(403)
    date = data.date
    user = User.query.get(data.user).name
    db.session.delete(data)
    db.session.commit()
    flash('Your data submitted on ' + date.strftime("%m/%d") +
          ' by {user} has been deleted!', 'success')
    return redirect(url_for('account'))


@app.route("/hospital/regenerate/<int:hospital_id>", methods=["GET", "POST"])
@login_required
def regenerate_links(hospital_id):
    hospital = Hospital.query.get_or_404(hospital_id)
    if current_user is None or current_user.user_type != "Admin" or current_user.association != hospital.id:
        abort(403)
    hospital.regenerate_hex_ids()
    db.session.commit()
    flash('Your links have been regenerated! Your previous links are now inactive.', 'success')
    return redirect(url_for('account'))


@app.route("/hospital/close/<int:hospital_id>", methods=["GET", "POST"])
@login_required
def close_system(hospital_id):
    hospital = Hospital.query.get_or_404(hospital_id)
    if current_user is None or current_user.user_type != "Admin" or current_user.association != hospital.id:
        abort(403)
    hospital.close_system()
    db.session.commit()
    flash('Your hospital system is now closed! Your previous links are now inactive and no new users can join.', 'success')
    return redirect(url_for('account'))


@app.route("/hospital/open/<int:hospital_id>", methods=["GET", "POST"])
@login_required
def open_system(hospital_id):
    hospital = Hospital.query.get_or_404(hospital_id)
    if current_user is None or current_user.user_type != "Admin" or current_user.association != hospital.id:
        abort(403)
    hospital.open_system()
    db.session.commit()
    flash('Your hospital system is now open! Your most recent invitation links have been reactivated and new users can now join.', 'success')
    return redirect(url_for('account'))


@app.route("/request_password_reset", methods=['GET', 'POST'])
def request_password_reset():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestPasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_password_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('request_password_reset.html', title='Password Reset Request', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_password_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in.', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
