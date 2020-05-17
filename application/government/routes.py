from flask import render_template, flash, request, url_for, redirect, abort
from flask_login import login_user, current_user, logout_user, login_required
from application import app, bcrypt, db
from application.models import Hospital, User, Data
from application.government.forms import GovernmentRequestAccountForm
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
