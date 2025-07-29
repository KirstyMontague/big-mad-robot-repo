
__all__ = ["qdSimple", "Kilobots"]

import time
import copy
import random
import os
import numpy
import pickle
import copy

from pathlib import Path
import numpy as np

from qdpy.phenotype import *
# from qdpy.containers import *

from containers import *

from deap import tools

from params import eaParams
from utilities import Utilities
from redundancy import Redundancy
from archive import Archive
from logs import Logs
import local



class EA():
	
	def __init__(self, params):
		self.params = params
		self.params.is_qdpy = True
		self.utilities = Utilities(params)
		self.utilities.setupToolbox(self.selTournament)
		self.utilities.saveConfigurationFile()
		self.redundancy = Redundancy()
		self.archive = Archive(params, self.redundancy)
		self.logs = Logs(params, self.utilities)

	def config(self, start_gen, container = None):
		self.toolbox = self.utilities.toolbox
		self.start_gen = start_gen
		self.current_iteration = start_gen
		self._init_container(container)
		self.total_elapsed = 0.
		random.seed(self.params.deapSeed)
		if self.params.saveOutput:
			Path(self.params.path()).mkdir(parents=False, exist_ok=True)
			Path(self.params.path()+"/csvs").mkdir(parents=False, exist_ok=True)

	def _init_container(self, container = None):
		if container == None:
			self.container = Container()
		else:
			self.container = container

	def save(self, outputFile):
		if self.params.saveOutput:
			results = {}
			results['current_iteration'] = self.current_iteration
			results['container'] = self.container
			results['random_state'] = random.getstate()
			results = {**results}
			with open(outputFile, "wb") as f:
				pickle.dump(results, f)

	def _iteration_callback(self, iteration, batch, container):
		self.current_iteration = iteration
		self.current_batch = batch
		if self.params.final_filename() != None and self.params.final_filename() != "":
			self.save(self.params.final_filename())
		if self.params.save_period == None or self.params.save_period == 0:
			return
		if iteration % self.params.save_period == 0 and self.params.iteration_filename() != None and self.params.iteration_filename() != "":
			self.save(self.params.iteration_filename() % iteration)			
			if self.params.saveHeatmap: self.utilities.saveHeatmap(self.container, self.current_iteration)
		if iteration % self.params.csv_save_period == 0:
			self.logs.saveCSV(iteration, self.utilities.getBestMax(container))
		time.sleep(self.params.genSleep)

		self.current_iteration = iteration + 1

	def run(self, init_batch = None, **kwargs):

		self.archive.getArchives(self.redundancy)

		if self.params.loadCheckpoint:
			from deap import base, creator, gp
			import pickle
			with open(self.params.input_filename(), "rb") as f:
				data = pickle.load(f)
			print ("")
			for i in data:
				if str(i) == "random_state":
					random.setstate(data[i])
			print ("")

		self.utilities.saveParams()

		start_time = round(time.time() * 1000)

		if init_batch == None:
			if not hasattr(self, "init_batch") or self.init_batch == None:
				init_batch = self.toolbox.population(n = self.params.populationSize)

		if len(init_batch) == 0:
			raise ValueError("``init_batch`` must not be empty.")

		self.evaluateNewPopulation(self.container, 0, init_batch, "w")

		max_gen = self.params.generations + 1
		generation = self.start_gen + 1
		
		while (generation < max_gen):
			self.params.configure()
			max_gen = self.params.generations + 1
			self.eaLoop(self.container, generation)
			generation += 1

		print("\nEnd the generational process\n")
		print ("\n\n")

		self.archive.saveArchive(self.redundancy)

		end_time = round(time.time() * 1000)

		self.utilities.saveDuration(start_time, end_time)

		time.sleep(self.params.eaRunSleep)

	def eaLoop(self, container, generation):

		batch = self.toolbox.select(container, self.params.populationSize)
		offspring = self.varAnd(batch, self.toolbox)

		self.evaluateNewPopulation(container, generation, offspring, "a")

		self._iteration_callback(generation, offspring, container)

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

		if self.params.saveCSV: # all seeds
			self.logs.logFitness(self.utilities.getBestMax(container))
			self.logs.logQdScore([self.utilities.getQDScore(container)])
			self.logs.logCoverage(self.utilities.getCoverage(container))

		if self.params.saveOutput: # one seed
			self.utilities.saveQDScore(container, generation, mode)
			self.utilities.saveCoverage(container, generation, mode)
			self.utilities.saveBestToCsv(container, generation, mode)

		if generation % self.params.best_save_period == 0:
			self.utilities.saveBestIndividuals(self.utilities.getBestMax(container, 25))


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
		
		if generation % 100 == 0 or invalid_new > 0: print (output_string)

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
