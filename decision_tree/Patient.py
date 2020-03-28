import operator

class Patient:
    def __init__(self, location, transport, conditions, age, symptoms, insurance):
        # hyper params for tuning
        self.ins_cutoff = 5 # number of hopsitals that match their insurance cutoff, if above then get rid of non-matches, if below keep all
        self.symp_cutoff = 1.75 # cutoff for symptom score for coronavirus vs. non coronavirus
        self.radius = 10 # cutoff for radius in miles of what hospitals we will look at
        self.scweight = 0.5 # weight value for symp_val for coronavirus positive patient
        self.ccweight = 0.3 # weight value for cond_val for coronavirus positive patient
        self.acweight = 0.2 # weight value for age_val for coronavirus positive patient
        self.crweight = 0.5 # weight value for cond_val for regular patient
        self.arweight = 0.5 # weight value for age_val for regular patient
        self.risk_scale = 0.1 # scale that brings down risk value

        # user data
        self.location = location
        self.transport = transport
        self.conditions = conditions
        self.age = age
        self.symptoms = symptoms
        self.insurance = insurance

        self.hospitals = self.getHospitals()
        self.times = dict()
        for h in self.hospitals:
            self.times[h] = self.calcTime()

        self.symp_val = self.calcSymp()
        self.cond_val = self.calcCond()
        self.age_val = self.calcAge()

        self.corona = self.symp_val > self.symp_cutoff
        if self.corona:
            self.risk = (self.symp_val * self.scweight) + (self.cond_val * self.ccweight) + (self.age_val * self.acweight)
        else:
            self.risk = (self.cond_val * self.crweight) + (self.age_val * self.arweight)

        self.checkIns()
        self.calcHosp()
        self.displayHosp()


    def getHospitals(self): # use location to find hospitals in a radius (default 10 miles)
        pass

    def calcTime(self): # use location and transport with google API to find time between hospital and patient
        pass

    def calcSymp(self): # use symptom values to determine total score
        val = 0
        symps = {"fever":0.879, "dry cough":0.677, "fatigue":0.381, "phlegm":0.334, "shortness of breath":0.186,
                "sore throat, headache": 0.139, "chills": 0.114, "vomiting":0.05, "nasal congestion":0.048, "diarrhea":0.037}
        for symptom in self.symptoms:
            val+=symps[symptom]
        return (val/2.845) * 10

    def calcCond(self): # use conditions values to determine total score
        if(self.conditions == 0)
            return 0
        if(self.conditions == 1)
            return 5
        if(self.conditions == 2)
            return 8
        return 10

    def calcAge(self): # condenses age to 0-10 scale
        return min(self.age,100) / 10.0

    def calcIns(self): # categorizes insurance type as int
        pass

    def checkIns(self): # check what hopsitals have the patient's insurance
        hosp = []
        for h in self.hospitals:
            if self.insurance in h.insurance:
                hosp.append(h);
        if len(hosp) > self.ins_cutoff:
            self.hospitals = hosp

    def calcHosp(self): # calculates the hospitals scores
        hrank = dict()
        for h in self.hospitals:
            if self.corona:
                rating = h.per_corona * ((h.corona_score * self.risk_scale * self.risk) + (self.times[h] * (1 - self.risk_scale * self.risk)))
                hrank[h] = rating
            else:
                rating = (h.reg_score * self.risk_scale * self.risk) + (self.times[h] * (1 - self.risk_scale * self.risk))
                hrank[h] = rating

        self.hosp_ranked = sorted(hrank.items(), reverse = True, key=operator.itemgetter(1))

    def displayHosp(self): # display hospitals in order (self.hosp_ranked) on screen
        pass
