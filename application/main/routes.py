import json
import geocoder
from flask import render_template, request, session
from sqlalchemy_json_querybuilder.querybuilder.search import Search
from application import app, db
from application.data_analysis import HomeDecision
from application.models import User, Hospital, Data
from application.utils import distance


@app.route("/")
@app.route("/home", methods=['GET'])
def home():
    if 'ADDRESS' not in session:
        session['IP'] = str(request.remote_addr)
        g = geocoder.ip(session['IP'])
        if g.ok and len(g.latlng) == 2 and g.latlng[0] is not None and g.latlng[1] is not None:
            session['ADDRESS'] = g.city + ", " + g.state + ", " + g.country
            session['CITY'] = g.city
            session['STATE'] = g.state
            session['COUNTRY'] = g.country
            latlng = g.latlng
        else:
            session['ADDRESS'] = "FAILURE"
            latlng = [38.8809, -77.3008]
        session['LATITUDE'] = latlng[0]
        session['LONGITUDE'] = latlng[1]
    print(session['LATITUDE'])
    print(session['LONGITUDE'])
    # print(state, latitude, longitude)

    if 'HOSPITALS' not in session or 'DATA' not in session or 'DISTANCES' not in session:
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
        return render_template('home.html', results=results, header="Hospitals Sorted by Distance & Rating", address=session['ADDRESS'])
    else:
        hospitals = [Hospital.query.get(hospital) for hospital in session['HOSPITALS']]
        new_ratings = [ratings[hospital] for hospital in hospitals]
        results = {hospitals[i] : new_ratings[i] for i in range(len(hospitals))}
        return render_template('home.html', results=results, header="Hospitals Sorted by Distance")


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
