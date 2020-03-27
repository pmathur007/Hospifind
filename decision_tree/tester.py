from HospitalDataReader import HospitalDataReader
from CoronavirusCaseModeling import CoronavirusCaseModeling
import random

reader = HospitalDataReader()
data, name_data, bed_data = reader.read_file("hospital_beds.csv")
growth_data = dict()
tester = CoronavirusCaseModeling()

sum = 0
for i in range(len(name_data)):
    data = tester.predict(capacity=int(bed_data[i].replace(",", "")), start_full=random.uniform(0.5, 0.7), start_corona=random.uniform(0.05, 0.1), factor=random.uniform(1.15, 1.25), overload=1)
    growth_data[name_data[i]] = data
    print(name_data[i], bed_data[i], "Beds", len(data), "Days")
    sum += data[0][0]
print(sum)
print(growth_data)
