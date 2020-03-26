from HospitalDataReader import HospitalDataReader
from CoronavirusCaseModeling import CoronavirusCaseModeling


reader = HospitalDataReader()
data, name_data, bed_data = reader.read_file("hospital_beds.csv")
growth_data = dict()
tester = CoronavirusCaseModeling()

sum = 0
for i in range(len(name_data)):
    data = tester.predict(int(bed_data[i].replace(",", "")))
    growth_data[name_data[i]] = data
    print(name_data[i], "Beds:", bed_data[i], "Days:", len(data))
    sum += data[0][0]
print(sum)
print(growth_data)
