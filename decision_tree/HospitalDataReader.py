import pandas as pd


class HospitalDataReader:
    def __init__(self):
        pass

    def read_file(self, file_name):
        data = pd.read_csv(file_name)
        name_data = list(data["Name"])
        bed_data = list(data["Beds"])
        return data, name_data, bed_data
