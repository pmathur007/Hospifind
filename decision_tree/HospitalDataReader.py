import pandas as pd

class HospitalDataReader:
    def __init__(self, state, dir):
        self.hospital_list = self.read_file(state, dir)

    def read_file(self, state, dir):
        df = pd.read_csv(dir+str(state).lower()+"_data.csv")
        hout = []
        for index, row in df.iterrows():
            name = row['Name']
            location = row['Location']
            vent = row['Ventilators Available']
            beds = row['Beds']
            icu = row['ICUs Available']
            tests = row['Number of Corona Tests']
            coron = row['Percent Coronavirus Cases']
            insurance = row['Insurance Covered']
            hout.append(Hospital(name, location, vent, bed, icu, tests, coron, insurance))
        return hout

#h = HospitalDataReader("ny","~/Documents/Python/decision_tree/") # for testing purposes only
