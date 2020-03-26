class Hospital:
    def __init__(self, location, vent, bed, icu, daily, total):
        self.location = location
        self.ventilators_available = vent
        self.beds_available = bed
        self.icu_available = icu
        self.daily_testing = daily
        self.num_coronavirus = total

    def info(self):
        print(self.location, self.ventilators_available, self.beds_available, self.icu_available, self.daily_testing, self.num_coronavirus)
