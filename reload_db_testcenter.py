from application import db
from application.models import TestingCenter
import pandas as pd
import os
import time
import random
from string import * 

csv_file = os.path.join(os.getcwd(), "data", "florida_testcenter_data.csv")
print(csv_file)

data = pd.read_csv(csv_file, encoding='unicode_escape')
data = data.dropna(how='any')

count = 1
for i, row in data.iterrows():
    testCenter = TestingCenter(name=row[0].title(), address=capwords(row[1]) + ", " + row[2].title() + ", " + row[4], state=row[4], county=row[3].title(), walkUp = (row[7] == 'Walk-Up'), appointment = row[6], referral = None, info = None, hours = None, latitude=None, longitude=None, data=None)
    db.session.add(testCenter)
    count += 1

print(count)
db.session.commit()
