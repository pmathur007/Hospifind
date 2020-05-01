import random
import operator
from application.models import Hospital


class Patient:
    def __init__(self, symptoms, age, under_conditions):
        self.symptoms = symptoms
        self.age = age
        self.under_conditions = under_conditions

    def info(self):
        s = ""
        for i in self.symptoms:
            s+=str(i)+","
        return s+str(self.age)+","+str(self.under_conditions)


class Hospital:
    def __init__(self, capacity, beds, icus, vents, tests, corona_percent):
        self.capacity = capacity
        self.beds = beds
        self.icus = icus
        self.vents = vents
        self.tests = tests
        self.corona_percent = corona_percent/100

    def info(self):
        return ""+str(self.capacity)+","+str(self.beds)+","+str(self.icus)+","+str(self.vents)+","+str(self.tests)+","+str(self.corona_percent)


class HomeDecision:
    def __init__(self, hospitals, data):
        self.hospitals = hospitals
        self.data = data
        self.ratings = {}

        # hyperparams
        self.capacity_weight = 1
        self.beds_weight = 4
        self.icus_weight = 2
        self.vents_weight = 1.5
        self.tests_weight = 1.5
        self.distance_weight = 5

        self.base = 1.1

    def get_rating(self):
        capacities = self.scale_capacity()
        beds = self.scale_beds()
        icus = self.scale_icus()
        vents = self.scale_vents()
        tests = self.scale_tests()
        ratings = {}

        for i in range(len(self.data)):
            ncap = self.capacity_weight * capacities[i]
            nbeds = self.beds_weight * beds[i]
            nicus = self.icus_weight * icus[i]
            nvents = self.vents_weight * vents[i]
            ntests = self.tests_weight * tests[i]
            rating = ncap + nbeds + nicus + nvents + ntests
            ratings[self.hospitals[i]] = rating

        ratings = sorted(ratings.items(), reverse=True, key=operator.itemgetter(1))
        for i in ratings:
            self.ratings[i[0]] = round(i[1],2)
        return self.ratings

    def get_rating_with_distance(self, distances_dict):
        if not bool(self.ratings):
            self.get_rating()
        distances = self.scale_distance(distances_dict)

        nratings = {}
        for i in range(len(self.hospitals)):
            ndis = self.distance_weight * distances[i]
            rating = self.ratings[self.hospitals[i]]
            nrating = ndis + rating
            nratings[self.hospitals[i]] = nrating

        nratings = sorted(nratings.items(), reverse=True, key=operator.itemgetter(1))

        out = {}
        for h in nratings:
            out[h[0]] = round(h[1],2)
        return out

    def scale_capacity(self):
        lst = [self.data[i].bed_capacity for i in range(len(self.data))]
        max_val = max(lst); min_val = min(lst)
        out = [(n - min_val) / (max_val - min_val) for n in lst]
        return out

    def scale_beds(self):
        lst = [self.data[i].beds_available for i in range(len(self.data))]
        max_val = max(lst); min_val = min(lst)
        out = [(n - min_val) / (max_val - min_val) for n in lst]
        return out

    def scale_icus(self):
        lst = [self.data[i].icus_available for i in range(len(self.data))]
        max_val = max(lst); min_val = min(lst)
        out = [(n - min_val) / (max_val - min_val) for n in lst]
        return out

    def scale_vents(self):
        lst = [self.data[i].ventilators_available for i in range(len(self.data))]
        max_val = max(lst); min_val = min(lst)
        out = [(n - min_val) / (max_val - min_val) for n in lst]
        return out

    def scale_tests(self):
        lst = [self.data[i].coronavirus_tests_available for i in range(len(self.data))]
        max_val = max(lst); min_val = min(lst)
        out = [(n - min_val) / (max_val - min_val) for n in lst]
        return out

    def scale_distance(self, distances_dict):
        iterator = iter(distances_dict.items())
        max = min = next(iterator)[1]
        list = [-1*(self.base**max)]
        for i in range(1,len(self.hospitals)):
            n = next(iterator)[1]
            #linear
            #list.append(-1*n)
            #exponential
            list.append(-1*(self.base**n))
            if n > max:
                max = n
            if n < min:
                min = n
        out = []
        max = self.base**max
        min = self.base**min
        for n in list:
            out.append((n + max) / (max - min))
        return out


