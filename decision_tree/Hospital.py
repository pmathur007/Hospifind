class Hospital:
    def __init__(self, location, vent, bed, icu, tests, coron, insurance):
        self.location = location
        self.ventilators_available = vent
        self.beds_available = bed
        self.icu_available = icu
        self.num_tests = tests
        self.per_corona = coron
        self.insurance = insurance

        self.corona_score = calcCor()
        self.reg_score = calcReg()

    def calcCor(self): # calculate corona score (based off test, ventilators, icus and beds)
        pass

    def calcReg(self): # calculate regular score (based of bed only)
        pass
