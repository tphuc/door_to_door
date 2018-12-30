#!/usr/bin/env python3
from sys import argv
from RObjects import Graph, Node
from RouteAlgorithms import *
from RouteVisualizer import *

def generateNode():
    """ generate nodes from file argument"""
    def _getFileArg(n):
        return argv[n]
    def parseLine(line):
        attrs = [k.strip() for k in line.split(',')]
        return [attrs[0], float(attrs[1]), float(attrs[2])]

    file = _getFileArg(1)
    Nodes = []
    with open(file, 'r') as f:
        for line in f:
            attrs = parseLine(line)
            Nodes.append(Node(attrs[0], attrs[1], attrs[2]))
    return Nodes



def main():
    graph = Graph(generateNode())
    #graph.find_shortest_path(GA.Solve)
    pop = GA.initPopulation(graph.Nodes)
    window = Window()
    window.addNodes(graph.Nodes)
    # window.addAlgoChoice('2opt', LocalSearch.Opt2Solve, graph.Nodes,  returnid = 0)
    # window.addAlgoChoice('NN', NNRoute.Solve, graph.Nodes, returnid = 0)
    window.addAlgoChoice('GA',GA._Evolving, pop, GA.bestGene, returnid = 1)
    window.run()
if __name__ == '__main__':
    main()

