import pandas as pd 
import os 
from datetime import datetime 
from pytz import timezone
import json
from application import db
from application.models import Hospital

tz = timezone('US/Eastern')

path = "C:\\Users\\Ron\\Hospifind\\data"
beds = os.path.join(path, "flhospitals722.csv")
icus = os.path.join(path, "flicus722.csv")

beds = pd.read_csv(beds, delimiter='\t', encoding='utf-16')
icus = pd.read_csv(icus, delimiter='\t', encoding='utf-16') 

hospitals = list(beds['ProviderName']); hospitals = [hospital.title() for hospital in hospitals]
bed_capacity = list(beds['Bed Census']); bed_capacity = [int(i.replace(',', '')) if not isinstance(i, int) else i for i in bed_capacity]
beds_available = list(beds['Available']); beds_available = [int(i.replace(',', '')) if not isinstance(i, int) else i for i in beds_available]
beds_percent_available = list(beds['Available Capacity']); beds_percent_available = [float(i.replace('%', '')) if isinstance(i, str) else 0 for i in beds_percent_available]

adult_icu_capacity = list(icus['Adult ICU Census']); adult_icu_capacity = [int(i.replace(',', '')) if not isinstance(i, int) else i for i in adult_icu_capacity]
adult_icus_available = list(icus['Available Adult ICU']); adult_icus_available = [int(i.replace(',', '')) if not isinstance(i, int) else i for i in adult_icus_available]
adult_icus_percent_available = list(icus['Available Adult ICU%']); adult_icus_percent_available = [float(i.replace('%', '')) if isinstance(i, str) else 0 for i in adult_icus_percent_available]

count = 0
for i, hospital in enumerate(hospitals):
    if len(Hospital.query.filter_by(name=hospital).all()) > 0:
        hospital = Hospital.query.filter_by(name=hospital).first()
        if hospital.data is None:
            data = dict()
        else:
            data = hospital.data.__dict__        
        time = datetime.now(tz).timestamp() * 1000
        data[time] = dict()
        data[time]["Bed Capacity"] = bed_capacity[i]
        data[time]["Beds Available"] = beds_available[i]
        data[time]["Beds Available Percent"] = beds_percent_available[i]
        data[time]["Adult ICU Capacity"] = adult_icus_percent_available[i]
        data[time]["Adult ICUs Available"] = adult_icus_available[i]
        data[time]["Adult ICUs Available Percent"] = adult_icus_percent_available[i]

        data_json = json.dumps(data)
        print(data_json)
        hospital.data = data_json
        
db.session.commit()
print(time)
print(count, len(hospitals))