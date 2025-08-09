
import time

from utilities import Utilities
from archive import Archive


class EA():

    def __init__(self):

        start_time = round(time.time() * 1000)

        self.utilities = Utilities()

        self.utilities.population_size = 8
        self.utilities.elites = 3
        self.utilities.sigma = 5.0

        num_inputs = 9
        num_hidden = 5
        num_outputs = 1

        self.utilities.seed = 1
        self.generations = 3
        self.sqrtRobots = 3
        self.saveOutput = False
        self.saveCSV = False
        self.utilities.objective = "density"
        self.utilities.indexes = [0]
        self.utilities.num_threads = 8
        self.cancelled = False
        self.csv = "./test/"+self.utilities.objective+"/results.csv"

        self.configure()
        if self.cancelled: return

        if self.utilities.seed == 0: self.utilities.seed = self.utilities.parseArguments()
        if self.utilities.seed == None:
            print("no seed")
            return

        self.utilities.num_inputs = num_inputs
        self.utilities.num_hidden = num_hidden
        self.utilities.num_outputs = num_outputs
        self.utilities.ind_size = (num_inputs * num_hidden) + num_hidden + (num_hidden * num_outputs) + num_outputs
        self.utilities.setupToolbox()

        self.archive = Archive(self.utilities)
        self.archive.loadArchives()

        experiment_length = 500 if self.utilities.objective == "foraging" else 100
        with open('../txt/configuration.txt', 'w') as f:
            f.write("numInputs:"+str(self.utilities.num_inputs))
            f.write("\n")
            f.write("numHidden:"+str(self.utilities.num_hidden))
            f.write("\n")
            f.write("numOutputs:"+str(self.utilities.num_outputs))
            f.write("\n")
            f.write("experimentLength:"+str(experiment_length))
            f.write("\n")
            f.write("sqrtRobots:"+str(self.sqrtRobots))

        population = self.eaLoop()

        end_time = round(time.time() * 1000)
        self.utilities.printDuration(start_time, end_time)
        
        best = self.utilities.getBest(population)[0]
        bestFitness = best.fitness.getValues()[0]
        print(bestFitness)

        with open('../txt/best.txt', 'w') as f:
            f.write(str(self.utilities.ind_size))
            for s in best:
                f.write(" ")
                f.write(str(s))
        
        if self.saveOutput:
            self.archive.saveArchive()
        
        csv_string = str(self.utilities.objective) +","
        csv_string += str(self.utilities.seed) +","
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


    def eaLoop(self):

        population = self.utilities.toolbox.generate_first_gen()
        self.evaluateNewPopulation(0, population)
        self.utilities.toolbox.update_first_gen(population)

        gen = 0
        while gen < self.generations:

            gen += 1

            elites = self.utilities.getBest(population, self.utilities.elites)

            population = self.utilities.toolbox.generate()
            population = elites + population

            self.evaluateNewPopulation(gen, population)
            self.utilities.toolbox.update(population)

            self.configure()

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

        best = self.utilities.getBest(population)[0]
        
        scores = ""
        for i in range(1): # should come from params (features)
            scores += str("%.7f" % best.fitness.getValues()[i]) + "\t"
        
        if (generation % 1 == 0 or invalid_new > 0):
            print ("\t"+str(self.utilities.seed)+" - "+str(generation)+" - "+str(scores)+"\tinvalid "+str(invalid_new)+" / "+str(invalid_orig)+" (matched "+str(matched[0])+" & "+str(matched[1])+")")

    def assignFitness(self, offspring, fitness):
        offspring.fitness.values = fitness

    def assignPopulationFitness(self, population, fitnesses):
        for ind, fit in zip(population, fitnesses):
            ind.fitness.values = fit

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
        
