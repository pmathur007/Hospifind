import math
import numpy as np
from flask import render_template, request, url_for, redirect, session
from application import app
from application.data_analysis import HomeDecision
from application.models import Hospital, Data


@app.route("/")
@app.route("/home", methods=['GET'])
def home():
    print("IP: " + str(request.remote_addr))
    ip = '71.191.46.159'  # str(request.remote_addr)
    # g = geocoder.ip(ip)
    # print(g)
    state = 'VA'  # g.state()
    session['latitude'] = 38.8809
    session['longitude'] = -77.3008  # g.latlng()
    # print(state, latitude, longitude)
    hospitals = Hospital.query.all()
    hospitals.sort(key=lambda x: distance(session['latitude'], session['longitude'], x.latitude, x.longitude))
    hospitals = hospitals[:10]

    sort = ""
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
    elif sort == "distance_and_rating" or sort == "rating_and_distance":
        data = [Data.query.filter_by(hospital=hospital.id).order_by(Data.date.desc()).first() for hospital in hospitals]
        decision_maker = HomeDecision(hospitals, data)
        distances_dict = {h: distance(session['latitude'], session['longitude'], h.latitude, h.longitude) for h in
                          hospitals}
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