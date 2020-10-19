import sys

from graph_representation import Graph
from hive_representation import *


class TSP(object):
    """Class to solve TSP
    using ABC algorithm"""

    def __init__(self, cities_number, employed_bees_num,
                 onlooker_bees_num, limit_num, tsp_iterations, graph1):
        """Init main params"""

        self.employed_bees_num = employed_bees_num
        self.onlooker_bees_num = onlooker_bees_num
        self.graph = graph1

        self.cities_number = cities_number
        self.hive = Hive(limit_num)
        self.tsp_iterations = tsp_iterations

    def solve(self):
        """Main method to solve TSP
        All phases of the algorithm are performed from here"""

        self.__pre_hive_phase()
        for t in range(self.tsp_iterations):
            self.__employed_bee_phase()

            self.__onlooker_bee_phase()

            self.__scout_bee_phase()
            if t % 100 == 0:
                print(f"Best employed bee of {t} iteration: {self.hive.best_bee[1]}")
        return self.hive.best_bee[0], self.hive.best_bee[1]

    def __pre_hive_phase(self):
        """Method which represents phase of the starter initialization of the employed bees.
        (Randomly solution selection)"""
        init_employed_bees = []
        for i in range(int(self.employed_bees_num)):
            r_solution = random.sample(range(self.cities_number), self.cities_number)
            bee = EmployedBee(r_solution, self.graph, self.hive)
            init_employed_bees.append(bee)
        self.hive.add_employed_bees_from(init_employed_bees)

    def __employed_bee_phase(self):
        """Method which represents employed bees phase
        (All employed bees try to improve their solution by generation new variable by using
        the partner variable. Partner gets randomly)"""

        for bee in self.hive.employed_bees:
            bee.try_new_solution()

    def __onlooker_bee_phase(self):
        """Method which represents onlooker bee phase
        (Every employed bee (formal onlooker bee) try to generate new solution that is better
        than previous one. In case there were a huge number of tries bee becomes scout)"""

        self.hive.recount_employed_prob()
        n = 0
        for m in range(self.onlooker_bees_num):
            solution_to_check = self.hive.employed_bees[n]
            if random.random() < solution_to_check.probability:
                solution_to_check.try_new_solution()
                m += 1
            n += 1
            if n > self.employed_bees_num - 1:
                n = 0

    def __scout_bee_phase(self):
        self.hive.setup_scouts()


# python tsp.py {cities_number} {employed_bees} {onlooker_bees} {iterations}
if __name__ == '__main__':
    if len(sys.argv) != 5:
        sys.exit('Incorrect number of parameters!')
    if not sys.argv[1].isnumeric():
        sys.exit('Invalid number of cities')
    if not sys.argv[2].isnumeric():
        sys.exit('Invalid number of employed bees')
    if not sys.argv[3].isnumeric():
        sys.exit('Invalid number of onlooker bees')
    if not sys.argv[4].isnumeric():
        sys.exit('Invalid number of iterations')

    cities = int(sys.argv[1])
    employed_bees = int(sys.argv[2])
    onlooker_bees = int(sys.argv[3])
    limit = cities * employed_bees
    iterations = int(sys.argv[4])

    graph = Graph(cities)

    solver = TSP(cities, employed_bees, onlooker_bees, limit, iterations, graph)
    print(solver.solve()[1])
