class Hospital:
    def __init__(self, location, vent, bed, icu, tests, coron, insurance):
        self.location = location
        self.ventilators_available = vent
        self.beds_available = bed
        self.icu_available = icu
        self.num_tests = tests
        self.per_corona = coron
        self.insurance = insurance

        self.corona_score = self.calc_corona_score()
        self.reg_score = self.calc_regular_score()

    def calc_corona_score(self): # calculate corona score (based off test, ventilators, icus and beds)
        return -1

    def calc_regular_score(self): # calculate regular score (based of bed only)
        return -1
