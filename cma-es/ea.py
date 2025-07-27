# from deap
from operator import attrgetter

# from main
import random

# from bmrr
from deap import algorithms
from deap import creator
from deap import tools

# from bmrr
import time

from utilities import Utilities
from archive import Archive

# to evaluate one chromosome
import subprocess

class EA():
    
    def eaInit(self, cxpb, mutpb):

        start_time = round(time.time() * 1000)
        
        self.utilities = Utilities()
        
        self.description = "action nodes - min/max val -1 to 1 and 10 hidden nodes"

        self.utilities.ind_size = 111
        self.utilities.min_value = -1
        self.utilities.max_value = 1
        self.utilities.min_strategy = 0.5
        self.utilities.max_strategy = 3

        mu, lambda_ = 25,25
        
        self.seed = 0
        self.generations = 0
        self.sqrtRobots = 3
        self.saveOutput = False
        self.saveCSV = False
        self.utilities.objective = "density"
        self.utilities.indexes = [0]
        
        #  self.evaluateOneIndividual()
        #  return

        self.precision = 4

        self.csv = "./test/"+self.utilities.objective+"/results.csv"
        
        if self.seed == 0: self.seed = self.utilities.parseArguments()
        self.cancelled = False
        
        self.utilities.setupToolbox(self.selTournament, self.precision)
        self.archive = Archive(self.utilities)
        
        
        self.archive.getArchives(self.seed)
        random.seed(self.seed)

        toolbox = self.utilities.toolbox
        population = toolbox.population(n=mu)

        self.evaluateNewPopulation(0, population)

        pop = self.eaLoop(population, toolbox, mu, lambda_, cxpb, mutpb)
        
        end_time = round(time.time() * 1000)
        self.utilities.printDuration(start_time, end_time)
        
            
        best = self.utilities.getBest(population)
        bestFitness = best.fitness.getValues()[0]
        print(bestFitness)

        with open('./chromosome.txt', 'w') as f:
            f.write("20")
            for s in best:
                f.write(" ")
                f.write(str(s))
        
        if self.saveOutput:
            self.archive.saveArchive(self.seed)
        
        csv_string = str(self.utilities.objective) +","
        csv_string += str(self.seed) +","
        csv_string += str(self.generations) +","
        csv_string += str(bestFitness) +","
        for c in best:
            csv_string += str(c) + " "
        csv_string = csv_string[0:-1]
        csv_string += "\n"
        print(csv_string)
        
        if self.saveCSV:
            
            with open(self.csv, 'a') as f:
                f.write(csv_string)

        # if self.cancelled == False: time.sleep(30.0)

        return pop


    def eaLoop(self, population, toolbox, mu, lambda_, cxpb, mutpb):

        toolbox = self.utilities.toolbox

        #  with open(self.csv, 'w') as f:
            #  f.write("")

        gen = 0
        while gen < self.generations:
            
            gen += 1
            self.configure()
            
            # ===================
                
            best = self.utilities.getBest(population)
            bestFitness = best.fitness.getValues()[0]

            # ===================
                
            elites = []
            for i in range(1): # should come from params (features)
                elites.append(self.utilities.getBest(population))
            
            offspring = []
            for ind in population:
                if ind not in elites:
                    offspring.append(ind)
            
            offspring = algorithms.varOr(offspring, toolbox, lambda_, cxpb, mutpb)

            if self.precision != 0:
                for ind in offspring:
                    for i in range(self.utilities.ind_size):
                        ind[i] = round(ind[i], self.precision)
                    

            self.evaluateNewPopulation(gen, elites + offspring)
            
            # hard coded for only one elite
            elites[0] = self.utilities.getBest(elites + offspring)

            population[:] = elites + toolbox.select(offspring, mu - len(elites))
            
        return population


    def evaluateNewPopulation(self, generation, population):
        
        invalid_ind = [ind for ind in population if not ind.fitness.valid]
        invalid_orig = len(invalid_ind)

        matched = [0,0]
        invalid_ind = self.archive.assignDuplicateFitness(invalid_ind, self.assignFitness, matched)
        archive_ind = invalid_ind

        invalid_ind = [ind for ind in population if not ind.fitness.valid]
        invalid_new = len(invalid_ind)
        
        self.utilities.evaluate(self.assignPopulationFitness, invalid_ind)
    
        for ind in invalid_ind:
            self.archive.addToArchive(ind)
        
        for ind in archive_ind:
            self.archive.addToCompleteArchive(ind)

        best = self.utilities.getBest(population)
        
        scores = ""
        for i in range(1): # should come from params (features)
            scores += str("%.7f" % best.fitness.getValues()[i]) + "\t"
        
        if (generation % 1 == 0 or invalid_new > 0):
            print ("\t"+str(generation)+" - "+str(scores)+"\tinvalid "+str(invalid_new)+" / "+str(invalid_orig)+" (matched "+str(matched[0])+" & "+str(matched[1])+")")
            
        return population
            
    def assignFitness(self, offspring, fitness):
        offspring.fitness.values = fitness

    def assignPopulationFitness(self, population, fitnesses):
        for ind, fit in zip(population, fitnesses):
            ind.fitness.values = fit

    def selTournament(self, individuals, k, tournsize, fit_attr="fitness"):
        chosen = []
        for i in range(k):
            aspirants = tools.selRandom(individuals, tournsize)
            chosen.append(max(aspirants, key=attrgetter(fit_attr)))
        return chosen

    def configure(self):
        f = open("../config.txt", "r")
        for line in f:
            data = line.split()
            if len(data) > 0:
                for d in data:
                    print(d)
                if data[0] == "generations": self.generations = int(data[1])
                if data[0] == "saveOutput": self.saveOutput = False if data[1] == "False" else True
                if data[0] == "saveCSV": self.saveCSV = False if data[1] == "False" else True
                if data[0] == "cancel":
                    self.saveOutput = False
                    self.saveCSV = False
                    self.generations = 0
                    self.cancelled = True
        
    def evaluateOneIndividual(self):
        
        # evaluates the individual in ./chromosome.txt and prints its fitness score
        
        thread_index = 1
        
        with open('./chromosome.txt', 'r') as f:
            for line in f:
                chromosome = line
        
        with open('./txt/chromosome'+str(thread_index)+'.txt', 'w') as f:
            f.write(line)

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
            
            for line in f:
                first = line[0:line.find(" ")]
                if (first == "result"):
                    lines = line.split()
                    robotId = int(float(lines[1]))
                    robots[robotId] = []
                    for j in range(7):
                        for k in range(5): # should come from params (iterations)
                            if j in self.utilities.indexes:
                                index = (j * 5) + k + 2 # should come from params (j * self.params.iterations) + k + 2
                                robots[robotId].append(float(lines[index]))
            
            # get scores for each robot and add to cumulative total
            totals[0] += self.utilities.collectFitnessScore(robots, 0)
            
        # divide to get average per seed and arena configuration then apply derating factor
        deratingFactor = 1.0
        features = []
        
        for i in range(1): # should come from params (features)
            fitness.append(self.utilities.getAvgAndDerate(totals[i], deratingFactor))
        
        print(fitness)
