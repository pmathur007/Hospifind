from datetime import date
import operator


class Hospital:
    def __init__(self, authentication_key, total_bed, bed, icu, vent, tests, num_corona, last_input):
        self.authentication_key = authentication_key
        self.beds = total_bed

        self.last_input = last_input
        if self.last_input == -1:
            self.ventilators_available, self.beds_available, self.icu_available, self.num_tests, self.percent_corona = self.simulate_data(self.last_input)
        else:
            self.ventilators_available, self.beds_available, self.icu_available, self.num_tests, self.percent_corona = self.simulate_data(self.last_input, vent, bed, icu, tests, num_corona)

        # hyper params for tuning
        self.beds_weight = 1
        self.icu_weight = 10
        self.test_weight = 5
        self.ventilator_weight = 7
        self.per_corona_weight = 0.25

        self.corona_score = self.calculate_corona_score()
        self.regular_score = self.calculate_regular_score()

    def simulate_data(self, last_input, available_ventilators=0, available_beds=0, available_icus=0, available_tests=0, num_corona=0):
        if last_input == -1:
            days_behind = (date.today() - date(2020, 3, 28)).days
            total_icu = int(self.beds * 0.08)
            total_ventilators = int(self.beds * 0.17)
            available_tests = int(self.beds * 0.3)

            percent_corona = 0.1

            full_beds = int(self.beds * 0.6)
            corona_start = int(percent_corona * self.beds)
            start = (corona_start, corona_start + full_beds)
            cases = [start]
            while cases[-1][1] < self.beds and len(cases) <= days_behind:
                cases.append((round(cases[-1][0] * 1.2), round(cases[-1][0] * 1.2 + full_beds)))

            num_corona = cases[-1][0]
            percent_corona = cases[-1][0] / cases[-1][1]
            return max(int(total_ventilators - 0.2*num_corona), 0), max(self.beds - cases[-1][1], 0), max(int(total_icu - 0.1*num_corona), 0), available_tests, round(percent_corona, 2)
        else:
            split = last_input.split("/")
            days_behind = (date.today() - date(int(split[2]), int(split[0]), int(split[1]))).days

            full_beds = int(self.beds * 0.6)
            start = (num_corona, num_corona + full_beds)
            cases = [start]
            while cases[-1][1] < self.beds and len(cases) <= days_behind:
                cases.append((round(cases[-1][0] * 1.2), round(cases[-1][0] * 1.2 + full_beds)))
            new_cases = cases[-1][0] - num_corona
            percent_corona = cases[-1][0] / cases[-1][1]
            return max(int(available_ventilators - 0.2*num_corona), 0), max(available_beds - new_cases, 0), max(int(available_icus - 0.1*num_corona), 0), available_tests, round(percent_corona, 2)

    def calculate_corona_score(self):
        return self.percent_corona * self.per_corona_weight * (self.beds_available * self.beds_weight + self.icu_available * self.icu_weight + self.num_tests * self.test_weight + self.ventilator_weight * self.ventilators_available)

    def calculate_regular_score(self):
        return (1 - self.percent_corona) * self.per_corona_weight * self.beds_available

    def to_string(self):
        return self.authentication_key + "\nHospital Beds Available: " + str(self.beds_available) + "\nICU Beds Available: " + str(self.icu_available) + "\nVentilators Available: " + str(self.ventilators_available) + "\nNumber of Tests Available: " + str(self.num_tests) + "\nPercentage Coronavirus Patients: " + str(self.percent_corona)


class Patient:
    def __init__(self, conditions, age, symptoms):
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
        self.conditions = conditions
        self.age = age
        self.symptoms_val = symptoms

        # later defined data
        self.hospitals = []
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
        self.conditions_val = self.calculate_condition_score()
        self.age_val = self.calculate_age_score()

        self.corona = self.symptoms_val > self.symptom_cutoff
        if self.corona:
            self.risk = (self.symptoms_val * self.symptoms_corona_weight) + (self.conditions_val * self.conditions_corona_weight) + (self.age_val * self.age_corona_weight)
        else:
            self.risk = (self.conditions_val * self.conditions_regular_weight) + (self.age_val * self.age_regular_weight)

        self.calculate_hospital_score()
        self.display_hospitals()
        return self.hospital_ranks

    def get_hospitals(self): # get it from java script
        return self.given_hospitals

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
        hospital_output = sorted(hospital_ranks.items(), reverse=True, key=operator.itemgetter(1))
        max = hospital_output[0][1]
        for h in hospital_output:
            score = (h[1] / max) * 10.0
            if score > 9:
                score = "Great"
            elif score > 7:
                score = "Good"
            elif score > 5:
                score = "OK"
            else:
                score = "Bad"
            self.hospital_ranks.append((h[0].authentication_key, score))

    def display_hospitals(self): # display hospitals in order (self.hospital_ranks) on screen
        for h in self.hospital_ranks:
            print(h[0].name + "\nTime: " + str(self.hospitals[h[0]]) + "\nRating: " + h[1] + "\n")


def process(json):
    hospitals = dict()
    patient = Patient(json["Patient"]["prev_conditions"], json["Patient"]["age"], json["Patient"]["symptoms"])
    for hosp in json["Hospitals"]:
        if hosp != "Patient":
            hospitals[Hospital(json[hosp]["AuthenticationKey"], json[hosp]["Beds"], json[hosp]["BedsAvailable"], json[hosp]["ICUAvailable"], json[hosp]["VentilatorsAvailable"], json[hosp]["TestsAvailable"], json[hosp]["CoronavirusNumber"], json[hosp]["LastInput"])] = json[hosp]["TravelTime"]
    patient.input_hospitals(hospitals)
    ranks = patient.process()
