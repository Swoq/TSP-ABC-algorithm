import random


class Graph(object):
    """The Graph class that represent Graph"""

    def __init__(self, vertex_num):
        self.vertex_num = vertex_num
        self.v_dict = {}
        self.e_dict = {}
        self.__create_graph()

    def __create_graph(self):
        for v1 in range(self.vertex_num):
            t = []
            self.v_dict[v1] = t
            for v2 in range(self.vertex_num):
                if v1 != v2:
                    self.v_dict[v1].append(v2)
                    self.e_dict[(v1, v2)] = random.randint(5, 150)
