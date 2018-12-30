
from RObjects import *
from random import sample, uniform, random, randint
from mathDistance import EuclideanDistance
from RouteVisualizer import Window

class GA():
    popMax = 200
    step = 100
    mutationRate = 0.01
    bestGene = None
    bestDistance = None

    @staticmethod
    def initPopulation(gene):
        pop = [Graph(gene)]
        #pop.append(Graph(gene))
        for _ in range(GA.popMax):
            pop.append(Graph([gene[0]]+sample(gene[1:], len(gene)-1)))
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
        return newGene
        
    @staticmethod
    def _Evolving(population, bestNodes=None):
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
        for _ in range(GA.step):
            pop = GA.initPopulation(nodes)
            pop, bestGene = GA._Evolving(pop, GA.bestGene)
        return bestGene

