import sys
sys.path.insert(0, '..')

import time
import random
import os
import numpy
import pickle

import warnings
warnings.filterwarnings("error")

from qdpy.phenotype import *
from containers import *

from deap import tools

from params import eaParams
from behaviours import Behaviours
from redundancy import Redundancy
from utilities import Utilities


class EA():

    def __init__(self, params):

        self.params = params
        self.params.is_qdpy = True
        self.params.using_repertoire = False
        self.params.deapSeed = 1
        self.params.makePaths()

        random.seed(self.params.deapSeed)

        self.behaviours = Behaviours(params)

        self.utilities = Utilities(self.params, self.behaviours)
        self.redundancy = Redundancy(self.params)

        self.repertoire = (Grid(shape = [50,50,50],
                                max_items_per_bin = 1,
                                fitness_domain = [(0.0,1.0),],
                                features_domain = [(0,0.2), (0,0.2), (0,0.2)],
                                storage_type=list))

        self.gp_toolbox = self.utilities.setupToolboxGP(self.emptyTournament)
        path = self.params.shared_path+"/ga/"+self.params.experiment+"/foraging/foraging.txt"
        self.utilities.updateContainerFromString(self.redundancy, self.gp_toolbox, self.repertoire, path)

        print()
        flat_indexes = []
        grid_indexes = []
        for idx, inds in self.repertoire.solutions.items():
            if len(inds) > 0:
                ind = inds[0]
                idx2 = self.repertoire.items.index(ind)
                ig = self.repertoire.index_grid(ind.features)
                flat_indexes.append(idx2)
                grid_indexes.append(list(ig))
        print("repertoire size "+str(len(self.repertoire))+"\n")

        self.utilities.toolbox = self.utilities.setupToolboxGA(self.repertoire, self.mutateOneIndividual, flat_indexes, grid_indexes)

        self.utilities.saveConfigurationFile()
        self.toolbox = self.utilities.toolbox

        self.CXPB, self.MUTPB = 0.5, 1.0

    def run(self, init_batch = None, **kwargs):

        if self.params.cancelled:
            self.params.console("\naborted\n")
            return

        start_time = round(time.time() * 1000)
        self.utilities.saveParams()

        self.container = Grid(shape = self.params.nb_bins,
                              max_items_per_bin = self.params.max_items_per_bin,
                              fitness_domain = self.params.fitness_domain,
                              features_domain = self.params.features_domain,
                              storage_type=list)

        self.current_batch = self.utilities.toolbox.population(n = self.params.populationSize)
        generation = 0
        self.evaluateNewPopulation(self.container, generation, self.current_batch, "w")
        self.params.runtime()

        self.eaLoop(self.container, generation)

        # self.params.deleteTempFiles()

        end_time = round(time.time() * 1000)
        self.utilities.saveDuration(start_time, end_time)

        time.sleep(self.params.eaRunSleep)

    def eaLoop(self, container, generation):

        max_gen = self.params.generations

        while (generation < max_gen):

            generation += 1

            offspring = self.utilities.toolbox.select(container, self.params.populationSize)
            offspring = list(map(self.utilities.toolbox.clone, offspring))

            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                rand = random.random()
                if rand < self.params.crossoverProbability:
                    self.utilities.toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values

            for mutant in offspring:
                if random.random() < self.params.mutNRProbability:
                    self.utilities.toolbox.mutate(mutant)
                    del mutant.fitness.values

            self.evaluateNewPopulation(container, generation, offspring, "a")

            self.current_batch = offspring

            self.params.runtime()
            max_gen = self.params.generations

    def transferTrimmedFitnessScores(self, offspring, trimmed):
        for i in range(len(offspring)):
            offspring[i].fitness.values = trimmed[i].fitness.values
            offspring[i].features = trimmed[i].features

    def evaluateNewPopulation(self, container, generation, offspring, mode):

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        invalid_new = len(invalid_ind)

        self.utilities.evaluate(self.assignPopulationFitness, invalid_ind)

        self.utilities.removeDuplicates(offspring, container)

        nb_updated = container.update(offspring, issue_warning = self.params.show_warnings)

        self.printOutput(generation, invalid_new)

        if generation != 0 and generation % 100 == 0 and invalid_new == 0:
            time.sleep(10.0)

        if invalid_new > 0:
            time.sleep(self.params.genSleep)

    def printOutput(self, generation, invalid_new):

        best = self.utilities.getBestHeterogenousSwarm(self.container)
        fitness = str("%.6f" % best.fitness.values[0])

        coverage = str("%.4f" % self.utilities.getCoverage(self.container))
        filled = str(len(self.container))
        total = str(self.params.nb_bins[0] * self.params.nb_bins[1] * self.params.nb_bins[2])

        qd_score = str("%.6f" % self.utilities.getAdjustedQDScore(self.container))

        description = self.params.description

        output_string = "\t"+description+" - "+str(self.params.deapSeed)+" - "+str(generation)+"\t | "
        output_string += fitness+" | "
        output_string += filled+" / "+total+" | "
        output_string += qd_score
        output_string += "\t| invalid "+str(invalid_new)

        write_out = False
        if generation % self.params.output_interval == 0 and invalid_new > 0: write_out = True
        if generation % 100 == 0 or generation == self.params.generations: write_out = True
        if write_out: self.params.console(output_string)

    def assignPopulationFitness(self, population, fitnesses):
        for ind, fit in zip(population, fitnesses):
            ind.fitness.values = fit[0]
            ind.features = fit[1]

    def mutateOneIndividual(self, swarm, flat_indexes, grid_indexes, indpb=0.05):

        index = int(random.random() * len(swarm))
        swarm[index] = random.choice(grid_indexes)

    def mutateAllAxes(self, swarm, flat_indexes, grid_indexes, indpb=0.05):

        count = 0
        for index in range(len(swarm)):
            if random.random() < 0.5:
                swarm[index] = random.choice(grid_indexes)
                count += 1
        return swarm

    def mutateOneAxis(self, swarm, flat_indexes, grid_indexes, indpb=0.05):

        for index in range(len(swarm)):

            ind = swarm[index]
            axis = random.choice([0,1,2])
            if axis == 0: i, j = 1, 2
            if axis == 1: i, j = 0, 2
            if axis == 2: i, j = 0, 1

            candidates = [x for x in grid_indexes if x[i] == ind[i] and x[j] == ind[j] and x[axis] != ind[axis]]

            if (len(candidates) > 0):
                swarm[index] = random.choice(candidates)

        return swarm

    def emptyTournament(self):
        return []

    def selTournament(self, individuals, k, tournsize, fit_attr="fitness"):

        chosen = []
        for i in range(k):
            aspirants = tools.selRandom(individuals, tournsize)
            best = self.utilities.getBestHDRandom(aspirants, 0)
            chosen.append(best)
        return chosen
