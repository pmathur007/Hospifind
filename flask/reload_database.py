from application import db
from application.models import Hospital
import pandas as pd

db.drop_all()
db.create_all()

# csv_file = "C:\\Users\\Ron\\Hospifind\\decision_tree\\us_data.csv"
csv_file = "/Users/pranav/Documents/Development/WHOCorona/decision_tree/us_data.csv"

data = pd.read_csv(csv_file)

names = list(data['Name'])
address = list(data['Address'])
latitude = list(data['Latitude'])
longitude = list(data['Longitude'])
state = [a.split(" ")[-2] for a in address]

for i in range(len(names)):
    if len(state[i]) == 2:
        db.session.add(Hospital(name=names[i], address=address[i], latitude = latitude[i], longitude = longitude[i], state=state[i]))
db.session.commit()
