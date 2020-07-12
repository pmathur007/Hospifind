from flask import render_template, flash, request, url_for, redirect, abort
from flask_login import login_user, current_user, logout_user, login_required
from application import app, bcrypt, db
from application.models import Hospital, User, Data, Government
from application.forms.government_forms import GovernmentRequestAccountForm, GovernmentRegistrationForm
from application.utils import send_government_request_email


@app.route("/government/request_account", methods=["GET", "POST"])
def government_request_account():
    form = GovernmentRequestAccountForm()
    if form.validate_on_submit():
        send_government_request_email(form.government.data, form.government_type.data, form.name.data, form.title.data,
                                      form.email.data, form.phone.data, form.message.data)
        flash("An email has been sent to the Hospifind team for review. We will be in contact with you shortly.", 'success')
        return redirect(url_for('home'))
    return render_template('government_request_account.html', form=form)


@app.route("/government/register/<string:hex_id>", methods=["GET", "POST"])
def government_register(hex_id):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = GovernmentRegistrationForm()
    government = Government.query.filter_by(hex_id=hex_id).first_or_404()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(name=form.name.data, username=form.username.data, email=form.email.data,
                    password=hashed_password, association=government.id, user_type="Government")
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', heading=government.name + " - User Registration", form=form)
