class CoronavirusCaseModeling:
    def __init__(self, factor, pop):
        self.growth_factor = factor
        self.max = pop*0.6

    def predict(self, start, capacity):
        

tester = CoronavirusCaseModeling(1.2, 8623000)
cases = tester.predict(14)
for i in range(len(cases)):
    print(cases[i])