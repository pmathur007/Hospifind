class CoronavirusCaseModeling:
    def predict(self, capacity, start_full=0.6, start_corona=0.07, factor=1.2, overload=1):
        full_beds = int(capacity*start_full)
        corona_start = int(start_corona * capacity)
        start = (corona_start, corona_start + full_beds)
        cases = list()
        cases.append(start)
        while cases[-1][1] < overload * capacity:
            cases.append((round(cases[-1][0] * factor), round(cases[-1][0] * factor + full_beds)))
        cases[-1] = (round(overload * capacity - full_beds), round(overload * capacity))
        return cases
