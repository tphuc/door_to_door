from mathDistance import EuclideanDistance, SumDistance


class Node:
    def __init__(self, name, y, x):
        self.name = name
        self.y = y
        self.x = x
        self.loc = (y, x)



class Graph:
    def __init__(self, Nodes):
        self.Nodes = Nodes

    def totalDistance(self):
        return SumDistance([node.loc for node in self.Nodes])

    def displayRoute(self):
        for node in self.Nodes:
            print(node.name, end='->')
        print('')
    
    def find_shortest_path(self, *algorithm):
        for algo in algorithm:
            self.Nodes = algo(self.Nodes)
        print(self.totalDistance())
    