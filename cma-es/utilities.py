
import numpy
import subprocess
import threading

from deap import tools
from deap import base
from deap import creator
from deap import cma

import array
import random
import argparse

class Utilities():

    def __init__(self, params):
        self.params = params
        self.setupToolbox()

    def setupToolbox(self):

        toolbox = base.Toolbox()

        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)

        toolbox.register("evaluate", self.evaluateRobot)

        strategy = cma.Strategy(centroid=[0.0]*self.params.ind_size, sigma=self.params.sigma, lambda_=self.params.population_size - self.params.elites)
        toolbox.register("generate", strategy.generate, creator.Individual)
        toolbox.register("update", strategy.update)

        initial_strategy = cma.Strategy(centroid=[0.0]*self.params.ind_size, sigma=self.params.sigma, lambda_=self.params.population_size)
        toolbox.register("generate_first_gen", initial_strategy.generate, creator.Individual)
        toolbox.register("update_first_gen", initial_strategy.update)

        self.evaluation_functions = []
        for i in range(1,9):
            toolbox.register("evaluate"+str(i), self.evaluateRobot, thread_index=i)
            self.evaluation_functions.append(self.makeEvaluationFunction("evaluate"+str(i)))

        self.toolbox = toolbox

    def setSeed(self):
        numpy.random.seed(self.params.seed)

    def evaluateRobot(self, individual, thread_index):
        
        # save number of robots and chromosome to file
        with open('../txt/chromosome'+str(thread_index)+'.txt', 'w') as f:
            f.write(str(self.params.ind_size))
            for s in individual:
                f.write(" ")
                f.write(str(s))

        totals = [0.0]

        fitness = []
        features = []
        robots = {}
        seed = 0

        sqrtRobots = 3 # should come from params (sqrtRobots)

        for i in [0.5, 0.7]: # should come from params (arena params)

            # write seed to file
            seed += 1
            with open('../txt/seed'+str(thread_index)+'.txt', 'w') as f:
                f.write(str(seed))
                f.write("\n")
                f.write(str(i))

            # run argos
            subprocess.call(["/bin/bash", "./evaluate"+str(thread_index), "", "./"])

            # result from file
            f = open("../txt/result"+str(thread_index)+".txt", "r")

            # print ("")
            for line in f:
                first = line[0:line.find(" ")]
                if (first == "result"):
                    #  print (line[0:-1])
                    lines = line.split()
                    robotId = int(float(lines[1]))
                    robots[robotId] = []
                    for j in range(7):
                        for k in range(5): # should come from params (iterations)
                            if j in self.params.indexes:
                                index = (j * 5) + k + 2 # should come from params (j * self.params.iterations) + k + 2
                                robots[robotId].append(float(lines[index]))

            # get scores for each robot and add to cumulative total
            totals[0] += self.collectFitnessScore(robots, 0)

        # divide to get average per seed and arena configuration then apply derating factor
        deratingFactor = 1.0
        features = []

        for i in range(1): # should come from params (features)
            fitness.append(self.getAvgAndDerate(totals[i], deratingFactor))

        return fitness

    def collectFitnessScore(self, robots, feature, maxScore = 1.0):

        thisFitness = 0.0

        # get food collected by each robot and add to cumulative total
        for r in (range(len(robots))):
            for i in range(5): # should come from params (iterations)
                thisFitness += float(robots[r][i])

        # divide to get average for this iteration, normalise and add to running total
        thisFitness /= 3*3 # should come from params (sqrtRobots)
        thisFitness /= maxScore

        return thisFitness

    def getAvgAndDerate(self, score, deratingFactor):
        fitness = score / 5 # should come from params (iterations)
        fitness = fitness / len([0.5, 0.7]) # should come from params (arenaParams)
        fitness /= deratingFactor
        return fitness

    def getBest(self, population, qty = 1):

        best = []
        for ind in population:
            if len(best) < qty:
                best.append(ind)
            else:
                worst = 9999.0
                worstIndex = qty
                for i in range(qty):
                    if best[i].fitness.values[0] < worst:
                        worst = best[i].fitness.values[0]
                        worstIndex = i

                if ind.fitness.values[0] > worst:
                    best[worstIndex] = ind
        return best

    def printPopulationFitness(self, population):
        
        for i in population:
            print(i.fitness.getValues()[0])
        print()

    def printDuration(self, start_time, end_time):

        duration = end_time - start_time
        minutes = (duration / 1000) / 60
        minutes_str = str("%.2f" % minutes)
        print("\nDuration " +minutes_str+" minutes\n")

    def parseArguments(self):
        
        parser = argparse.ArgumentParser()
        parser.add_argument('--seed', type=int, default=None, help="DEAP random seed")
        args = parser.parse_args()

        if args.seed != None:
            return args.seed

    def evaluate(self, assign_fitness, invalid_ind):

        # fitnesses = self.toolbox.map(self.toolbox.evaluate, invalid_ind)
        # assign_fitness(invalid_ind, fitnesses)

        self.split(assign_fitness, invalid_ind)

    def split(self, assign_fitness, population):

        pop = []
        for i in range(self.params.num_threads):
            pop.append([])

        for i in range(len(population)):
            for j in range(self.params.num_threads):
                if i % self.params.num_threads == j:
                    pop[j].append(population[i])
                    continue

        threads = []
        for i in range(self.params.num_threads):
            threads.append(threading.Thread(target=self.evaluation_functions[i], args=(assign_fitness, [pop[i]], getattr(self.toolbox, "evaluate"+str(i+1)))))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

    def makeEvaluationFunction(self, name):

        def _method(assign_fitness, population, evaluation_function):
            toolbox_function = getattr(self.toolbox, name)
            fitnesses = self.toolbox.map(toolbox_function, population[0])
            assign_fitness(population[0], fitnesses)

        return _method
