#!/usr/bin/env python3
from sys import argv
from RObjects import Graph, Node
from RouteAlgorithms import NNRoute, LocalSearch
from visual import *

def _generateCities():
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
    graph = Graph(_generateCities())
    #graph.Nodes = NNRoute.Solve(graph.Nodes)
    #graph.Nodes = LocalSearch.Opt2Solve(graph.Nodes)

    window = Window(root)
    window.addNodes(graph.Nodes)
    window.plot()

    mainloop()
main()

