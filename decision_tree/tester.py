from Hospital import Hospital
from Patient import Patient

hospitals = dict()
hospitals[Hospital("Hosp 1", (100, 100), 35, 397, 85, 111, 0.21, None)] = 5
hospitals[Hospital("Hosp 2", (100, 120), 85, 397, 35, 111, 0.21, None)] = 5

patient = Patient((100, 110), "car", 1, 57, ["fever", "dry cough"], "None")
patient.input_hospitals(hospitals)
patient.process()