

import random
import pickle

class Checkpoint():

    def __init__(self, params):
        self.params = params

    def read(self):

        with open(self.params.checkpointInputFilename(self.params.start_gen), "rb") as checkpoint_file:
            checkpoint = pickle.load(checkpoint_file)
        population = checkpoint["population"]
        containers = checkpoint["containers"]
        generation = checkpoint["generation"]
        fitness = checkpoint["fitness"]
        qd_scores = checkpoint["qd_scores"]
        coverage = checkpoint["coverage"]
        save_interval = checkpoint["save_interval"]

        print("============================================")
        print("generation: "+str(generation))

        print("population size: "+str(len(population)))

        for i in range(len(containers)):
            print("container "+str(i)+": "+str(len(containers[i])))

        print("============================================")

        fitness = fitness[0:-1].split(",")
        qd_scores = qd_scores[0:-1].split(",")
        coverage = coverage[0:-1].split(",")

        print("save interval: "+str(save_interval))
        print("fitness: "+str(fitness))
        print("qd score: "+str(qd_scores))
        print("coverage: "+str(coverage))

        return population

    def load(self, logs, grid):

        with open(self.params.checkpointInputFilename(self.params.start_gen), "rb") as checkpoint_file:
            checkpoint = pickle.load(checkpoint_file)

        random.setstate(checkpoint["rndstate"])

        grid.grids = checkpoint["containers"]

        self.params.csv_save_interval = checkpoint["save_interval"]
        logs.best = checkpoint["fitness"]
        logs.qd_scores = checkpoint["qd_scores"]
        logs.coverage = checkpoint["coverage"]

        return checkpoint["population"]

    def save(self, generation, population, containers, logs):
        
        if self.params.saveOutput and (generation % self.params.save_period == 0 or generation == self.params.generations):

            checkpoint = dict(containers=containers,
                              population=population,
                              generation=self.params.generations,
                              fitness=logs.best,
                              qd_scores=logs.qd_scores,
                              coverage=logs.coverage,
                              save_interval=self.params.csv_save_interval,
                              rndstate=random.getstate())

            with open(self.params.checkpointOutputFilename(generation), "wb") as checkpoint_file:
                 pickle.dump(checkpoint, checkpoint_file)
