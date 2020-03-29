from datetime import date
import datetime


class Hospital:
    def __init__(self, name, total_bed, location, bed, icu, vent, tests, corona, days):
        self.name = name
        self.beds = total_bed
        self.location = location

        self.days = days
        if days == -1:
            self.ventilators_available, self.beds_available, self.icu_available, self.num_tests, self.percent_corona = self.simulate_data(days)
        else:
            self.ventilators_available, self.beds_available, self.icu_available, self.num_tests, self.percent_corona = self.simulate_data(days, vent, bed, icu, tests, corona)

        # hyper params for tuning
        self.beds_weight = 1
        self.icu_weight = 10
        self.test_weight = 5
        self.ventilator_weight = 7
        self.per_corona_weight = 0.25

        self.corona_score = self.calculate_corona_score()
        self.regular_score = self.calculate_regular_score()

    def simulate_data(self, days, available_ventilators=0, available_beds=0, available_icus=0, available_tests=0, percent_corona=0.1):
        if days == -1:
            days_behind = (date.today() - date(2020, 3, 28)).days
            total_icu = int(self.beds * 0.08)
            total_ventilators = int(self.beds * 0.17)
            available_tests = int(self.beds * 0.3)

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
            days_behind = days
            num_corona = percent_corona * (self.beds - available_beds)

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
        return self.name + "\nLocation: " + str(self.location) + "\nHospital Beds Available: " + str(self.beds_available) + "\nICU Beds Available: " + str(self.icu_available) + "\nVentilators Available: " + str(self.ventilators_available) + "\nNumber of Tests Available: " + str(self.num_tests) + "\nPercentage Coronavirus Patients: " + str(self.percent_corona)