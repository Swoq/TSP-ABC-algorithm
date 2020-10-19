import random
from operator import attrgetter


class Hive(object):
    """Class to represent all types of Bees together"""

    def __init__(self, limit, employed_bees=None, onlooker_bees=None):
        if not employed_bees:
            self.employed_bees = []
        else:
            self.employed_bees = employed_bees[:]

        if not onlooker_bees:
            self.onlooker_bees = []
        else:
            self.onlooker_bees = onlooker_bees[:]

        self.best_bee = None
        self.limit = limit

    def add_employed_bees_from(self, employed_bees):
        self.employed_bees = employed_bees[:]

    def recount_employed_prob(self):
        fitness_sum = 0
        for bee in self.employed_bees:
            fitness_sum += bee.fitness

        for bee in self.employed_bees:
            bee.recount_probability(fitness_sum)

    def setup_scouts(self):
        scout = max(self.employed_bees, key=attrgetter('trial'))

        if scout.trial > self.limit:
            scout.reset_random_solution()


class EmployedBee(object):
    """Class to represent EmployedBee"""

    def __init__(self, solution, graph, hive):
        self.solution = solution
        self.trial = 0
        self.graph = graph
        self.hive = hive
        self.fitness = None
        self.status = None
        self.probability = None

        self.__recount_fitness()

    def __recount_fitness(self):
        pairs = list(zip(self.solution, self.solution[1:] + self.solution[:1]))

        res = None
        for pair in pairs:
            if not res:
                res = self.graph.e_dict[pair]
                continue
            res += self.graph.e_dict[pair]
        self.fitness = res

        # if the fitness better than previous the best fitness -> change better bee
        if not self.hive.best_bee:
            self.hive.best_bee = (self.solution, self.fitness)
        elif self.fitness < self.hive.best_bee[1]:
            self.hive.best_bee = (self.solution, self.fitness)

    def recount_probability(self, fitness_sum):
        # self.probability = 0.9*(self.fitness/self.hive.best_bee.fitness)+0.1
        self.probability = self.fitness / fitness_sum

    def try_new_solution(self):
        # variable to change randomly
        j = random.randint(0, len(self.solution) - 1)
        # random partner
        p_bee = random.choice(self.hive.employed_bees)
        while p_bee == self:
            p_bee = random.choice(self.hive.employed_bees)
        # new variable
        x = round(self.solution[j] + random.uniform(-1.0, 1.0) * (self.solution[j] - p_bee.solution[j]))
        # bound variable
        if x < 0:
            x = 0
        if x > self.graph.vertex_num - 1:
            x = self.graph.vertex_num - 1
        self.validate_new_solution(x, j)

    def validate_new_solution(self, new_var, num_of_war):
        # save old data to recover
        old_fitness = self.fitness
        old_var = self.solution[num_of_war]
        old_solution = self.solution

        # try to change solution
        self.solution[self.solution.index(new_var)] = old_var
        self.solution[num_of_war] = new_var
        self.__recount_fitness()
        # check if it was effectively
        if self.fitness > old_fitness:
            self.solution = old_solution
            self.fitness = old_fitness
            self.trial += 1
        else:
            self.trial = 0

    def reset_random_solution(self):
        r_solution = random.sample(range(self.graph.vertex_num), self.graph.vertex_num)
        self.solution = r_solution
        self.__recount_fitness()
        self.trial = 0

    def __repr__(self):
        return str(self.solution) + "=" + str(self.fitness)

    def __eq__(self, other):
        if not isinstance(other, EmployedBee):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.solution == other.solution
