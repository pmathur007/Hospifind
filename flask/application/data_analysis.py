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
        max = min = self.data[0].bed_capacity
        list = [max]
        for i in range(1,len(self.data)):
            n = self.data[i].bed_capacity
            list.append(n)
            if n > max:
                max = n
            if n < min:
                min = n
        out = []
        for n in list:
            out.append((n - min) / (max - min))
        return out

    def scale_beds(self):
        max = min = self.data[0].beds_available
        list = [max]
        for i in range(1,len(self.data)):
            n = self.data[i].beds_available
            list.append(n)
            if n > max:
                max = n
            if n < min:
                min = n
        out = []
        for n in list:
            out.append((n - min) / (max - min))
        return out

    def scale_icus(self):
        max = min = self.data[0].icus_available
        list = [max]
        for i in range(1,len(self.data)):
            n = self.data[i].icus_available
            list.append(n)
            if n > max:
                max = n
            if n < min:
                min = n
        out = []
        for n in list:
            out.append((n - min) / (max - min))
        return out

    def scale_vents(self):
        max = min = self.data[0].ventilators_available
        list = [max]
        for i in range(1,len(self.data)):
            n = self.data[i].ventilators_available
            list.append(n)
            if n > max:
                max = n
            if n < min:
                min = n
        out = []
        for n in list:
            out.append((n - min) / (max - min))
        return out

    def scale_tests(self):
        max = min = self.data[0].coronavirus_tests_available
        list = [max]
        for i in range(1,len(self.data)):
            n = self.data[i].coronavirus_tests_available
            list.append(n)
            if n > max:
                max = n
            if n < min:
                min = n
        out = []
        for n in list:
            out.append((n - min) / (max - min))
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
    def __init__(self, patient, hospitals, times_dict):
        self.patient = patient
        self.hospitals = hospitals
        self.times_dict = times_dict
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

    def get_rating(self):
        capacities = self.scale_capacity()
        beds = self.scale_beds()
        icus = self.scale_icus()
        vents = self.scale_vents()
        tests = self.scale_tests()
        corona_percents = self.scale_corona_percents()
        times = self.scale_times()
        ratings = {}

        for i in range(len(self.hospitals)):
            ncap = self.capacity_weight * capacities[i]
            nbeds = self.beds_weight * beds[i]
            nicus = self.icus_weight * icus[i]
            nvents = self.vents_weight * vents[i]
            ntests = self.tests_weight * tests[i]
            ncorona_percents = self.corona_weight * corona_percents[i]
            ntimes = self.times_weight * times[i]
            rating = ncap + nbeds + nicus + nvents + ntests + ncorona_percents + ntimes
            ratings[self.hospitals[i]] = rating

        ratings = sorted(ratings.items(), reverse=True, key=operator.itemgetter(1))
        for i in ratings:
            self.ratings[i[0]] = round(i[1],2)
        return self.ratings

    def scale_capacity(self):
        max = min = self.hospitals[0].capacity
        list = [max]
        for i in range(1,len(self.hospitals)):
            n = self.hospitals[i].capacity
            list.append(n)
            if n > max:
                max = n
            if n < min:
                min = n
        out = []
        for n in list:
            out.append((n - min) / (max - min))
        return out

    def scale_beds(self):
        max = min = self.hospitals[0].beds
        list = [max]
        for i in range(1,len(self.hospitals)):
            n = self.hospitals[i].beds
            list.append(n)
            if n > max:
                max = n
            if n < min:
                min = n
        out = []
        for n in list:
            out.append((n - min) / (max - min))
        return out

    def scale_icus(self):
        max = min = self.hospitals[0].icus
        list = [max]
        for i in range(1,len(self.hospitals)):
            n = self.hospitals[i].icus
            list.append(n)
            if n > max:
                max = n
            if n < min:
                min = n
        out = []
        for n in list:
            out.append((n - min) / (max - min))
        return out

    def scale_vents(self):
        max = min = self.hospitals[0].vents
        list = [max]
        for i in range(1,len(self.hospitals)):
            n = self.hospitals[i].vents
            list.append(n)
            if n > max:
                max = n
            if n < min:
                min = n
        out = []
        for n in list:
            out.append((n - min) / (max - min))
        return out

    def scale_tests(self):
        max = min = self.hospitals[0].tests
        list = [max]
        for i in range(1,len(self.hospitals)):
            n = self.hospitals[i].tests
            list.append(n)
            if n > max:
                max = n
            if n < min:
                min = n
        out = []
        for n in list:
            out.append((n - min) / (max - min))
        return out

    def scale_corona_percents(self):
        symps = {"fever":0.879, "dry cough":0.677, "fatigue":0.381, "phlegm":0.334, "shortness of breath":0.186,
                 "sore throat, headache": 0.139, "chills": 0.114, "vomiting":0.05, "nasal congestion":0.048, "diarrhea":0.037}
        sval = 0
        for s in self.patient.symptoms:
            sval+=symps[s]
        symptoms = sval > self.symptoms_cutoff # if a person has high symptoms, true is high, false if low (use symptom score to calc)
        risk = self.patient.age + (20 * self.patient.under_conditions) > self.risk_cutoff # if a person is risky, true if risky, false if not (use age and underlying conditions to calc)

        max = min = self.hospitals[0].corona_percent
        list = [max]
        for i in range(1,len(self.hospitals)):
            n = self.hospitals[i].corona_percent
            list.append(n)
            if n > max:
                max = n
            if n < min:
                min = n
        out = []
        for n in list:
            out.append((n - min) / (max - min))
            if risk or (not symptoms): # could be 'and' instead of 'or'
                out.append(1 - n)
        return out

    def scale_times(self):
        iterator = iter(self.times_dict.items())
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


# for testing purposes (hyperparam tuning)

hospitals = []
patient = Patient(["fever","fatigue"],random.randint(10,80),random.randint(0,3))
times_dict = {}
for i in range(10):
    hosp = Hospital(random.randint(500,1500),random.randint(10,30),random.randint(10,30),random.randint(10,30),random.randint(100,200),random.random())
    hospitals.append(hosp)
    times_dict[hosp] = random.randint(5,50)

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
