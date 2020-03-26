import random
from decision_tree.Hospital import Hospital

# size is 1-10 indicator of hospital "size", corona_size is 1-10 hospital indicator of how much corona hospital is dealing with


def hospital_data_generate(location, size, corona_size):
    vent = int(250 * random.random(corona_size - 1, corona_size + 1))
    bed = int(1000 * random.random(size - 1, size + 1))
    icu = bed//10
    testing = int(100 * random.random(corona_size - 1, corona_size + 1))
    coronavirus_patient = int(500 * random.random(corona_size - 1, corona_size + 1))
    return Hospital(location, vent, bed, icu, testing, coronavirus_patient)

