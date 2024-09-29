

import random
import pickle

class Checkpoint():

    def __init__(self, params):
        self.params = params

    def read(self):

        with open(self.params.checkpointInputFilename(self.params.start_gen), "rb") as checkpoint_file:
            checkpoint = pickle.load(checkpoint_file)
        population = checkpoint["population"]

        print("============================================")
        print("population size: "+str(len(population)))

        print("============================================")
        for ind in population:
            print("")
            print (ind.fitness)
            print (ind)
            print("")
            print("============================================")

        return population

    def load(self):

        # load population and random state from pkl

        with open(self.params.checkpointInputFilename(self.params.start_gen), "rb") as checkpoint_file:
            checkpoint = pickle.load(checkpoint_file)
        population = checkpoint["population"]
        containers = checkpoint["containers"]
        random.setstate(checkpoint["rndstate"])

        best_output = self.getCsvData("best")
        qd_score_output = self.getCsvData("qd-scores")
        coverage_output = self.getCsvData("coverage")

        return population, best_output, qd_score_output, coverage_output, containers

    def getCsvData(self, query):

        # load output for earlier generations from csv

        csvFilename = self.params.csvInputFilename(self.params.start_gen, query)
        f = open(csvFilename, "r")

        for line in f:
            items = line.split(",")
            if len(items) > 1 and items[2] != "Seed":
                if items[0] == self.params.description and \
                   int(items[2]) == self.params.deapSeed and \
                   int(items[4]) == self.params.populationSize and \
                   int(items[5]) == self.params.tournamentSize:
                        output = ""
                        for i in range(9,self.params.start_gen+10):
                            output += items[i]+","

        return output

    def save(self, generation, population, containers):
        
        if self.params.saveOutput and (generation % self.params.save_period == 0 or generation == self.params.generations):

            checkpoint = dict(containers=containers, population=population, generation=self.params.generations, rndstate=random.getstate())

            with open(self.params.checkpointOutputFilename(generation), "wb") as checkpoint_file:
                 pickle.dump(checkpoint, checkpoint_file)
