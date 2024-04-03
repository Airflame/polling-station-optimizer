import sys
import six
sys.modules['sklearn.externals.six'] = six
import mlrose
from math import sqrt


class Station:
    """A polling station"""

    def __init__(self, index, x, y):
        self.index = index
        self.x = x
        self.y = y
        self.weight = 0

    def add_weight(self, amount):
        self.weight += amount

    def get_distance(self, px, py):
        return sqrt((px - self.x) ** 2 + (py - self.y) ** 2)

    def __str__(self):
        return f"Station [Id: {self.index}, X: {self.x}, Y: {self.y}, is_choosen: {self.is_chosen}, weight: {self.weight}]"

    def __repr__(self):
        return f"Station [X:{self.x},Y:{self.y},CH:{self.is_chosen},W: {self.weight}]"


possible_stations = [Station(0,0,0), Station(1,0,3),
                    Station(2,1,1),
                    Station(3,2,2), Station(4,3,2), Station(5,3,3),
                    Station(6,3,0), Station(7,3,4),
                    Station(8,4,1), Station(9,4,3)]
GOAL_STATIONS = 7
city_matrix = [
    [12, 15, 10,  6,  3],
    [8,  19, 12,  8,  1],
    [8,  12, 15, 10,  5],
    [10, 18, 20, 14, 10],
    [7,  12, 14, 11,  6]
]


def fitness_function(solution: tuple):
    if sum(solution) != GOAL_STATIONS:
        return sys.maxsize
    for station in possible_stations:
        station.weight = 0
    selected_stations = []
    for index, value in enumerate(solution):
        if value:
            selected_stations.append(possible_stations[index])
    for y, row in enumerate(city_matrix):
        for x, population in enumerate(row):
            closest_index = None
            closest_distance = sys.maxsize
            for index, station in enumerate(selected_stations):
                distance = station.get_distance(x, y)
                if distance < closest_distance:
                    closest_index = index
                    closest_distance = distance
            selected_stations[closest_index].add_weight(population)
    avg_weight = 0
    for station in selected_stations:
        avg_weight += station.weight
    avg_weight /= len(selected_stations)
    fitness_score = 0
    for station in selected_stations:
        fitness_score += abs(station.weight - avg_weight)
    return fitness_score


fitness = mlrose.CustomFitness(fitness_function)
problem = mlrose.DiscreteOpt(length=len(possible_stations), fitness_fn=fitness, maximize=False, max_val=2)
best_solution, best_fitness, fitness_curve = mlrose.genetic_alg(problem, curve=True)
print(best_solution)
print(best_fitness)
