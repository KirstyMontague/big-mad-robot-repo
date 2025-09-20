
import time

from archive import Archive
from params import Params
from utilities import Utilities

import warnings
warnings.filterwarnings("error")


class EA():
    
    def __init__(self):

        start_time = round(time.time() * 1000)

        self.params = Params()
        self.utilities = Utilities(self.params)
        self.archive = Archive(self.utilities, self.params)
        self.best = None

        self.configure()
        if self.params.cancelled:
            return

        if self.params.seed == 0: self.params.seed = self.utilities.parseArguments()
        if self.params.seed == None:
            print("no seed")
            return

        self.utilities.setSeed()
        self.archive.loadArchives()

        experiment_length = 500 if self.params.objective == "foraging" else 100
        with open('../txt/configuration.txt', 'w') as f:
            f.write("numInputs:"+str(self.params.num_inputs))
            f.write("\n")
            f.write("numHidden:"+str(self.params.num_hidden))
            f.write("\n")
            f.write("numOutputs:"+str(self.params.num_outputs))
            f.write("\n")
            f.write("experimentLength:"+str(experiment_length))
            f.write("\n")
            f.write("sqrtRobots:"+str(self.params.sqrt_robots))

        population = self.eaLoop()

        self.eaFinish(start_time, population)

        # if self.params.cancelled == False: time.sleep(30.0)

    def eaFinish(self, start_time, population):

        end_time = round(time.time() * 1000)
        self.utilities.printDuration(start_time, end_time)


        with open('../txt/best.txt', 'w') as f:
            f.write(str(self.params.ind_size))
            for s in self.best:
                f.write(" ")
                f.write(str(s))

        if self.params.saveOutput:
            self.archive.saveArchive()

        csv_string = str(self.params.objective) +","
        csv_string += str(self.params.seed) +","
        csv_string += str(self.params.generations) +","
        csv_string += str(self.best.fitness.getValues()[0]) +","
        for c in self.best:
            csv_string += str(c) + " "
        csv_string = csv_string[0:-1]
        csv_string += "\n"
        print(csv_string)

        if self.params.saveCSV:
            with open(self.params.csv, 'a') as f:
                f.write(csv_string)

    def eaLoop(self):

        generation = 0

        while generation <= self.params.generations:

            try:
                population = self.utilities.toolbox.generate()
                self.evaluateNewPopulation(generation, population)
                self.utilities.toolbox.update(population)

            except:
                self.params.generations = 0
                self.params.saveCSV = False
                self.params.cancelled = True
                with open('../config.txt', 'a') as f:
                    f.write("stop\n")
                print("\n\nFAILED\n\n")

            self.configure()
            generation += 1

        return population

    def evaluateNewPopulation(self, generation, population):

        invalid_ind = [ind for ind in population if not ind.fitness.valid]
        invalid_orig = len(invalid_ind)

        matched = [0,0]
        invalid_ind = self.archive.assignDuplicateFitness(invalid_ind, self.assignFitness, matched)
        archive_ind = invalid_ind

        invalid_ind = [ind for ind in population if not ind.fitness.valid]
        invalid_new = len(invalid_ind)

        trimmed = self.utilities.trimPopulationPrecision(invalid_ind)
        self.utilities.evaluate(self.assignPopulationFitness, trimmed)
        self.transferTrimmedFitnessScores(invalid_ind, trimmed)

        for ind in invalid_ind:
            self.archive.addToArchive(ind)

        for ind in archive_ind:
            self.archive.addToCompleteArchive(ind)

        best = self.utilities.getBest(population)[0]

        if self.best == None or best.fitness.getValues()[0] > self.best.fitness.getValues()[0]:
            self.best = best

        if (generation % 10 == 0 or invalid_new > 0):
            output = "\t"+str(self.params.seed)+" - "
            output += str(generation)+" - "
            output += str("%.7f" % best.fitness.getValues()[0]) + "\t"
            output += str("%.7f" % self.best.fitness.getValues()[0]) + "\t"
            output += "invalid "+str(invalid_new)+" / "+str(invalid_orig)+" "
            output += "(matched "+str(matched[0])+" & "+str(matched[1])+")"
            print(output)

    def transferTrimmedFitnessScores(self, invalid_ind, trimmed):
        for i in range(len(invalid_ind)):
            invalid_ind[i].fitness.values = trimmed[i].fitness.values

    def assignFitness(self, offspring, fitness):
        offspring.fitness.values = fitness

    def assignPopulationFitness(self, population, fitnesses):
        for ind, fit in zip(population, fitnesses):
            ind.fitness.values = fit

    def configure(self):
        with open("../config.txt", 'r') as f:
            for line in f:
                data = line.split()
                if len(data) > 0:
                    if data[0] == "generations": self.params.generations = int(data[1])
                    if data[0] == "saveOutput": self.params.saveOutput = False if data[1] == "False" else True
                    if data[0] == "saveCSV": self.params.saveCSV = False if data[1] == "False" else True
                    if data[0] == "stop":
                        self.params.saveCSV = False
                        self.params.generations = 0
                        self.params.cancelled = True
                    if data[0] == "cancel":
                        self.params.saveOutput = False
                        self.params.saveCSV = False
                        self.params.generations = 0
                        self.params.cancelled = True

