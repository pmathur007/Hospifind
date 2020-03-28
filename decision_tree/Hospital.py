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

        self.corona_score = self.calculate_corona_score()
        self.regular_score = self.calculate_regular_score()

    def calculate_corona_score(self):
        return (self.beds_available + self.icu_available + self.num_tests) # * self.percent_corona

    def calculate_regular_score(self):
        return (1 - self.percent_corona) * (self.beds_available)

    def get_name(self):
        return self.name

    def get_location(self):
        return self.location

    def get_ventilators(self):
        return self.ventilators_available

    def get_beds(self):
        return self.beds_available

    def get_icu(self):
        return self.icu_available

    def get_tests(self):
        return self.num_tests

    def get_percent_corona(self):
        return self.percent_corona

    def get_insurance(self):
        return self.insurance

    def get_corona_score(self):
        return self.corona_score

    def get_regular_score(self):
        return self.regular_score

    def to_string(self):
        return self.name + "\nLocation: " + str(self.location) + "\nHospital Beds Available: " + str(self.beds_available) + "\nICU Beds Available: " + str(self.icu_available) + "\nVentilators Available: " + str(self.ventilators_available) + "\nNumber of Tests Available: " + str(self.num_tests) + "\nPercentage Coronavirus Patients: " + str(self.percent_corona)