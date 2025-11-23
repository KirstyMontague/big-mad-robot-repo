
import time
import random
import os
import numpy
import pickle

import warnings
warnings.filterwarnings("error")

from pathlib import Path

from qdpy.phenotype import *
from containers import *

from deap import tools

from params import eaParams
from archive import Archive
from checkpoint import Checkpoint
from logs import Logs
from redundancy import Redundancy
from utilities import Utilities
import local



class EA():

    def __init__(self, params):

        self.params = params
        self.params.is_qdpy = True
        random.seed(self.params.deapSeed)

        self.params.local_path += "/"+str(self.params.deapSeed)
        Path(self.params.local_path+"/").mkdir(parents=False, exist_ok=True)

        if self.params.saveOutput or self.params.saveCSV or self.params.saveCheckpoint:
            Path(self.params.shared_path+"/"+self.params.algorithm+"/").mkdir(parents=False, exist_ok=True)
            Path(self.params.shared_path+"/"+self.params.algorithm+"/"+self.params.description+"/").mkdir(parents=False, exist_ok=True)

        if self.params.saveOutput or self.params.saveCheckpoint:
            Path(self.params.path()).mkdir(parents=False, exist_ok=True)

        if self.params.saveOutput:
            Path(self.params.path()+"/csvs").mkdir(parents=False, exist_ok=True)

        self.utilities = Utilities(params)
        self.utilities.setupToolbox(self.selTournament)
        self.utilities.saveConfigurationFile()
        self.toolbox = self.utilities.toolbox

        self.redundancy = Redundancy(self.params)
        self.archive = Archive(params, self.redundancy)
        self.logs = Logs(params, self.utilities)
        self.checkpoint = Checkpoint(self.params)

    def run(self, init_batch = None, **kwargs):

        if self.params.cancelled:
            print("\naborted\n")
            return

        start_time = round(time.time() * 1000)
        self.utilities.saveParams()

        self.archive.getArchives(self.redundancy)

        if self.params.readCheckpoint:
            self.checkpoint.read()
            return

        elif self.params.loadCheckpoint:
            self.current_batch, containers = self.checkpoint.load(self.logs)
            self.container = containers[0]
            generation = self.params.start_gen

        else:
            self.container = Grid(shape = self.params.nb_bins,
                                  max_items_per_bin = self.params.max_items_per_bin,
                                  fitness_domain = self.params.fitness_domain,
                                  features_domain = self.params.features_domain,
                                  storage_type=list)

            self.current_batch = self.toolbox.population(n = self.params.populationSize)
            generation = 0
            self.evaluateNewPopulation(self.container, generation, self.current_batch, "w")
            self.params.runtime()

        self.eaLoop(self.container, generation)

        self.checkpoint.save(self.params.generations, self.current_batch, [self.container], self.logs)
        self.archive.saveArchive(self.redundancy, self.params.generations)
        self.utilities.saveBestIndividuals(self.utilities.getBestMax(self.container, 25), self.params.generations)

        if os.path.exists(self.params.local_path+"/runtime.txt"):
            os.remove(self.params.local_path+"/runtime.txt")
        if os.path.exists(self.params.local_path+"/current.txt"):
            os.remove(self.params.local_path+"/current.txt")
        os.remove(self.params.local_path+"/configuration.txt")
        if len(os.listdir(self.params.local_path)) == 0:
            os.rmdir(self.params.local_path)

        end_time = round(time.time() * 1000)
        self.utilities.saveDuration(start_time, end_time)

        time.sleep(self.params.eaRunSleep)

    def eaLoop(self, container, generation):

        max_gen = self.params.generations

        while (generation < max_gen):

            generation += 1

            time.sleep(self.params.genSleep)

            batch = self.toolbox.select(container, self.params.populationSize)
            offspring = self.varAnd(batch, self.toolbox)

            self.evaluateNewPopulation(container, generation, offspring, "a")

            self.current_batch = offspring

            self.checkpoint.save(generation, self.current_batch, [container], self.logs)
            self.logs.saveCSV(generation, self.utilities.getBestMax(container))
            self.archive.saveArchive(self.redundancy, generation)
            self.utilities.saveBestIndividuals(self.utilities.getBestMax(container, 25), generation)

            self.params.runtime()
            max_gen = self.params.generations

    def transferTrimmedFitnessScores(self, offspring, trimmed):
        for i in range(len(offspring)):
            offspring[i].fitness.values = trimmed[i].fitness.values
            offspring[i].features = trimmed[i].features

    def evaluateNewPopulation(self, container, generation, offspring, mode):

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        invalid_orig = len(invalid_ind)

        matched = [0,0]
        invalid_ind = self.archive.assignDuplicateFitness(invalid_ind, self.assignFitness, matched)
        archive_ind = invalid_ind

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        invalid_new = len(invalid_ind)

        trimmed = self.utilities.getTrimmedPopulation(invalid_ind, self.redundancy)
        self.utilities.evaluate(self.assignPopulationFitness, trimmed)
        self.transferTrimmedFitnessScores(invalid_ind, trimmed)

        for ind in archive_ind:
            self.archive.addToCompleteArchive(str(ind), tuple([ind.fitness.values[0]] + ind.features))

        for ind in invalid_ind:
            self.archive.addToArchive(str(ind), tuple([ind.fitness.values[0]] + ind.features))
            
        if self.params.printOffspring:
            print ("\nPrint all offspring\n")
            for ind in offspring:
                performance = str("%.5f" % ind.fitness.values[0]) + "  \t"
                for f in ind.features:
                    performance += str("%.5f" % f) + " \t"
                print (performance)
            print ("---")
        
        # removing duplicates here because container throws away the individual that would have been replaced before throwing away the duplicate
        self.utilities.removeDuplicates(offspring, container)

        nb_updated = container.update(offspring, issue_warning = self.params.show_warnings)

        self.printOutput(generation, invalid_new, invalid_orig, matched)

        if (self.params.printContainer):
            print ("\nPrint all individuals in container\n")
            self.utilities.printContainer(container)

        if (self.params.printBestIndividuals):
            self.utilities.printBestMax(container)
            qdscore = self.utilities.getQDScore(container)
            coverage = self.utilities.getCoverage(container)
            print("QD Score: "+str("%.9f" % qdscore))
            print("Coverage: "+str("%.9f" % coverage))
            print("")

        if self.params.saveCSV or self.params.saveCheckpoint: # all seeds
            self.logs.logFitness(generation, self.utilities.getBestMax(container))
            self.logs.logQdScore(generation, [self.utilities.getQDScore(container)])
            self.logs.logCoverage(generation, self.utilities.getCoverage(container))

        if self.params.saveOutput: # one seed
            self.utilities.saveQDScore(container, generation, mode)
            self.utilities.saveCoverage(container, generation, mode)
            self.utilities.saveBestToCsv(container, generation, mode)

    def printOutput(self, generation, invalid_new, invalid_orig, matched):
        
        avg = 0
        for x in self.container:
            avg += len(x)
        avg = avg / len(self.container)
        avg_string = str("%.1f" % avg)
        
        # no repro after this change (29/7/25) because no longer using RNG
        best = self.utilities.getBestHDRandom(self.container, 0)
        best_length = str(len(best))
        best_fitness = str("%.6f" % best.fitness.values[0])
        derated = best.fitness.values[0] * self.utilities.deratingFactor(best)
        fitness = str("%.6f" % derated)+" ("+best_fitness+")"
        
        output_string = "\t"+str(self.params.deapSeed)+" - "+str(generation)+"\t| "
        output_string += avg_string+" | "+fitness+" - "+best_length
        output_string += "\t| invalid "+str(invalid_new)+" / "+str(invalid_orig)
        output_string += " (matched "+str(matched[0])+" & "+str(matched[1])+")"
        
        if generation % 100 == 0 or generation == self.params.generations or invalid_new > 0:
            print (output_string)

        if (generation % 10 == 0):
            filename = self.params.shared_path+"/qdpy/console"+str(self.params.deapSeed)+".txt"
            with open(filename, 'a') as f:
                f.write(output_string+"\n")


    def assignFitness(self, offspring, fitness):
        offspring.fitness.values = (fitness[0],)
        offspring.features = [fitness[1], fitness[2], fitness[3]]

    def assignPopulationFitness(self, population, fitnesses):
        for ind, fit in zip(population, fitnesses):
            ind.fitness.values = fit[0]
            ind.features = fit[1]

    def selTournament(self, individuals, k, tournsize, fit_attr="fitness"):

        chosen = []
        for i in range(k):
            aspirants = tools.selRandom(individuals, tournsize)
            feature = int(random.random() * self.params.features)
            best = self.utilities.getBestHDRandom(aspirants, feature)
            chosen.append(best)
        return chosen

    def varAnd(self, population, toolbox):
        
        # apply crossover and mutation
        
        offspring = [toolbox.clone(ind) for ind in population]
        
        # crossover
        for i in range(1, len(offspring), 2):
            if random.random() < self.params.crossoverProbability:
                offspring[i - 1], offspring[i] = toolbox.mate(offspring[i - 1],
                                                                             offspring[i])
                del offspring[i - 1].fitness.values, offspring[i].fitness.values

        # mutation - subtree replacement
        for i in range(len(offspring)):
            if random.random() < self.params.mutSRProbability:
                offspring[i], = toolbox.mutSubtreeReplace(offspring[i])
                del offspring[i].fitness.values

        # mutation - subtree shrink
        for i in range(len(offspring)):
            if random.random() < self.params.mutSSProbability:
                offspring[i], = toolbox.mutSubtreeShrink(offspring[i])
                del offspring[i].fitness.values

        # mutation - node replacement
        for i in range(len(offspring)):
            if random.random() < self.params.mutNRProbability:
                offspring[i], = toolbox.mutNodeReplace(offspring[i])
                del offspring[i].fitness.values

        return offspring
