from application import db
from application.models import Hospital, Data
import random
from datetime import datetime
from datetime import timedelta

hospitals = Hospital.query.all()

num_hosp = len(hospitals)

for i in range(1, num_hosp+1):
    bed_capacity = int(Data.query.filter_by(hospital=i).first().bed_capacity)
    for num in range(-15, 0):
        beds_available = int(random.uniform(0.1, 0.8) * bed_capacity)
        icus_available = int(random.uniform(0.05, 0.2) * beds_available)
        ventilators_available = int(random.uniform(0.05, 0.15) * beds_available)
        coronavirus_tests_available = int(random.uniform(0.05, 0.2) * bed_capacity)
        coronavirus_patients = int(random.uniform(0.4, 0.9) * (bed_capacity - beds_available))
        coronavirus_patient_percent = round(100*(round(coronavirus_patients / (bed_capacity - beds_available), 2)))

        data = Data(bed_capacity=bed_capacity, beds_available=beds_available, icus_available=icus_available,
                ventilators_available=ventilators_available, coronavirus_tests_available=coronavirus_tests_available,
                coronavirus_patients=coronavirus_patients, coronavirus_patient_percent=coronavirus_patient_percent,
                user=1, hospital=i, date=datetime.utcnow() + timedelta(days=num))

        db.session.add(data)

db.session.commit()
