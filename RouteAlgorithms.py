from mathDistance import EuclideanDistance, SumDistance
from RObjects import *
from random import *
import pyglet
class NNRoute:

    @staticmethod
    def Solve(Nodes):
        _Nodes = Nodes.copy()
        """ reorder list of Nodes visit, chosing the closet city each turn"""
        routeNodes = []
        # Initialize
        currentNode = _Nodes[0]
        routeNodes.append(currentNode)
        # remove the start of the Route
        _Nodes.remove(currentNode)
        # Iterate
        while len(routeNodes) != len(Nodes) and len(_Nodes):
            closetNode = NNRoute.closetSearch(currentNode, _Nodes)
            # Update list, current City
            currentNode = closetNode
            routeNodes.append(currentNode)
            _Nodes.remove(currentNode)
        return routeNodes

    @staticmethod
    def closetSearch(startObj, targetObj_ls):
        """ 
        Take a StartObject and a list of TargetsObjects and calculate which one is closet
        return the Closet target
        """
        minDist = EuclideanDistance(targetObj_ls[0].loc, startObj.loc)
        closetTarget = targetObj_ls[0]
        # Iterate all targets
        for tObj in targetObj_ls:
            if EuclideanDistance(tObj.loc, startObj.loc) < minDist:
                minDist = EuclideanDistance(tObj.loc, startObj.loc)
                closetTarget = tObj
        return closetTarget
    

class LocalSearch:
    @staticmethod
    def _Opt2swap(Route, i, k):
        return Route[:i+1] + Route[k:i:-1] + Route[k+1:]

    @staticmethod
    def Opt2Solve(Route):
        improved = True
        while improved:
            improved = False
            bestDistance = SumDistance([node.loc for node in Route])
            for i in range(1,len(Route)-2):
                for k in range(i+1, len(Route) - 1):
                    newRoute = LocalSearch._Opt2swap(Route, i, k)
                    newDist = SumDistance([node.loc for node in newRoute])
                    #print(i, k, str([c.name for c in newRoute]), newDist)
                    if newDist < bestDistance:
                        improved = True
                        Route = newRoute
        return Route

class GA():
    popMax = 500
    step = 100
    mutationRate = 0.01
    bestGene = None
    bestDistance = None

    @staticmethod
    def initPopulation(gene):
        pop = []
        #pop.append(Graph(gene))
        for _ in range(GA.popMax):
            pop.append(Graph([gene[0]] + sample(gene[1:], len(gene) - 1)))
        return pop
    
    @staticmethod
    def evalFitness(graph):
        graph.fitness = 1 / graph.totalDistance()
        return graph.fitness

    @staticmethod
    def normalizeFitness(population, sumfitness):
        for graph in population:
            graph.fitness = graph.fitness / sumfitness

    @staticmethod
    def select(population):
        i = 0
        r = random()
        while (r > 0):
            r -= population[i].fitness
            i += 1
        return population[i-1]

    @staticmethod
    def mutate(population):
        for graph in population:
            if random() < GA.mutationRate:
                index1 = randint(0,len(graph.Nodes)-1)
                k = randint(1, len(graph.nodes)-1)
                index2 = (k+1) % len(graph.Nodes)
                graph.Nodes[index1], graph.Nodes[index2] = graph.Nodes[index2], graph.Nodes[index1]
    
    @staticmethod
    def crossover(graphA, graphB):
        geneA = graphA.Nodes.copy()
        geneB = graphB.Nodes.copy()
        length = len(geneA)
        i = randint(1,len(geneA)-1)
        newGene = [geneA[0]]
        newGene.append(geneA[i])
        while len(newGene) != len(geneA):
            """ iterate through gene1 """
            k = i
            c1 = geneA[(k+1)%len(geneA)]
            while c1 in newGene:
                k += 1
                c1 = geneA[(k+1)%len(geneA)]
            """ iterate through gene2 """
            k = i
            c2 = geneB[(i+1)%len(geneA)]
            while c2 in newGene:
                k += 1
                c2 = geneB[(k+1)%len(geneA)]
            if EuclideanDistance(c1.loc, newGene[-1].loc) <= EuclideanDistance(c2.loc, newGene[-1].loc):
                newGene.append(c1)
            else:
                newGene.append(c2)
            i+= 1
        return newGene
        
    @staticmethod
    def _Evolving(population, bestNodes):
        GA.bestGene = Graph(bestNodes)
        maxDist = None
        minDist = None
        bestRoute = None
        for route in population:
            d = route.totalDistance()
            if None in [maxDist, minDist, bestRoute]:
                maxDist = d
                minDist = d
                bestRoute = route
            if None in [GA.bestDistance, GA.bestGene]:
                GA.bestDistance = d
                GA.bestGene = route
            if d < GA.bestDistance:
                GA.bestDistance = d 
                GA.bestGene = route
            if d < minDist:
                minDist = d
                bestRoute = route
            if d > maxDist:
                maxDist = d
        print(GA.bestGene.totalDistance())
        sumfitness = 0
        for route in population:
            route.fitness = 1 / route.totalDistance()
            sumfitness += route.fitness
        #normalize fitness
        for route in population:
            route.fitness /= sumfitness
        newGeneration = []
        # Creating new generation
        for _ in range(len(population)):
            a = GA.select(population)
            b = GA.select(population)
            route = GA.crossover(a, b)
            newGeneration.append(Graph(route))
        return newGeneration, GA.bestGene.Nodes

    @staticmethod
    def Solve(nodes):
        pop = GA.initPopulation(nodes)
        for _ in range(GA.step):
            pop, GA.bestGene = GA._Evolving(pop, GA.bestGene)
        return GA.bestGene
