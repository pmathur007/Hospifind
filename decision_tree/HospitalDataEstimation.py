class HospitalDataEstimation:
    def predict(self, capacity, start_full=0.6, start_corona=0.07, factor=1.2):
        full_beds = int(capacity*start_full)
        corona_start = int(start_corona * capacity)
        start = (corona_start, corona_start + full_beds)
        cases = list()
        cases.append(start)
        while cases[-1][1] < capacity:
            cases.append((round(cases[-1][0] * factor), round(cases[-1][0] * factor + full_beds)))
        cases[-1] = (round(capacity - full_beds), round(capacity))
        return cases
