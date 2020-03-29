from Hospital import Hospital
from Patient import Patient

hospitals = dict()
hospitals[Hospital("Hosp 1", 500, (100, 100), 397, 85, 35, 111, 0.21, -1)] = 5
hospitals[Hospital("Hosp 2", 500, (100, 120), 150, 35, 75, 150, 0.14, 1)] = 5

patient = Patient((100, 110), "car", 1, 57, ["fever", "dry cough"], "None")
patient.input_hospitals(hospitals)
patient.process()