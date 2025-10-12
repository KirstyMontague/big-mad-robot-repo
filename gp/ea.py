

import random
import time
import subprocess
import pickle
import sys
import os

import warnings
warnings.filterwarnings("error")

from deap import gp
from deap import tools
from deap import base
from deap import creator

from containers import *

from archive import Archive
from behaviours import Behaviours
from checkpoint import Checkpoint
from logs import Logs
from qd import QD
from redundancy import Redundancy
from utilities import Utilities

import local

class EA():

	def __init__(self, params):

		self.params = params
		self.params.is_qdpy = False

		self.behaviours = Behaviours(params)

		self.utilities = Utilities(params, self.behaviours)
		self.utilities.setupToolbox(self.selTournament)
		self.utilities.saveConfigurationFile()

		self.logs = Logs(self.params, self.utilities)
		self.redundancy = Redundancy(self.params.using_repertoire)
		self.archive = Archive(params, self.redundancy)
		self.checkpoint = Checkpoint(params)
		self.grid = QD(params, self.utilities)

	def selTournament(self, individuals, k, tournsize, fit_attr="fitness"):		
		chosen = []
		for i in range(k):
			aspirants = tools.selRandom(individuals, tournsize)
			feature = int(random.random() * self.params.features)
			# best = self.getBestHDRandom(aspirants, i % self.params.features)
			best = self.utilities.getBestHDRandom(aspirants, feature)
			chosen.append(best)
		return chosen

	def varAnd(self, population):
		
		# apply crossover and mutation
		
		offspring = [self.utilities.toolbox.clone(ind) for ind in population]
			
		# crossover
		for i in range(1, len(offspring), 2):
			if random.random() < self.params.crossoverProbability:
				offspring[i - 1], offspring[i] = self.utilities.toolbox.mate(offspring[i - 1],
																			 offspring[i])
				del offspring[i - 1].fitness.values, offspring[i].fitness.values

		# mutation - subtree replacement
		for i in range(len(offspring)):
			if random.random() < self.params.mutSRProbability:
				offspring[i], = self.utilities.toolbox.mutSubtreeReplace(offspring[i])
				del offspring[i].fitness.values

		# mutation - subtree shrink
		for i in range(len(offspring)):
			if random.random() < self.params.mutSSProbability:
				offspring[i], = self.utilities.toolbox.mutSubtreeShrink(offspring[i])
				del offspring[i].fitness.values

		# mutation - node replacement
		for i in range(len(offspring)):
			if random.random() < self.params.mutNRProbability:
				offspring[i], = self.utilities.toolbox.mutNodeReplace(offspring[i])
				del offspring[i].fitness.values

		return offspring

	def startWithNewPopulation(self):
		
		
		
		population = self.utilities.toolbox.population(n=self.params.populationSize)
	
		self.params.start_gen = 0	
		
		matched = self.evaluateNewPopulation(True, self.params.start_gen, population)
				
		self.printScores(population, self.params.printFitnessScores)
		self.printIndividuals(self.utilities.getBestAll(population), self.params.printBestIndividuals)
		self.printIndividuals(population, self.params.printAllIndividuals)
		
		# for ind in population:
			# self.printIndividual(ind)
		
		# Evaluate the individuals with an invalid fitness
		# invalid_ind = [ind for ind in population if not ind.fitness.valid]
		# invalid_orig = len(invalid_ind)			
		
		# matched = [0,0]
		# invalid_ind = self.assignDuplicateFitness(invalid_ind, matched)
		
		# invalid_ind = [ind for ind in population if not ind.fitness.valid]
		# invalid_new = len(invalid_ind)
		
		# self.evaluate(self.toolbox, invalid_ind)
		
		# redundancy
		# for ind in invalid_ind:
			# self.redundancy.addToLibrary(str(ind), ind.fitness.values)
		
		# print ("\t"+str(self.params.deapSeed)+" - "+str(self.params.start_gen)+" - invalid "+str(invalid_new)+" / "+str(invalid_orig)+" (matched "+str(matched[0])+" & "+str(matched[1])+")")
		
		# self.logFitness(self.getBestHDAll(population))
		
		return population

	def transferTrimmedFitnessScores(self, offspring, trimmed):
		for i in range(len(offspring)):
			offspring[i].fitness.values = trimmed[i].fitness.values

	def evaluateNewPopulation(self, starting, generation, population):
		
		invalid_ind = [ind for ind in population if not ind.fitness.valid]
		invalid_orig = len(invalid_ind)			
		
		matched = [0,0]
		invalid_ind = self.archive.assignDuplicateFitness(invalid_ind, self.assignFitness, matched)
		archive_ind = invalid_ind
		
		invalid_ind = [ind for ind in population if not ind.fitness.valid]
		invalid_new = len(invalid_ind)
		
		trimmed = self.utilities.getTrimmedPopulation(invalid_ind, self.redundancy)
		self.utilities.evaluate(self.assignPopulationFitness, trimmed)
		self.transferTrimmedFitnessScores(invalid_ind, trimmed)

		self.grid.addPopulation(population)

		for ind in archive_ind:
			self.archive.addToCompleteArchive(str(ind), ind.fitness.values)

		for ind in invalid_ind:
			self.archive.addToArchive(str(ind), ind.fitness.values)
		
		best = self.utilities.getBestAll(population, False)
		
		scores = ""
		for i in range(self.params.features):
			if self.params.description == "foraging":
				derated = best[i].fitness.values[i] * self.utilities.deratingFactorForForaging(best[i])
			else:
				derated = best[i].fitness.values[i] * self.utilities.deratingFactor(best[i])
			scores += str("%.7f" % derated) + " (" + str("%.7f" % best[i].fitness.values[i]) + ") \t"
		
		if self.params.using_repertoire:
			length = str(len(best[0]))+" ("+str(self.behaviours.unpack(best[0]))+")"
		else:
			length = str(len(best[0]))+" "
		
		if generation == self.params.generations or generation % 100 == 0 or invalid_new > 0:
			print ("\t"+str(self.params.deapSeed)+" - "+str(generation)+" - "+str(scores)+length+"\tinvalid "+str(invalid_new)+" / "+str(invalid_orig)+" (matched "+str(matched[0])+" & "+str(matched[1])+")")
		
		if generation != 0 and generation % 100 == 0 and invalid_new == 0:
			time.sleep(10.0)

		# print ("\t"+str(self.params.deapSeed)+" - "+str(generation)+" - "+str(scores)+str(len(best[0]))+"\tinvalid "+str(invalid_new)+" / "+str(invalid_orig)+" (matched "+str(matched[0])+" & "+str(matched[1])+")")

		self.logs.logFitness(generation, best)
		self.logs.logQdScore(generation, self.grid.getQDScores())
		self.logs.logCoverage(generation, self.utilities.getCoverage(self.grid.grids[0]))

		return matched

	def printIndividual(self, ind):
		performance = ""
		for fitness in ind.fitness.values:
			performance += str("%.9f" % fitness) + "  \t"
		print (performance)

	def printIndividuals(self, population, print_individuals):
		
		if print_individuals:
			print ("")
			for b in population:
				# print (b.fitness)
				print (self.utilities.formatChromosome(b))
				print ("")
			print ("")

	def printScores(self, population, print_scores):
		if print_scores:
			print ("")
			for ind in population:
				performance = ""
				for f in ind.fitness.values:
					performance += str("%.16f" % f) + " \t"
				print (performance)
				if self.params.printBestIndividuals:
					print (self.utilities.formatChromosome(ind))
			print ("")
					

	def eaInit(self, population, stats=None, halloffame=None, verbose=__debug__):

		start_time = round(time.time() * 1000)
		
		self.archive.getArchives(self.redundancy)
		
		invalid_orig = 0
		invalid_new = 0

		if self.params.readCheckpoint:
			population = self.checkpoint.read()
			return population

		elif self.params.loadCheckpoint:
			self.archive.setCompleteArchive(self.archive.getArchive())
			population = self.checkpoint.load(self.logs, self.grid)

		else:
			population = self.startWithNewPopulation()
		
		self.utilities.saveParams()
		
		# begin evolution
		self.eaLoop(population, stats)

		# get the best individual at the end of the evolutionary run
		best = self.utilities.getBestAll(population)
		self.printIndividuals(best, True)

		self.checkpoint.save(self.params.generations, population, self.grid.grids, self.logs)
		self.archive.saveArchive(self.redundancy)
		self.utilities.saveBestToFile(best[0])

		self.grid.save()

		end_time = round(time.time() * 1000)
		self.utilities.saveDuration(start_time, end_time)

		time.sleep(self.params.eaRunSleep)

		return population

	def eaLoop(self, population, stats=None, verbose=__debug__):

		max_gen = self.params.generations
		gen = self.params.start_gen

		while (gen < max_gen):

			gen += 1

			time.sleep(self.params.genSleep)
		
			elites = []
			for i in range(self.params.features):
				elite = self.utilities.getBestHDRandom(population, i)
				elites.append(elite)	
			
			offspring = self.utilities.toolbox.select(population, len(population)-self.params.features)
			offspring = self.varAnd(offspring)
			
			newPop = elites + offspring
			population[:] = newPop
			
			self.evaluateNewPopulation(False, gen, population)

			self.printScores(elites, self.params.printEliteScores)
			self.printScores(offspring, self.params.printFitnessScores)
			self.printIndividuals(self.utilities.getBestAll(population), self.params.printBestIndividuals)
			
			self.checkpoint.save(gen, population, self.grid.grids, self.logs)
			self.logs.saveCSV(gen, population)
			if gen % self.params.csv_save_period == 0: self.archive.saveArchive(self.redundancy)
			if gen % self.params.best_save_period == 0: self.utilities.saveBestIndividuals(population)

			self.params.configure()
			max_gen = self.params.generations

	def checkDuplicatesAreCorrect(self, population):
		
		# use self.params.pset instead
		pset = local.PrimitiveSetExtended("MAIN", 0)
		self.params.addNodes(pset)
		
		expected = population
		
		trimmed = []
		for ind in population:
			trimmed_string = self.redundancy.removeRedundancy(str(ind))
			trimmed_individual = [creator.Individual.from_string(trimmed_string, pset)][0]
			trimmed.append(trimmed_individual)
		
		actual = []
		actual_fitnesses = self.utilities.toolbox.map(self.utilities.toolbox.evaluate, trimmed)
		for ind, fit in zip(trimmed, actual_fitnesses):
			print(fit)
			ind.fitness.values = fit
			actual.append(ind)
		
		for i in range(len(population)):
			
			print(str(len(expected[i]))+" vs "+str(len(actual[i])))
			expected_fitness = expected[i].fitness.values
			actual_fitness = actual[i].fitness.values
			
			# fitness[3] doesn't need to match because trailing condition nodes affect conditionality in arbitrary ways
			if expected_fitness[0] != actual_fitness[0] or expected_fitness[1] != actual_fitness[1] or expected_fitness[2] != actual_fitness[2]:
				print ("ERROR")
				print (str(expected[i]))
				print ()
				print (str(actual[i]))
				print ()
				print (str(expected[i].fitness))
				print (str(actual[i].fitness))

	def assignFitness(self, offspring, fitness):
		offspring.fitness.values = fitness

	def assignPopulationFitness(self, population, fitnesses):
		for ind, fit in zip(population, fitnesses):
			ind.fitness.values = fit
