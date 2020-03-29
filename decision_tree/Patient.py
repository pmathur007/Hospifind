import operator
import random
import json

from Hospital import Hospital

class Patient:
    def __init__(self, transport, conditions, age, symptoms, insurance):
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
        self.max_time = 100 # maximum time people will drive

        # user data
        self.transport = transport
        self.conditions = conditions
        self.age = age
        self.symptoms_val = symptoms
        self.insurance = insurance

        # later defined data
        self.hospitals = []
        # self.symptoms_val = 0
        self.conditions_val = 0
        self.age_val = 0
        self.insurance_cat = 0
        self.corona = False
        self.risk = 0
        self.hospital_ranks = []

        # test
        self.given_hospitals = []

    def input_hospitals(self, hospitals):
        self.given_hospitals = hospitals

    def process(self):
        self.hospitals = self.get_hospitals()
        self.symptoms_val = self.calculate_symptom_score()
        self.conditions_val = self.calculate_condition_score()
        self.age_val = self.calculate_age_score()
        # self.insurance_cat = self.calculate_insurance()

        self.corona = self.symptoms_val > self.symptom_cutoff
        if self.corona:
            self.risk = (self.symptoms_val * self.symptoms_corona_weight) + (self.conditions_val * self.conditions_corona_weight) + (self.age_val * self.age_corona_weight)
        else:
            self.risk = (self.conditions_val * self.conditions_regular_weight) + (self.age_val * self.age_regular_weight)

        print("Patient Risk Factor: ", self.risk)

        # self.check_insurance()
        self.calculate_hospital_score()
        self.display_hospitals()

    def get_hospitals(self): # get it from java script
        # hospitals = dict()
        # with open("test.json") as f:
        #     hospital_data = json.load(f)
        # for hospital in hospital_data:
        #     hospitals[Hospital(hospital['Name'], hospital['Beds'], (hospital['Latitude'], hospital['Longitude']), hospital['BedsAvailable'], hospital['ICUAvailable'], hospital['VentilatorsAvailable'], hospital["TestsAvailable"], hospital["CoronavirusPatientPercent"], hospital["DaysSinceLastInput"])] = hospital["TravelTime"]
        pass

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
        for hospital in self.hospitals:
            if self.corona:
                corona_factor = hospital.corona_score * self.risk_scale * self.risk
                regular_factor = (1 - self.risk_scale * self.risk) * (self.max_time - min(self.hospitals[hospital],self.max_time))

                rating = corona_factor + regular_factor
                hospital_ranks[hospital] = rating
            else:
                risk_factor = hospital.regular_score * self.risk_scale * self.risk
                regular_factor = (1 - self.risk_scale * self.risk) * (self.max_time - min(self.hospitals[hospital],self.max_time))

                rating = risk_factor + regular_factor
                hospital_ranks[hospital] = rating
        hout = sorted(hospital_ranks.items(), reverse=True, key=operator.itemgetter(1))
        max = hout[0][1]
        for h in hout:
            self.hospital_ranks.append((h[0],(h[1] / max) * 10.0))

    def display_hospitals(self): # display hospitals in order (self.hospital_ranks) on screen
        # for h in self.hospital_ranks:
            # print(h[0].to_string() + "\nTime: " + str(self.hospitals[h[0]]) + "\nRating: " + str(round(h[1],2)) + "\n")
        with open('output.json', 'w') as fp:
            json.dump(self.hospital_ranks, fp)
