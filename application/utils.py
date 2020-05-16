import numpy as np
import math
from flask import url_for
from application import mail
from flask_mail import Message


def distance(lat1, lon1, lat2, lon2):
    R = 6373.0

    lat1 = np.deg2rad(lat1)
    lat2 = np.deg2rad(lat2)
    lon1 = np.deg2rad(lon1)
    lon2 = np.deg2rad(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * \
        math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def send_hospital_request_email(hospital, name, title, email, phone, message):
    msg = Message('Hospifind - New Account Request', sender='Hospifind Account Request', recipients=[
                  "ronnachum13@gmail.com", "foramritasahu@gmail.com", "arya.grayeli@gmail.com", "pranavmathur001@gmail.com", "aarav.cube@gmail.com"])
    msg.body = f'''A New User is Requesting a Hospifind Account! Here is their information:
        Hospital Name: {hospital}
        Name: {name}   Title: {title}
        Email: {email}   Phone: {phone}
        Message:
        {message}
    '''
    mail.send(msg)


def send_contact_email(name, email, subject, message):
    msg = Message('Hospifind - Contact Us Email', sender='Hospifind Contact Us Email', recipients=[
                  "ronnachum13@gmail.com", "foramritasahu@gmail.com", "arya.grayeli@gmail.com", "pranavmathur001@gmail.com", "aarav.cube@gmail.com"])
    msg.body = f'''A New User Submitted a Contact Form:
        Name: {name}
        Email: {email}
        Subject: {subject}
        Message:
        {message}
    '''
    mail.send(msg)


def send_password_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Hospifind - Password Reset Request',
                  sender='Hospifind Password Management', recipients=[user.email])
    msg.body = f'''Hello {user.name}! A password reset has been requested for your hospifind account: {user.username}.
    
    To reset your password, visit the following link:
    {url_for('reset_token', token=token, _external=True)}

    If you did not make this request then simply ignore this email and no changes will be made.

    '''

    mail.send(msg)
