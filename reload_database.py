from application import db
from application.models import Hospital
import pandas as pd
import os
import time
import random
from string import * 

db.drop_all()
db.create_all()

csv_file = os.path.join(os.getcwd(), "data", "newest_us_data.csv")
print(csv_file)
data = pd.read_csv(csv_file, encoding='unicode_escape')
data = data.dropna(how='any')

count = 1
for i, row in data.iterrows():
    hospital = Hospital(name=row[0].title(), address=capwords(row[1]) + ", " + row[2].title() + ", " + row[3], state=row[3], county=row[9].title(), latitude=row[10], longitude=row[11], data=None)
    db.session.add(hospital)
    count += 1

print(count)
db.session.commit()
