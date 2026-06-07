import sys
sys.path.insert(0, '..')

import time
import random
import os
import numpy
import pickle

import warnings
warnings.filterwarnings("error")

# from containers import *
from grid import Grid

from deap import tools

from archive import Archive
from behaviours import Behaviours
from logs import Logs
from params import eaParams
from redundancy import Redundancy
from utilities import Utilities


class EA():

    def __init__(self, params):

        start_time = round(time.time() * 1000)

        self.params = params
        self.params.is_qdpy = True
        self.params.using_repertoire = False

        random.seed(self.params.deapSeed)

        self.behaviours = Behaviours(params)

        self.utilities = Utilities(self.params, self.behaviours)
        self.redundancy = Redundancy(self.params)

        self.gp_toolbox = self.utilities.setupToolboxGP(None)

        if not self.utilities.checkContainerSize():
            return

        self.params.makePaths()

        repertoire_path = self.params.shared_path+"/ga/"+self.params.experiment+"/foraging"
        repertoire_file = repertoire_path+"/foraging-"+str(self.params.src_bins[0])+"-bins.txt"
        print("\nReading from "+repertoire_file)

        self.repertoire = self.utilities.createContainer(self.params.src_bins,
                                                         self.params.src_domain,
                                                         self.params.max_items_per_bin)
        self.utilities.updateContainerFromString(self.redundancy, self.gp_toolbox,
                                                 self.repertoire, repertoire_file,
                                                 0, 0, 0)

        print()
        flat_indexes = []
        grid_indexes = []

        if self.params.usingNewGrid:
            flat_indexes.extend(range(len(self.repertoire.items())))
            grid_indexes = [key for key, value in self.repertoire.items()]
            print("repertoire size "+str(len(self.repertoire.values()))+"\n")
        else:
            container = self.repertoire.solutions.items()
            flat_indexes = [self.repertoire.items.index(inds[0]) for index, inds in container if len(inds) > 0]
            grid_indexes = [self.repertoire.index_grid(inds[0].features) for index, inds in container if len(inds) > 0]
            print("repertoire size "+str(len(self.repertoire))+"\n")

        self.utilities.toolbox = self.utilities.setupToolboxGA(self.repertoire, self.mutateOneIndividual, flat_indexes, grid_indexes)

        self.logs = Logs(self.params, self.utilities)

        self.utilities.saveConfigurationFile()
        self.toolbox = self.utilities.toolbox

        self.CXPB, self.MUTPB = 0.5, 1.0

        self.archive = Archive(params, None)

        end_time = round(time.time() * 1000)

        duration = end_time - start_time
        self.params.console("\nLoading time: " +self.utilities.formatDuration(duration)+"\n")


    def run(self):

        if self.params.cancelled:
            self.params.console("\naborted\n")
            return

        start_time = round(time.time() * 1000)

        self.archive.getArchives()

        self.utilities.saveParams()

        self.container = self.utilities.createContainer(self.params.nb_bins,
                                                        self.params.features_domain,
                                                        self.params.max_items_per_bin)

        self.current_batch = self.utilities.toolbox.population(n = self.params.populationSize)

        generation = 0
        self.evaluateNewPopulation(generation, self.current_batch, "w")
        self.params.runtime()

        self.eaLoop(generation)

        self.archive.saveArchive(None, self.params.generations)

        # self.params.deleteTempFiles()

        end_time = round(time.time() * 1000)
        self.utilities.saveDuration(start_time, end_time)

        time.sleep(self.params.eaRunSleep)

    def eaLoop(self, generation):

        max_gen = self.params.generations

        while (generation < max_gen):

            generation += 1

            population = list(self.container.values()) if self.params.usingNewGrid else self.container
            offspring = self.utilities.toolbox.select(population, self.params.populationSize)
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

            self.evaluateNewPopulation(generation, offspring, "a")

            self.current_batch = offspring

            self.params.runtime()
            max_gen = self.params.generations

            self.archive.saveArchive(None, self.params.generations)
            self.logs.saveCSV(generation, population)

    def evaluateNewPopulation(self, generation, offspring, mode):

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        invalid_orig = len(invalid_ind)

        matched = [0,0]
        invalid_ind = self.archive.assignDuplicateFitness(invalid_ind, self.assignFitness, matched)
        archive_ind = invalid_ind

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        invalid_new = len(invalid_ind)

        self.utilities.evaluate(self.assignPopulationFitness, invalid_ind)

        for ind in archive_ind:
            self.archive.addToCompleteArchive(str(ind), tuple([ind.fitness.values[0]] + ind.features))

        for ind in invalid_ind:
            self.archive.addToArchive(str(ind), tuple([ind.fitness.values[0]] + ind.features))

        self.utilities.removeDuplicates(offspring, self.container)

        if self.params.usingNewGrid:
            self.container.update(offspring)
        else:
            self.container.update(offspring, issue_warning = self.params.show_warnings)

        self.printOutput(generation, invalid_new, invalid_orig, matched)

        if (self.params.printExtrema and (generation % self.params.verbose_interval == 0 or generation == self.params.generations)):
            self.params.console(self.utilities.printExtrema(self.container))
            filename = self.params.path()+"extrema.txt"
            if os.path.exists(self.params.path()):
                with open(filename, "w") as f:
                    f.write(self.utilities.printExtrema(self.container, True))

        if self.params.printBestIndividuals and generation == self.params.generations:
            best = self.utilities.getBestSwarmFromContainer(self.container)
            self.utilities.printHeterogeneousSwarm(self.repertoire, best)
            qd_score_and_coverage = "QD Score: "+str("%.9f" % self.utilities.getAdjustedQDScore(self.container))+"\n"
            qd_score_and_coverage += "Coverage: "+str("%.9f" % self.utilities.getCoverage(self.container))+"\n"
            self.params.console(qd_score_and_coverage)
            self.params.console(self.utilities.printRepertoireQdScores(self.container))

        if self.params.saveCSV:
            self.logs.logFitness(generation, [self.utilities.getBestSwarmFromContainer(self.container)])
            self.logs.logQdScore(generation, [self.utilities.getQDScore(self.container)])
            self.logs.logCoverage(generation, self.utilities.getCoverage(self.container))

        if generation != 0 and generation % 100 == 0 and invalid_new == 0:
            time.sleep(10.0)

        if invalid_new > 0:
            time.sleep(self.params.genSleep)

    def printOutput(self, generation, invalid_new, invalid_orig, matched):

        best = self.utilities.getBestSwarmFromContainer(self.container)
        fitness = str("%.6f" % best.fitness.values[0])

        coverage = str("%.4f" % self.utilities.getCoverage(self.container))
        filled = str(int(self.utilities.getFilledBins(self.container)))
        total = str(self.params.nb_bins[0] * self.params.nb_bins[1] * self.params.nb_bins[2])

        qd_score = str("%.6f" % self.utilities.getAdjustedQDScore(self.container))

        description = self.params.description

        output_string = "\t"+description+" - "+str(self.params.deapSeed)+" - "+str(generation)+"\t | "
        output_string += fitness+" | "
        output_string += filled+" / "+total+" | "
        output_string += qd_score
        output_string += "\t| invalid "+str(invalid_new)+" / "+str(invalid_orig)
        output_string += " (matched "+str(matched[0])+" & "+str(matched[1])+")"

        write_out = False
        if generation % self.params.output_interval == 0 and invalid_new > 0: write_out = True
        if generation % 100 == 0 or generation == self.params.generations: write_out = True
        if write_out: self.params.console(output_string)

    def assignFitness(self, offspring, fitness):
        offspring.fitness.values = (fitness[0],)
        offspring.features = [fitness[1], fitness[2], fitness[3]]

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

    def selTournament(self, individuals, k, tournsize, fit_attr="fitness"):

        chosen = []
        for i in range(k):
            aspirants = tools.selRandom(individuals, tournsize)
            best = self.utilities.getBestHDRandom(aspirants, 0)
            chosen.append(best)
        return chosen
