import operator
import random
from math import radians, cos, sin, asin, sqrt

class Patient:
    def __init__(self, state, location, time, transport, conditions, age, symptoms, insurance):
        # hyper params for tuning
        self.insurance_cutoff = 5 # number of hospitals that match their insurance cutoff, if above then get rid of non-matches, if below keep all
        self.symptom_cutoff = 1.75 # cutoff for symptom score for coronavirus vs. non coronavirus
        self.radius = 10 # cutoff for radius in miles of what hospitals we will look at
        self.symptoms_corona_weight = 0.5 # weight value for symptom_val for coronavirus positive patient
        self.conditions_corona_weight = 0.3 # weight value for condition_val for coronavirus positive patient
        self.age_corona_weight = 0.2 # weight value for age_val for coronavirus positive patient
        self.conditions_regular_weight = 0.5 # weight value for conditions_val for regular patient
        self.age_regular_weight = 0.5 # weight value for age_val for regular patient
        self.risk_scale = 0.1 # scale that brings down risk value

        # user data
        self.state = state
        self.location = location
        self.max_time = time
        self.transport = transport
        self.conditions = conditions
        self.age = age
        self.symptoms = symptoms
        self.insurance = insurance

        # later defined data
        self.hospitals = []
        self.symptoms_val = 0
        self.conditions_val = 0
        self.age_val = 0
        self.insurance_cat = 0
        self.corona = False
        self.risk = 0
        self.hospital_times = dict()
        self.hospital_ranks = []

    def process(self):
        self.get_hospitals()

        self.symptoms_val = self.calculate_symptom_score()
        self.conditions_val = self.calculate_condition_score()
        self.age_val = self.calculate_age_score()
        self.insurance_cat = self.calculate_insurance()

        self.corona = self.symptoms_val > self.symptom_cutoff
        if self.corona:
            self.risk = (self.symptoms_val * self.symptoms_corona_weight) + (self.conditions_val * self.conditions_corona_weight) + (
                      self.age_val * self.age_corona_weight)
        else:
            self.risk = (self.conditions_val * self.conditions_regular_weight) + (self.age_val * self.age_regular_weight)

        #self.check_insurance()
        self.calculate_hospital_score()
        self.display_hospitals()

    def get_hospitals(self): # get it from java script
        pass

    def calculate_symptom_score(self): # use symptom values to determine total score
        val = 0
        symptom_dict = {"fever": 0.879, "dry cough": 0.677, "fatigue": 0.381, "phlegm": 0.334, "shortness of breath": 0.186,
                        "sore throat, headache": 0.139, "chills": 0.114, "vomiting": 0.05, "nasal congestion": 0.048, "diarrhea": 0.037}
        for symptom in self.symptoms:
            val += symptom_dict[symptom]
        return (val/2.845) * 10

    def calculate_condition_score(self): # use conditions values to determine total score
        if self.conditions == 0:
            return 0
        if self.conditions == 1:
            return 5
        if self.conditions == 2:
            return 8
        return 10

    def calculate_age_score(self): # condenses age to 0-10 scale
        return min(self.age, 100) / 10.0

    #def calculate_insurance(self): # categorizes insurance type as int
    #    return 1

    #def check_insurance(self): # check what hospitals have the patient's insurance
    #    hosp = []
    #    for h in self.hospitals:
    #        if self.insurance_cat in h.insurance:
    #            hosp.append(h)
    #    if len(hosp) > self.insurance_cutoff:
    #        self.hospitals = hosp

    def calculate_hospital_score(self): # calculates the hospitals scores
        hospital_ranks = dict()
        for h in self.hospitals:
            if self.corona:
                rating = h.per_corona * ((h.corona_score * self.risk_scale * self.risk) + (self.hospital_times[h] * (1 - self.risk_scale * self.risk)))
                hospital_ranks[h] = rating
            else:
                rating = (h.reg_score * self.risk_scale * self.risk) + (self.hospital_times[h] * (1 - self.risk_scale * self.risk))
                hospital_ranks[h] = rating

        self.hospital_ranks = sorted(hospital_ranks.items(), reverse=True, key=operator.itemgetter(1))

    def display_hospitals(self): # display hospitals in order (self.hospital_ranks) on screen
        for h in self.hospital_ranks:
            print("Hospital: " + str(h[0].name) + ", Rating: " + str(h[1]) + "\n")
