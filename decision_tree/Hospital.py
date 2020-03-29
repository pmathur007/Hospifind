class Hospital:
    def __init__(self, name, location, vent, bed, icu, tests, corona, insurance=None):
        self.name = name
        self.location = location
        self.ventilators_available = vent
        self.beds_available = bed
        self.icu_available = icu
        self.num_tests = tests
        self.percent_corona = corona
        self.insurance = insurance

        # hyper params for tuning
        self.beds_weight = 1
        self.icu_weight = 10
        self.test_weight = 5
        self.ventilator_weight = 7
        self.per_corona_weight = 0.25


        self.corona_score = self.calculate_corona_score()
        self.regular_score = self.calculate_regular_score()

    def calculate_corona_score(self):
        return self.percent_corona * self.per_corona_weight * (self.beds_available * self.beds_weight + self.icu_available * self.icu_weight + self.num_tests * self.test_weight + self.ventilator_weight * self.ventilators_available)

    def calculate_regular_score(self):
        return (1 - self.percent_corona) * self.per_corona_weight * self.beds_available

    def to_string(self):
        return self.name + "\nLocation: " + str(self.location) + "\nHospital Beds Available: " + str(self.beds_available) + "\nICU Beds Available: " + str(self.icu_available) + "\nVentilators Available: " + str(self.ventilators_available) + "\nNumber of Tests Available: " + str(self.num_tests) + "\nPercentage Coronavirus Patients: " + str(self.percent_corona)
