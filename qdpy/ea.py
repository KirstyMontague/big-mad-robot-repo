
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

from params import eaParams
from archive import Archive
from behaviours import Behaviours
from checkpoint import Checkpoint
from logs import Logs
from redundancy import Redundancy
from utilities import Utilities
import local



class EA():

    def __init__(self, params):

        self.params = params
        self.params.is_qdpy = True
        self.params.makePaths()

        random.seed(self.params.deapSeed)

        self.behaviours = Behaviours(params)

        self.utilities = Utilities(params, self.behaviours)

        tournament = self.selTournament
        if self.params.tournament == "agnosticTournament":
            tournament = self.agnosticTournament
        elif self.params.tournament == "multiFoodTournament":
            tournament = self.multiFoodTournament
        elif self.params.tournament == "multiFoodMaxTournament":
            tournament = self.multiFoodMaxTournament
        elif self.params.tournament == "multiFoodFloorTournament":
            tournament = self.multiFoodFloorTournament

        self.utilities.toolbox = self.utilities.setupToolboxGP(tournament)
        self.utilities.saveConfigurationFile()
        self.toolbox = self.utilities.toolbox

        self.redundancy = Redundancy(self.params)
        self.archive = Archive(params, self.redundancy)
        self.logs = Logs(params, self.utilities)
        self.checkpoint = Checkpoint(self.params)

    def run(self, init_batch = None, **kwargs):

        if self.params.cancelled:
            self.params.console("\naborted\n")
            return

        start_time = round(time.time() * 1000)
        self.utilities.saveParams()

        self.archive.getArchives(self.redundancy)

        if self.params.readCheckpoint:
            self.checkpoint.read()
            return

        elif self.params.loadCheckpoint:
            try:
                self.current_batch, containers = self.checkpoint.load(self.logs)
            except ValueError as error:
                self.utilities.printError(error.args)
                return
            self.container = containers[0]
            generation = self.params.start_gen

        else:
            if self.params.usingNewGrid:
                self.container = Grid(self.params.nb_bins, self.params.features_domain)
            else:
                self.container = Grid(shape = self.params.nb_bins,
                                      max_items_per_bin = self.params.max_items_per_bin,
                                      fitness_domain = self.params.fitness_domain,
                                      features_domain = self.params.features_domain,
                                      storage_type=list)

            self.current_batch = self.toolbox.population(n = self.params.populationSize)
            generation = 0

            try:
                self.evaluateNewPopulation(self.container, generation, self.current_batch, "w")
            except ValueError as error:
                self.utilities.printError(error.args)
                return

            self.params.runtime()

        try:
            self.eaLoop(self.container, generation)
        except ValueError as error:
            self.utilities.printError(error.args)
            return

        self.checkpoint.save(self.params.generations, self.current_batch, [self.container], self.logs)
        self.archive.saveArchive(self.redundancy, self.params.generations)
        self.utilities.saveBestIndividuals(self.utilities.getBestMax(self.container, 25), self.params.generations)

        self.params.deleteTempFiles()

        end_time = round(time.time() * 1000)
        self.utilities.saveDuration(start_time, end_time)

        time.sleep(self.params.eaRunSleep)

    def eaLoop(self, container, generation):

        max_gen = self.params.generations

        while (generation < max_gen):

            generation += 1

            population = list(container.values()) if self.params.usingNewGrid else container
            batch = self.toolbox.select(population, self.params.populationSize)
            offspring = self.varAnd(batch, self.toolbox)

            self.evaluateNewPopulation(container, generation, offspring, "a")

            self.current_batch = offspring

            self.checkpoint.save(generation, self.current_batch, [container], self.logs)
            self.logs.saveCSV(generation, container)
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
            output = "\nPrint all offspring\n\n"
            for ind in offspring:
                output += str("%.5f" % ind.fitness.values[0]) + "  \t"
                for f in ind.features:
                    output += str("%.5f" % f) + " \t"
                output += "\n"
            output += "---"
            self.params.console(output)
        
        # removing duplicates here because container throws away the individual that would have been replaced before throwing away the duplicate
        self.utilities.removeDuplicates(offspring, container)

        if self.params.usingNewGrid:
            container.update(offspring)
        else:
            try:
                container.update(offspring, issue_warning = self.params.show_warnings)
            except UserWarning as error:
                raise ValueError(error)
                return

        self.printOutput(generation, invalid_new, invalid_orig, matched)

        if (self.params.printContainer and generation == self.params.generations):
            self.utilities.printContainer(container)

        if (self.params.printExtrema and (generation % self.params.verbose_interval == 0 or generation == self.params.generations)):
            self.params.console(self.utilities.getExtrema(container))
            filename = self.params.path()+"/extrema.txt"
            with open(filename, "w") as f:
                f.write(self.utilities.getExtrema(container, True))

        if (self.params.printBestIndividuals and generation == self.params.generations):
            self.utilities.printBestMax(container)
            adjustedqdscore = self.utilities.getAdjustedQDScore(container)
            qdscore = self.utilities.getQDScore(container)
            coverage = self.utilities.getCoverage(container)
            qd_score_and_coverage = "QD Score: "+str("%.9f" % adjustedqdscore)+" (was "+str("%.9f" % qdscore)+")\n"
            qd_score_and_coverage += "Coverage: "+str("%.9f" % coverage)+"\n"
            self.params.console(qd_score_and_coverage)
            self.params.console(self.utilities.printRepertoireQdScores(container))

        if self.params.saveCSV or self.params.saveCheckpoint:
            self.logs.logFitness(generation, self.utilities.getBestMax(container))
            self.logs.logQdScore(generation, [self.utilities.getQDScore(container)])
            self.logs.logCoverage(generation, self.utilities.getCoverage(container))

        if generation != 0 and generation % 100 == 0 and invalid_new == 0:
            time.sleep(10.0)

        if invalid_new > 0:
            time.sleep(self.params.genSleep)

    def printOutput(self, generation, invalid_new, invalid_orig, matched):

        population = self.container.values() if self.params.usingNewGrid else self.container

        avg = 0
        for x in population:
            avg += len(x)
        avg = avg / len(population)
        avg_string = str("%.1f" % avg)

        best = self.utilities.getBestFromContainer(self.container, 0)
        best_fitness = str("%.6f" % best.fitness.values[0])

        if self.params.using_repertoire:
            best_length = str(len(best))+" ("+str(self.behaviours.unpack(best))+")"
        else:
            best_length = str(len(best))+" "

        if self.params.project in ["straight_to_foraging", "multi_food_foraging_with_subbehaviours"]:
            derated = best.fitness.values[0] * self.utilities.deratingFactorHeterogeneous(best)
        elif self.params.description == "foraging":
            derated = best.fitness.values[0] * self.utilities.deratingFactorForForaging(best)
        else:
            derated = best.fitness.values[0] * self.utilities.deratingFactor(best)
        fitness = str("%.6f" % derated)+" ("+best_fitness+")"
        
        coverage = str("%.6f" % self.utilities.getCoverage(self.container))
        filled = str(self.utilities.getFilledBins(self.container))
        total = str(self.params.nb_bins[0] * self.params.nb_bins[1] * self.params.nb_bins[2])

        qd_score = str("%.6f" % self.utilities.getAdjustedQDScore(self.container))

        if self.params.description == "foraging" and self.params.using_repertoire:
            description = self.params.repertoire_type+str(self.params.repertoire_size)+""
        else:
            description = self.params.description

        output_string = "\t"+description+" - "+str(self.params.deapSeed)+" - "+str(generation)+"\t | "
        output_string += avg_string+" | "
        output_string += fitness+" - "+best_length+" | "
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

    def agnosticTournament(self, individuals, k, tournsize, fit_attr="fitness"):

        chosen = []
        for i in range(k):
            objectives = random.sample([0,1,2,3,4,5], 1)
            aspirants = tools.selRandom(individuals, tournsize)
            feature = objectives[0]
            best = self.utilities.getExtremis(aspirants, feature)
            chosen.append(best)
        return chosen

    def multiFoodMaxTournament(self, individuals, k, tournsize, fit_attr="fitness"):

        chosen = []
        for i in range(k):
            aspirants = tools.selRandom(individuals, tournsize)
            best = self.utilities.getBestFromPopulation(aspirants, 0)
            chosen.append(best)
        return chosen

    def multiFoodTournament(self, individuals, k, tournsize, fit_attr="fitness"):

        chosen = []
        for i in range(k):
            objective = random.sample([3,4,5], 1)
            aspirants = tools.selRandom(individuals, tournsize)
            best = self.utilities.getExtremis(aspirants, objective[0])
            chosen.append(best)
        return chosen

    def multiFoodFloorTournament(self, individuals, k, tournsize, fit_attr="fitness"):

        chosen = []
        for i in range(k):
            aspirants = tools.selRandom(individuals, tournsize)
            best = self.utilities.getBestGeneralist(aspirants)
            chosen.append(best)
        return chosen

    def selTournament(self, individuals, k, tournsize, fit_attr="fitness"):

        chosen = []
        for i in range(k):
            aspirants = tools.selRandom(individuals, tournsize)
            best = self.utilities.getBestFromPopulation(aspirants, 0)
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
