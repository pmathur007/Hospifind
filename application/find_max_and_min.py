from application import db
from application.models import Hospital, Data

hospital_data = [Data.query.filter_by(hospital=hospital.id).order_by(Data.date.desc()).first() for hospital in Hospital.query.all()]
data = [(d.bed_capacity, d.beds_available, d.icus_available, d.ventilators_available, d.coronavirus_tests_available, d.coronavirus_patients, d.coronavirus_patient_percent) for d in hospital_data]
max_bed_capacity = max(data, key=lambda x: x[0])[0]; min_bed_capacity = min(data, key=lambda x: x[0])[0]
max_beds_available = max(data, key=lambda x: x[1])[1]; min_beds_available = min(data, key=lambda x: x[1])[1]
max_icus_available = max(data, key=lambda x: x[2])[2]; min_icus_available = min(data, key=lambda x: x[2])[2]
max_ventilators_available = max(data, key=lambda x: x[3])[3]; min_ventilators_available = min(data, key=lambda x: x[3])[3]
max_coronavirus_tests_available = max(data, key=lambda x: x[4])[4]; min_coronavirus_tests_available = min(data, key=lambda x: x[4])[4]
max_coronavirus_patients = max(data, key=lambda x: x[5])[5]; min_coronavirus_patients = min(data, key=lambda x: x[5])[5]
max_coronavirus_patient_percent = max(data, key=lambda x: x[6])[6]; min_coronavirus_patient_percent = min(data, key=lambda x: x[6])[6]

print(f"Capacity: {min_bed_capacity} - {max_bed_capacity}")
print(f"Beds Available: {min_beds_available} - {max_beds_available}")
print(f"ICUs Available: {min_icus_available} - {max_icus_available}")
print(f"Ventilators Available: {min_ventilators_available} - {max_ventilators_available}")
print(f"Coronavirus Tests Available: {min_coronavirus_tests_available} - {max_coronavirus_tests_available}")
print(f"Coronavirus Patients: {min_coronavirus_patients} - {max_coronavirus_patients}")
print(f"Coronavirus Patient Percent: {min_coronavirus_patient_percent} - {max_coronavirus_patient_percent}")

# print(hospital_data)
