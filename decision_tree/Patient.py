class Patient:
    def __init__(self, location, time, car, corona, conditions, age, insurance):
        self.location = location
        self.time = time
        self.has_car = car
        self.corona_symptoms = corona
        self.preexisting_conditions = conditions
        self.age = age
        self.insurance = insurance

    def info(self):
        print(self.location, self.time, self.has_car, self.corona_symptoms, self.preexisting_conditions, self.age, self.insurance, sep="\n")
