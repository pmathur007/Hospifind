from Hospital import Hospital
from Patient import Patient

hospitals = dict()
hospitals[Hospital("Hosp 1", (100, 100), 35, 397, 35, 111, 0.21, None)] = 10
hospitals[Hospital("Hosp 2", (100, 120), 22, 143, 12, 26, 0.50, None)] = 5

patient = Patient((100, 110), "car", 1, 57, ["fever", "dry cough"], "None")
patient.input_hospitals({Hospital("Hosp 1", (100, 100), 35, 397, 35, 111, 0.21, None): 10, Hospital("Hosp 2", (100, 120), 22, 143, 12, 26, 0.50, None): 5})
patient.process()
