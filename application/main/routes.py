import math
import numpy as np
from flask import render_template, request, url_for, redirect, session
from application import app
from application.data_analysis import HomeDecision
from application.models import Hospital, Data


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


@app.route("/")
@app.route("/home", methods=['GET'])
def home():
    print("IP: " + str(request.remote_addr))
    session['IP'] = '71.191.46.159'  # str(request.remote_addr)
    # g = geocoder.ip(ip)
    # print(g)
    state = 'VA'  # g.state()
    session['LATITUDE'] = 38.8809
    session['LONGITUDE'] = -77.3008  # g.latlng()
    # print(state, latitude, longitude)

    if session.get('HOSPITALS') is None or session.get('DATA') is None or session.get('DISTANCES') is None:
        hospitals = Hospital.query.all()
        hospitals.sort(key=lambda x: distance(session['LATITUDE'], session['LONGITUDE'], x.latitude, x.longitude))
        hospitals = hospitals[:10]
        session['HOSPITALS'] = [hospital.id for hospital in hospitals]
        data = [Data.query.filter_by(hospital=hospital.id).order_by(Data.date.desc()).first() for hospital in hospitals]
        session['DATA'] = [d.id for d in data]

    decision_maker = HomeDecision([Hospital.query.get(hospital) for hospital in session['HOSPITALS']], [Data.query.get(data) for data in session['DATA']])
    results = decision_maker.get_rating()

    hospitals = []
    ratings = {}
    for hospital in results:
        hospitals.append(hospital)
        rating = results[hospital]
        if rating > 8:
            rating = "Great"
        elif rating > 5:
            rating = "Good"
        elif rating > 1:
            rating = "OK"
        else:
            rating = "Low Availability"
        ratings[hospital] = rating

    sort = "distance_and_rating"
    if sort == "rating":
        new_ratings = [ratings[hospital] for hospital in ratings]
        results = {hospitals[i]: new_ratings[i] for i in range(len(hospitals))}
        return render_template('home.html', results=results, header="Hospitals Sorted by Rating")
    elif sort == "distance_and_rating" or sort == "rating_and_distance":
        distances = [distance(session['LATITUDE'], session['LONGITUDE'], Hospital.query.get(hosp).latitude, Hospital.query.get(hosp).longitude) for hosp in session['HOSPITALS']]
        results_with_dist = decision_maker.get_rating_with_distance(distances)
        hospitals = []
        new_ratings = []
        for hospital in results_with_dist:
            hospitals.append(hospital)
            new_ratings.append(ratings[hospital])
        results = {hospitals[i]: new_ratings[i] for i in range(len(hospitals))}
        return render_template('home.html', results=results, header="Hospitals Sorted by Distance AND Rating")
    else:
        hospitals = [Hospital.query.get(hospital) for hospital in session['HOSPITALS']]
        new_ratings = [ratings[hospital] for hospital in hospitals]
        results = {hospitals[i] : new_ratings[i] for i in range(len(hospitals))}
        return render_template('home.html', results=results, header="Hospitals Sorted by Distance")


# @app.route("/db", methods=['POST'])
# def query_db():
#     tables = {
#         'Hospital': Hospital,
#         'User': User,
#         'Data': Data
#     }
#
#     req_data = request.get_json()
#
#     filter_by = req_data['filter_by']
#
#     raw_results = Search(db.session, 'application.models', (tables[req_data['table_name']],), filter_by=filter_by, all=True).results['data']
#
#     dict_results = [{c.name: str(getattr(result, c.name)) for c in result.__table__.columns} for result in raw_results]
#
#     return json.dumps(dict_results)