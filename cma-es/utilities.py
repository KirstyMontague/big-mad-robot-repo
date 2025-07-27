
import subprocess
import time
import threading

from deap import tools
from deap import base
from deap import creator

import array
import random
import argparse

class Utilities():

    def setupToolbox(self, tournament, precision):

        IND_SIZE = self.ind_size
        MIN_VALUE = self.min_value
        MAX_VALUE= self.max_value
        MIN_STRATEGY= self.min_strategy
        MAX_STRATEGY= self.max_strategy

        toolbox = base.Toolbox()

        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", array.array, typecode="d", fitness=creator.FitnessMax, strategy=None)
        creator.create("Strategy", array.array, typecode="d")

        def generateES(icls, scls, size, imin, imax, smin, smax):
            ind = icls(random.uniform(imin, imax) for _ in range(size))
            ind.strategy = scls(random.uniform(smin, smax) for _ in range(size))
            if precision != 0:
                for i in range(IND_SIZE):
                    ind[i] = round(ind[i], precision)
            return ind

        def checkStrategy(minstrategy):
            def decorator(func):
                def wrappper(*args, **kargs):
                    children = func(*args, **kargs)
                    for child in children:
                        for i, s in enumerate(child.strategy):
                            if s < minstrategy:
                                child.strategy[i] = minstrategy
                    return children
                return wrappper
            return decorator

        toolbox = base.Toolbox()
        toolbox.register("individual", generateES, creator.Individual, creator.Strategy, IND_SIZE, MIN_VALUE, MAX_VALUE, MIN_STRATEGY, MAX_STRATEGY)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        toolbox.register("mate", tools.cxESBlend, alpha=0.1)
        toolbox.register("mutate", tools.mutESLogNormal, c=1.0, indpb=0.03)
        toolbox.register("select", tournament, tournsize=3)
        toolbox.register("evaluate", self.evaluateRobot)

        self.evaluation_functions = []
        for i in range(1,9):
            toolbox.register("evaluate"+str(i), self.evaluateRobot, thread_index=i)
            self.evaluation_functions.append(self.makeEvaluationFunction("evaluate"+str(i)))

        toolbox.decorate("mate", checkStrategy(MIN_STRATEGY))
        toolbox.decorate("mutate", checkStrategy(MIN_STRATEGY))
        
        self.toolbox = toolbox

    def evaluateRobot(self, individual, thread_index):
        
        # save number of robots and chromosome to file
        with open('./txt/chromosome'+str(thread_index)+'.txt', 'w') as f:
            #  f.write("20")
            f.write(str(self.ind_size))
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
            with open('./txt/seed'+str(thread_index)+'.txt', 'w') as f:
                f.write(str(seed))
                f.write("\n")
                f.write(str(sqrtRobots))
                f.write("\n")
                f.write(str(i))

            # run argos
            subprocess.call(["/bin/bash", "./evaluate"+str(thread_index), "", "./"])
            
            # result from file
            f = open("./txt/result"+str(thread_index)+".txt", "r")
            
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
                            if j in self.indexes:
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

    def getBest(self, population):
        
        best = None
        bestFitness = 0.0
        for i in population:
            if i.fitness.getValues()[0] > bestFitness or best == None:
                best = i
                bestFitness = i.fitness.getValues()[0]
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

        # fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        # assign_fitness(invalid_ind, fitnesses)

        self.split(assign_fitness, invalid_ind)


    def split(self, assign_fitness, population):

        num_threads = 8

        pop = []
        for i in range(num_threads):
            pop.append([])

        for i in range(len(population)):
            for j in range(num_threads):
                if i % num_threads == j:
                    pop[j].append(population[i])
                    continue

        threads = []
        for i in range(num_threads):
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
