
import array
import numpy
import os
import random
import subprocess
import threading
import time

from deap import tools
from deap import base
from deap import creator
from deap import cma

from datetime import datetime


class Utilities():

    def __init__(self, params):
        self.params = params
        self.setupToolbox()

    def setupToolbox(self):

        toolbox = base.Toolbox()

        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)

        toolbox.register("evaluate", self.evaluateRobot)

        strategy = cma.Strategy(centroid=[0.0]*self.params.ind_size, sigma=self.params.sigma, lambda_=self.params.population_size)
        toolbox.register("generate", strategy.generate, creator.Individual)
        toolbox.register("update", strategy.update)

        self.evaluation_functions = []
        for i in range(1, self.params.num_threads + 1):
            toolbox.register("evaluate"+str(i), self.evaluateRobot, thread_index=i)
            self.evaluation_functions.append(self.makeEvaluationFunction("evaluate"+str(i)))

        self.toolbox = toolbox

    def setSeed(self):
        numpy.random.seed(self.params.seed)

    def evaluateRobot(self, individual, thread_index):

        # save number of robots and chromosome to file
        with open(self.params.local_path+'/chromosome'+str(thread_index)+'.txt', 'w') as f:
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
            with open(self.params.local_path+'/seed'+str(thread_index)+'.txt', 'w') as f:
                f.write(str(seed))
                f.write("\n")
                f.write(str(i))

            # run argos
            subprocess.call(["/bin/bash", "./evaluate", str(thread_index), self.params.local_path, "", "./"])

            # result from file
            with open(self.params.local_path+"/result"+str(thread_index)+".txt", 'r') as f:

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

        try:
            os.remove(self.params.local_path+"/seed"+str(thread_index)+".txt")
            os.remove(self.params.local_path+"/chromosome"+str(thread_index)+".txt")
            os.remove(self.params.local_path+"/result"+str(thread_index)+".txt")
        except Exception as e:
            now = datetime.now()
            self.params.console(str(e))
            with open(self.params.shared_path+"/cma-es/errors"+str(self.params.seed)+".txt", "a") as f:
                f.write(now.strftime("%H:%M %d/%m/%Y")+" ")
                f.write(str(e))
                f.write("\n")
            with open(self.params.local_path+"/runtime.txt", "w") as f:
                f.write("stop\n")

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
        
        fitnesses = ""
        for i in population:
            fitnesses += str(i.fitness.getValues()[0])+"\n"
        fitnesses += "\n"
        self.params.console(fitnesses)

    def saveConfigurationFile(self):
        experiment_length = 500 if self.params.objective == "foraging" else 100
        with open(self.params.local_path+'/configuration.txt', 'w') as f:
            f.write("numInputs:"+str(self.params.num_inputs))
            f.write("\n")
            f.write("numHidden:"+str(self.params.num_hidden))
            f.write("\n")
            f.write("numOutputs:"+str(self.params.num_outputs))
            f.write("\n")
            f.write("experimentLength:"+str(experiment_length))
            f.write("\n")
            f.write("sqrtRobots:"+str(self.params.sqrt_robots))

    def saveParams(self):

        if self.params.saveOutput or self.params.saveCSV or self.params.saveBest:

            params_string = "---\n\n"

            with open("../revision.txt", "r") as f:
                for line in f:
                    params_string += "revision "+line+"\n"

            params_string += "time: "+str(time.ctime()) + "\n"
            params_string += "seed: "+str(self.params.seed) + "\n"
            params_string += "\n"

            with open(self.params.shared_path+"/config.txt", "r") as f:
                for line in f:
                    params_string += line

            with open(self.params.paramsFilename(), 'a') as f:
                f.write("\n"+params_string+"\n")

    def formatDuration(self, duration):

        hours = int(duration / 3600000)
        minutes = int((duration % 3600000) / 60000)
        seconds = int((duration % 60000) / 1000)

        duration_str = ""
        if hours > 0: duration_str += str(hours)+"h "
        if hours > 0 or minutes > 0: duration_str += str(minutes)+"m "
        duration_str += str(seconds)+"s"

        return duration_str

    def saveDuration(self, start_time, end_time):

        duration = end_time - start_time
        duration_str = self.formatDuration(duration)
        self.params.console("\nDuration: " + duration_str + "\n")

        if self.params.saveOutput or self.params.saveCSV or self.params.saveBest:
            with open(self.params.paramsFilename(), 'a') as f:
                f.write("-- finish --------------\n\n")
                f.write("generations: "+str(self.params.generations) + "\n")
                f.write("duration: "+duration_str+" ("+str(duration) + " ms)\n")
                f.write("\n")

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
