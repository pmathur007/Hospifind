from application import app, db
from application.models import TestingCenter
import pandas as pd
import os
import time
import random
from string import * 
import geocoder 

csv_file = os.path.join(os.getcwd(), "data", "florida_testcenter_data.csv")
print(csv_file)

data = pd.read_csv(csv_file, encoding='unicode_escape')
data = data.dropna(how='any')

for t in TestingCenter.query.all():
    db.session.delete(t)
db.session.commit()

count = 1
for i, row in data.iterrows():
    address = capwords(row[1]) + ", " + row[2].title() + ", " + row[4]
    g = geocoder.google(address, key=app.config["GOOGLE_MAPS_API_KEY_BACKEND"])
    # print(g.url)
    if g.ok:
        lat, long = g.latlng
    else:
        lat, long = None, None
    testCenter = TestingCenter(name=row[0].title(), address=address, state=row[4], county=row[3].title(), walkUp = (row[7] == 'Walk-Up'), appointment = row[6], referral = None, info = None, hours = None, latitude=lat, longitude=long, data=None)
    # print(testCenter)
    db.session.add(testCenter)
    count += 1

db.session.commit()
