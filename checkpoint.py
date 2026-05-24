

import random
import pickle
from utilities import Utilities

class Checkpoint():

    def __init__(self, params):
        self.params = params
        self.utilities = Utilities(params, None)

    def read(self):

        with open(self.params.checkpointInputFilename(self.params.start_gen)+".pkl", "rb") as checkpoint_file:
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

        try:
            for i in range(len(containers)):
                if self.params.usingNewGrid:
                    print("container "+str(i)+": "+str(len(containers[i].items())))
                else:
                    print("container "+str(i)+": "+str(len(containers[i])))
        except:
            print("\n\nFailed to get container length, params.usingNewGrid must match input file format\n")


        print("============================================")

        fitness = fitness[0:-1].split(",")
        qd_scores = qd_scores[0:-1].split(",")
        coverage = coverage[0:-1].split(",")

        print("save interval: "+str(save_interval))
        print("fitness: "+str(fitness))
        print("qd score: "+str(qd_scores))
        print("coverage: "+str(coverage))


        best = []
        for feature in range(self.params.features):
            best.append(self.utilities.getBestFromPopulation(population, feature, False))
        print("best from population: "+str(best[0].fitness.values)+" ("+str(len(best[0]))+" nodes)")

        try:
            for i in range(len(containers)):
                best = self.utilities.getBestFromContainer(containers[i], 0, False)
                print("best from container: "+str(best.fitness.values)+" ("+str(len(best))+" nodes)")
        except:
            print("\n\nFailed to get best from container, params.usingNewGrid must match input file format\n")

        return population

    def load(self, logs):

        with open(self.params.checkpointInputFilename(self.params.start_gen)+".pkl", "rb") as checkpoint_file:
            checkpoint = pickle.load(checkpoint_file)

        type_check = checkpoint["containers"][0].features_domain[0]
        if self.params.usingNewGrid and not isinstance(type_check, list):
            raise ValueError("params.usingNewGrid (currently True) must match input file format")
        if not self.params.usingNewGrid and not isinstance(type_check, tuple):
            raise ValueError("params.usingNewGrid (currently False) must match input file format")

        random.setstate(checkpoint["rndstate"])

        self.params.csv_save_interval = checkpoint["save_interval"]
        logs.best = checkpoint["fitness"]
        logs.qd_scores = checkpoint["qd_scores"]
        logs.coverage = checkpoint["coverage"]

        return checkpoint["population"], checkpoint["containers"]

    def save(self, generation, population, containers, logs):

        if generation % self.params.save_period == 0 or generation == self.params.generations:

            if self.params.saveCheckpoint:

                if not self.params.usingNewGrid:
                    bins = self.params.nb_bins[0] * self.params.nb_bins[1] * self.params.nb_bins[2]
                    if bins > 10 * 10 * 10:
                        raise ValueError("too many bins to save save qdpy checkpoint")

                checkpoint = dict(containers=containers,
                                  population=population,
                                  generation=self.params.generations,
                                  fitness=logs.best,
                                  qd_scores=logs.qd_scores,
                                  coverage=logs.coverage,
                                  save_interval=self.params.csv_save_interval,
                                  rndstate=random.getstate())

                with open(self.params.checkpointOutputFilename(generation)+".pkl", "wb") as checkpoint_file:
                     pickle.dump(checkpoint, checkpoint_file)

            if self.params.saveContainer:

                for i in range(len(containers)):
                    container_string = self.utilities.writeContainerToString(containers[i])
                    filename = self.params.checkpointOutputFilename(generation)+"-"+self.params.objectives[self.params.indexes[i]]+".txt"
                    with open(filename, "w") as f:
                         f.write(container_string)