class PersonalDecision:
    def __init__(self, hospitals, data, patient):
        self.hospitals = hospitals
        self.data = data
        self.patient = patient
        self.ratings = {}

        # hyperparams
        self.capacity_weight = 1
        self.beds_weight = 3
        self.icus_weight = 1.5
        self.vents_weight = 1
        self.tests_weight = 1
        self.corona_weight = 1
        self.times_weight = 1.5

        self.symptoms_cutoff = 1
        self.risk_cutoff = 50

        self.base = 1.1

    def get_rating(self, distance_dict):
        capacities = self.scale_capacity()
        beds = self.scale_beds()
        icus = self.scale_icus()
        vents = self.scale_vents()
        tests = self.scale_tests()
        corona_percents = self.scale_corona_percents()
        distances = self.scale_distance(distance_dict)
        ratings = {}

        for i in range(len(self.hospitals)):
            ncap = self.capacity_weight * capacities[i]
            nbeds = self.beds_weight * beds[i]
            nicus = self.icus_weight * icus[i]
            nvents = self.vents_weight * vents[i]
            ntests = self.tests_weight * tests[i]
            ncorona_percents = self.corona_weight * corona_percents[i]
            ndistances = self.times_weight * distances[i]
            rating = ncap + nbeds + nicus + nvents + ntests + ncorona_percents + ndistances
            ratings[self.hospitals[i]] = rating

        ratings = sorted(ratings.items(), reverse=True, key=operator.itemgetter(1))
        for i in ratings:
            self.ratings[i[0]] = round(i[1], 2)
        return self.ratings

    def scale_capacity(self):
        lst = [self.data[i].bed_capacity for i in range(len(self.data))]
        max_val = max(lst); min_val = min(lst)
        out = [(n - min_val) / (max_val - min_val) for n in lst]
        return out

    def scale_beds(self):
        lst = [self.data[i].beds_available for i in range(len(self.data))]
        max_val = max(lst); min_val = min(lst)
        out = [(n - min_val) / (max_val - min_val) for n in lst]
        return out

    def scale_icus(self):
        lst = [self.data[i].icus_available for i in range(len(self.data))]
        max_val = max(lst); min_val = min(lst)
        out = [(n - min_val) / (max_val - min_val) for n in lst]
        return out

    def scale_vents(self):
        lst = [self.data[i].ventilators_available for i in range(len(self.data))]
        max_val = max(lst); min_val = min(lst)
        out = [(n - min_val) / (max_val - min_val) for n in lst]
        return out

    def scale_tests(self):
        lst = [self.data[i].coronavirus_tests_available for i in range(len(self.data))]
        max_val = max(lst); min_val = min(lst)
        out = [(n - min_val) / (max_val - min_val) for n in lst]
        return out

    def scale_corona_percents(self):
        symptoms = {"fever":0.879, "dry cough":0.677, "fatigue":0.381, "phlegm":0.334, "shortness of breath":0.186,
                 "sore throat, headache": 0.139, "chills": 0.114, "vomiting":0.05, "nasal congestion":0.048, "diarrhea":0.037}
        symptom_val = 0
        for s in self.patient.symptoms:
            symptom_val += symptoms[s]
        symptoms = symptom_val > self.symptoms_cutoff # if a person has high symptoms, true is high, false if low (use symptom score to calc)
        risk = self.patient.age + self.patient.under_conditions + self.patient.area > self.risk_cutoff # if a person is risky, true if risky, false if not (use age and underlying conditions to calc)

        lst = [self.data[i].coronavirus_patient_percent for i in range(len(self.data))]
        max_val = max(lst); min_val = min(lst)
        out = [(n - min_val) / (max_val - min_val) if risk or (not symptoms) else (1-n) for n in lst] # could be 'and' instead of 'or'
        return out

    def scale_distance(self, distance_dict):
        min_val = min(distance_dict.values())
        max_val = max(distance_dict.values())
        lst = [-1*(self.base**distance_dict[i]) for i in range(len(distance_dict))]
        max_val = self.base**max_val
        min_val = self.base**min_val
        out = [(n + max_val) / (max_val - min_val) for n in lst]
        return out


# for testing purposes (hyperparam tuning)

# hospitals = []
# patient = Patient(["fever","fatigue"],random.randint(10,80),random.randint(0,3))
# times_dict = {}
# for i in range(10):
#     hosp = Hospital(random.randint(500,1500),random.randint(10,30),random.randint(10,30),random.randint(10,30),random.randint(100,200),random.random())
#     hospitals.append(hosp)
#     times_dict[hosp] = random.randint(5,50)

# h = HomeDecision(hospitals)
# p = PersonalDecision(patient,hospitals,times_dict)
# hr = h.get_rating()
# hrt = h.get_rating_with_distance(times_dict)
# pr = p.get_rating()
#
# for i in hr.keys():
#     print(i.info(),hr[i])
# print("---------------")
# print("---------------")
# print("---------------")
# for i in hrt.keys():
#     print(i.info(),times_dict[i],hrt[i])
# print("---------------")
# print("---------------")
# print("---------------")
# print(patient.info())
# for i in pr.keys():
#     print(i.info(),times_dict[i],pr[i])
