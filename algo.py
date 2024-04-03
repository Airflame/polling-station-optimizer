from difflib import diff_bytes
from math import sqrt
from os import sep
import random
import copy
class City:
    def __init__(self, city_matrix):
        self.city_matrix = city_matrix

class Station:
    """A polling station"""
    def __init__(self, index, x, y, is_choosen):
        self.index = index
        self.x = x
        self.y = y
        self.is_choosen = is_choosen
        self.weight = 0

    
    def add_weight(self, amount):
        self.weight += amount

    # @property
    # def value(self):
    #     return self.popularity+(self.density-100)/10000
    
    def __str__(self):
        return f"Station [Id: {self.index}, X: {self.x}, Y: {self.y}, is_choosen: {self.is_choosen}, weight: {self.weight}]"
    
    def __repr__(self):
        return f"Station [X:{self.x},Y:{self.y},CH:{self.is_choosen},W: {self.weight}]"


# possibleStations = [Station(0,0,0, False), Station(1,1,2, False), Station(2,2,1, False)]
# N = 3
# M = 3
# GOAL_STATIONS = 2
# city_matrix = [
#     [12, 15, 5],
#     [8, 19, 12],
#     [8, 12, 11]
# ]

# city_matrix = [
#     [x,  15, 10,  x,  3],
#     [8,   x, 12,  8,  1],
#     [8,   x,  x,  x,  5],
#     [x,  18, 20,  10, x],
#     [7,   x, 14,  x,  6]
# ]
possibleStations = [Station(0,0,0, False), Station(1,0,3, False),
                    Station(2,1,1, False),
                    Station(3,2,2, False), Station(4,3,2, False), Station(5,3,3, False),
                    Station(6,3,0, False), Station(7,3,4, False),
                    Station(8,4,1, False), Station(9,4,3, False)]
N = 5
M = 5
GOAL_STATIONS = 7
city_matrix = [
    [12, 15, 10,  6,  3],
    [8,  19, 12,  8,  1],
    [8,  12, 15, 10,  5],
    [10, 18, 20, 14, 10],
    [7,  12, 14, 11,  6]
]

limit = 20
initial_population = 100
mutation_chances = 0.25
generations = 50

def max_stations_diffrence(possibleStations):
    mean = 0
    choosen_stations = list(filter(lambda x: x.is_choosen, possibleStations))
    for station in choosen_stations:
        mean += station.weight

    mean = mean / len(choosen_stations)
    delta = 0
    for station in choosen_stations:
        delta += abs(station.weight - mean)
    return delta

def goal_second(possibleStations, occupation_matrix=False):
    district_assignment_matrix = []
    for station in possibleStations:
        station.weight = 0

    for y in range(N):
        assignment_row = []
        for x in range(M):
            closestStation = possibleStations[0] # domyslnie pierwsza
            closestProximity = N+M
            for station in possibleStations:
                if not station.is_choosen:
                    continue
                # proximity = abs(x - station.x) + abs(y - station.y) # Manhattan
                proximity = sqrt(pow(x - station.x, 2) + pow(y - station.y, 2))
                if proximity < closestProximity:
                    closestStation = station
                    closestProximity = proximity
            closestStation.add_weight(city_matrix[x][y])
            assignment_row.append(closestStation.index)
        district_assignment_matrix.append(assignment_row)

    if occupation_matrix:
        for row in district_assignment_matrix:
            print(row, sep=" ")
    
    difference = max_stations_diffrence(possibleStations)
    return difference

# Crossing with keeping the same number of ones
chosenStationsChromosome = [int(i.is_choosen) for i in possibleStations]

# Crossing with keeping the same number of ones
def crossing(c1, c2):
    assert sum(c1)==sum(c2) and len(c1)==len(c2)
    ind = [i for i in range(len(c1)) if c1[i]]
    ind += [i for i in range(len(c2)) if c2[i]]
    ind = list(dict.fromkeys(ind))
    random.shuffle(ind)
    out = [c1[i] & c2[i] for i in range(len(c1))]
    to_remove = [index for index, value in enumerate(out) if value == 1]
    it = sum(c1)-sum(out)
    ind = list(filter(lambda a: a not in to_remove, ind))
    for i in range(it):
        out[ind[i]] = 1
    return out

def crossing_second(chromosomeOne, chromosomeTwo):
    r = []
    c1 = [int(i.is_choosen) for i in chromosomeOne]
    c2 = [int(i.is_choosen) for i in chromosomeTwo]
    crossed = crossing(c1, c2)
    r = copy.deepcopy(chromosomeOne)
    for i in range(len(crossed)):
        r[i].is_choosen = bool(crossed[i])
        r[i].weight = 0
    return r

# Crossing randomly
def crossing_random(c1, c2):
    assert len(c1)==len(c2)
    p = [c1, c2]
    return [p[random.randrange(2)][i] for i in range(len(c1))]

current = 0
seed = [0 for _ in range(len(possibleStations))]
for i in range(GOAL_STATIONS):
    seed[i]=1
chromosomes = []
for x in range(limit):
    random.shuffle(seed)
    temp = copy.deepcopy(possibleStations)
    # print(f"Sample chromosome {x}")
    for i in range(len(temp)):
        temp[i].is_choosen = bool(seed[i])
    # for station in temp:
    #     if station.is_choosen:
    #         print(station)
    chromosomes.append(temp)

for gen in range(generations):
    # calculating weights for each station in each chromosome
    for chromosome in chromosomes:
        goal_second(chromosome)

    chromosomes = sorted(chromosomes, key=max_stations_diffrence)
    print(f"Generation {gen} with best score: {max_stations_diffrence(chromosomes[0])}")
    for station in chromosomes[0]:
        if station.is_choosen:
            print(station)
    goal_second(chromosomes[0], True)

    # Selection
    chromosomes = chromosomes[:1+len(chromosomes)//3]
    # Crossing
    new_gen = []
    while(len(new_gen)<limit):
        c1 = random.choice(chromosomes)
        c2 = random.choice(chromosomes)
        new_gen.append(crossing_second(c1, c2))
    chromosomes = copy.deepcopy(new_gen)
    # Mutations
    for i in range(len(chromosomes)):
        if random.randrange(100) < mutation_chances*100:
            rnd_index = random.randrange(len(chromosomes[i]))
            rnd_station_is_choosen = copy.deepcopy(chromosomes[i][rnd_index].is_choosen)
            rnd_other_station_index = copy.deepcopy(rnd_index) # Presetup
            rnd_other_station_is_choosen = copy.deepcopy(chromosomes[0][rnd_index].is_choosen) # Presetup

            while rnd_index == rnd_other_station_index:
                rnd_other_station_index = random.randrange(len(chromosomes[i]))
                rnd_other_station_is_choosen = copy.deepcopy(chromosomes[i][rnd_other_station_index].is_choosen)

                if rnd_other_station_index is not rnd_index:
                    if rnd_other_station_is_choosen is not rnd_station_is_choosen:
                        # Flipping
                        chromosomes[i][rnd_other_station_index].is_choosen = rnd_station_is_choosen
                        chromosomes[i][rnd_index].is_choosen = rnd_other_station_is_choosen
