import pandas as pd

class HospitalDataReader:
    def __init__(self, dir):
        self.hospital_list = self.read_file(dir)

    def read_file(self, dir):
        df = pd.read_csv(dir+"hospital_data.csv")
        hout = []
        for index, row in df.iterrows():
            name = row['Name']
            location = row['Location']
            address = row['Address']
            beds = row['Beds']
            hout.append(Hospital(name, location, address, bed))
        return hout

#h = HospitalDataReader("~/Documents/Python/decision_tree/") # for testing purposes only
