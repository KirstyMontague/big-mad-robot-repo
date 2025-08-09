
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

        fitness = 0.0
        robots = {}
        seed = 0

        for i in self.params.arena_params:

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
                    for j in range(len(self.params.objectives)):
                        for k in range(self.params.arena_iterations):
                            if j == self.params.objective_index:
                                index = (j * self.params.arena_iterations) + k + 2
                                robots[robotId].append(float(lines[index]))

            # average the robots' scores and add to cumulative total
            fitness += self.avgFitnessScore(robots)

        # divide to get average per seed and arena configuration
        fitness /= self.params.arena_iterations
        fitness /= len(self.params.arena_params)

        return (fitness,)

    def avgFitnessScore(self, robots):

        thisFitness = 0.0

        # get food collected by each robot and add to running total
        for r in (range(len(robots))):
            for i in range(self.params.arena_iterations):
                thisFitness += float(robots[r][i])

        # divide to get average for this iteration
        thisFitness /= self.params.sqrt_robots * self.params.sqrt_robots

        return thisFitness

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

    def trimPopulationPrecision(self, population):

        trimmed = [creator.Individual(a) for a in numpy.zeros((len(population), self.params.ind_size))]

        for i in range(len(population)):
            trimmed[i] = self.trimIndividualPrecision(population[i])

        return trimmed

    def trimIndividualPrecision(self, ind):

        trimmed_ind = creator.Individual(numpy.zeros((self.params.ind_size)))

        if self.params.precision != 0:
            for i in range(self.params.ind_size):
                trimmed_ind[i] = round(ind[i], self.params.precision)
        else:
            for i in range(self.params.ind_size):
                trimmed_ind[i] = ind[i]

        return trimmed_ind

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
