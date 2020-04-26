from application import db
from application.models import Hospital, Data
import pandas as pd
import os
import time
import random

db.drop_all()
db.create_all()

csv_file = os.path.join(os.path.dirname(os.getcwd()), "decision_tree", "us_data.csv")
data = pd.read_csv(csv_file)

names = list(data['Name'])
address = list(data['Address'])
latitude = list(data['Latitude'])
longitude = list(data['Longitude'])
capacity = list(data['Beds'])
state = [a.split(" ")[-2] for a in address]

count = 1
for i in range(len(names)):
    if len(state[i]) == 2:
        bed_capacity = int(capacity[i].replace(",", ""))
        beds_available = int(random.uniform(0.1, 0.8) * bed_capacity)
        icus_available = int(random.uniform(0.05, 0.2) * beds_available)
        ventilators_available = int(random.uniform(0.05, 0.15) * beds_available)
        coronavirus_tests_available = int(random.uniform(0.05, 0.2) * bed_capacity)
        coronavirus_patients = int(random.uniform(0.4, 0.9) * (bed_capacity - beds_available))
        coronavirus_patient_percent = round(coronavirus_patients/(bed_capacity-beds_available), 2)

        hospital = Hospital(name=names[i], address=address[i], latitude = latitude[i], longitude = longitude[i], state=state[i])
        data = Data(bed_capacity=bed_capacity, beds_available=beds_available, icus_available=icus_available, ventilators_available=ventilators_available, coronavirus_tests_available=coronavirus_tests_available, coronavirus_patients=coronavirus_patients, coronavirus_patient_percent=coronavirus_patient_percent, user=1, hospital=count)

        db.session.add(hospital)
        db.session.add(data)

        count += 1
db.session.commit()
