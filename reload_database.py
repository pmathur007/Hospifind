from application import db
from application.models import Hospital, Data
import pandas as pd
import os
import time
import random

db.drop_all()
db.create_all()

csv_file = os.path.join(os.getcwd(), "filled_all_us_data.csv")
data = pd.read_csv(csv_file)
data = data.dropna(how='any')

count = 1
for i, row in data.iterrows():
    print(i, data['Name'][i], data['Address'][i].split(" ")[-2])
    bed_capacity = int(str(int(data['Num Beds'][i])).replace(",", ""))
    if bed_capacity != 0:
        beds_available = int(random.uniform(0.1, 0.8) * bed_capacity)
        icus_available = int(random.uniform(0.05, 0.2) * beds_available)
        ventilators_available = int(random.uniform(0.05, 0.15) * beds_available)
        coronavirus_tests_available = int(random.uniform(0.05, 0.2) * bed_capacity)
        coronavirus_patients = int(random.uniform(0.4, 0.9) * (bed_capacity - beds_available))
        coronavirus_patient_percent = round(100*coronavirus_patients/(bed_capacity-beds_available))
        hospital = Hospital(name=data['Name'][i], address=data['Address'][i], latitude=data['Lat'][i], longitude=data['Long'][i], state=data['Address'][i].split(" ")[-2])
        d = Data(bed_capacity=bed_capacity, beds_available=beds_available, icus_available=icus_available, ventilators_available=ventilators_available, coronavirus_tests_available=coronavirus_tests_available, coronavirus_patients=coronavirus_patients, coronavirus_patient_percent=coronavirus_patient_percent, user=1, hospital=count)

        db.session.add(hospital)
        db.session.add(d)

        count += 1

print(count)
db.session.commit()
