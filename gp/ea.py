

import random
import time
import subprocess
import pickle
import sys
import os

from deap import gp
from deap import tools
from deap import base
from deap import creator

from containers import *

from redundancy import Redundancy
from utilities import Utilities

import local

class EA():

	def subBehaviours(self):
		self.subBehaviourNodes = []
		for i in range(8):
			self.subBehaviourNodes.append("increaseDensity"+str(i+1))
			self.subBehaviourNodes.append("gotoNest"+str(i+1))
			self.subBehaviourNodes.append("gotoFood"+str(i+1))
			self.subBehaviourNodes.append("reduceDensity"+str(i+1))
			self.subBehaviourNodes.append("goAwayFromNest"+str(i+1))
			self.subBehaviourNodes.append("goAwayFromFood"+str(i+1))

	subBehaviourSizes = {}
	
	output = ""
	
	def setParams(self, params):
		self.params = params
		self.params.is_qdpy = False
		self.utilities = Utilities(params)
		self.utilities.setupToolbox(self.selTournament)
		
		self.redundancy = Redundancy()
		self.subBehaviours()
		self.loadSubBehaviours()
		# self.setUpGrid()

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

	def saveDuration(self, duration, minutes_str):
		
		if self.params.saveOutput:
			with open(self.params.path()+"params.txt", 'a') as f:
				f.write("duration: "+str(duration)+" ("+minutes_str+") minutes\n")

	def readCheckpoint(self):
	
		with open(self.params.checkpointInputFilename(self.params.start_gen), "rb") as checkpoint_file:
			checkpoint = pickle.load(checkpoint_file)
		population = checkpoint["population"]
		
		output = ""
		for i in range(len(population)):
			if True or population[i].fitness.values[5] > 0.7:
				output += "\n"
				output += str(population[i])
				output += "\n"
				for f in population[i].fitness.values:
					output += str("%.9f" % f) + " \t"
				output += "\n"
			# output += "\n\n\n\n"
			# print (output)
		
		print("population size")
		print(len(population))
		
		self.printIndividuals(self.utilities.getBestAll(population), True)
		
		# print(output)
		return population
		
		self.params.features = 1
		for i in range(len(population)):
			self.utilities.evaluateRobot(population[i], 5)
		return population

	def loadCheckpoint(self):
			
		with open(self.params.checkpointInputFilename(self.params.start_gen), "rb") as checkpoint_file:
			checkpoint = pickle.load(checkpoint_file)
		population = checkpoint["population"]
		random.setstate(checkpoint["rndstate"])
		csvFilename = self.params.csvInputFilename(self.params.start_gen)
		
		f = open(csvFilename, "r")
		output = ""
		for line in f:
			items = line.split(",")
			if len(items) > 1 and items[2] != "Seed":
				# print (items[0]+" | "+items[2]+" | "+items[4]+" | "+items[5])
				# print (self.params.description+" | "+str(self.params.deapSeed)+" | "+str(self.params.populationSize)+" | "+str(self.params.tournamentSize))
				if items[0] == self.params.description and \
					int(items[2]) == self.params.deapSeed and \
					int(items[4]) == self.params.populationSize and \
					int(items[5]) == self.params.tournamentSize:
						output = ""
						for i in range(9,self.params.start_gen+10):
							# print(items[i]+",")
							output += items[i]+","
							
		self.output += output
		
		for ind in population:
			self.printIndividual(ind)
		
		return population
	
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
	
	def saveCheckpoint(self, generation, population):
		
		if self.params.saveOutput and (generation % self.params.save_period == 0 or generation == self.params.generations):
			
			# qdpy_population = []
			# for ind in population:
				# qdpy_individual = dict(genome=str(ind), fitness=ind.fitness.values)
				# qdpy_population.append(qdpy_individual)
			checkpoint = dict(population=population, generation=self.params.generations, rndstate=random.getstate())
			
			with open(self.params.checkpointOutputFilename(generation), "wb") as checkpoint_file:
				 pickle.dump(checkpoint, checkpoint_file)
	
	def saveCSV(self, generation, population):
		
		if self.params.saveCSV and generation % self.params.csv_save_period == 0:
			logHeaders = "Type,Time,Seed,Robots,Pop,Tourn,Iterations,Params,,"
			for i in range(generation + 1):
				logHeaders += str(i)+","
			logHeaders += ",Chromosome,Nodes,"
			
			# get the best individual at the end of the evolutionary run
			allBest = []
			for i in range(self.params.features):
				bestThisPop = self.utilities.getBestHDRandom(population, i)
				allBest.append(bestThisPop)		
				performance = ""
				for f in bestThisPop.fitness.values:
					performance += str("%.5f" % f) + " \t"

			chromosomes = ",\""
			for bestThisPop in allBest:
				chromosomes += ""+str(bestThisPop)+" + "
			chromosomes = chromosomes[0:-3]
			chromosomes += "\",,"
			
			nodes = ""
			for node in self.params.nodes:
				if node: nodes += node+" "
	
			filename = self.params.csvOutputFilename(generation)
			with open(filename, 'a') as f:
				f.write(logHeaders)
				f.write("\n")
				f.write(self.output)
				f.write(chromosomes)
				f.write(nodes)

	def evaluateNewPopulation(self, starting, generation, population):
		
		invalid_ind = [ind for ind in population if not ind.fitness.valid]
		invalid_orig = len(invalid_ind)			
		
		matched = [0,0]
		invalid_ind = self.utilities.assignDuplicateFitness(self.redundancy, invalid_ind, self.assignFitness, matched)
		
		invalid_ind = [ind for ind in population if not ind.fitness.valid]
		invalid_new = len(invalid_ind)
		
		self.utilities.evaluate(self.assignPopulationFitness, invalid_ind)
		
		if generation > 0 and generation % self.params.save_period == 0:
			self.checkDuplicatesAreCorrect(invalid_ind)

		# self.convertDEAPtoGrid(population)
		
		for ind in invalid_ind:
			self.redundancy.addToLibrary(str(ind), ind.fitness.values)
		
		best = self.utilities.getBestAll(population)
		# self.printIndividuals(best, True)
		
		scores = ""
		for i in range(self.params.features):
			derated = best[i].fitness.values[i] * self.utilities.deratingFactor(best[i])
			# derated = best[i].fitness.values[i] * self.deratingFactorForForaging(best[i])
			scores += str("%.7f" % derated) + " (" + str("%.7f" % best[i].fitness.values[i]) + ") \t"
		
		length = str(len(best[0]))+" ("+str(self.unpackSubBehaviours(best[0]))+")"
		print ("\t"+str(self.params.deapSeed)+" - "+str(generation)+" - "+str(scores)+length+"\tinvalid "+str(invalid_new)+" / "+str(invalid_orig)+" (matched "+str(matched[0])+" & "+str(matched[1])+")")
		
		# print ("\t"+str(self.params.deapSeed)+" - "+str(generation)+" - "+str(scores)+str(len(best[0]))+"\tinvalid "+str(invalid_new)+" / "+str(invalid_orig)+" (matched "+str(matched[0])+" & "+str(matched[1])+")")

		self.logFitness(best)
			
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
		
		self.utilities.getArchives(self.redundancy)
		
		invalid_orig = 0
		invalid_new = 0

		self.logFirst()
		
		if self.params.readCheckpoint:
			population = self.readCheckpoint()
			return population

		elif self.params.loadCheckpoint:			
			population = self.loadCheckpoint()
			
		else:	
			population = self.startWithNewPopulation()
		
		self.utilities.saveParams()
		
		# begin evolution
		self.eaLoop(population, self.params.start_gen, self.params.generations, stats)

		# get the best individual at the end of the evolutionary run
		best = self.utilities.getBestAll(population)
		self.printIndividuals(best, True)
		
		# log chromosome and test performance in different environments
		self.logChromosomes(best)
		self.logNodes()
		
		self.saveCheckpoint(self.params.generations, population)
		self.utilities.saveArchive(self.redundancy)
		
		end_time = round(time.time() * 1000)
		duration = end_time - start_time
		minutes = (duration / 1000) / 60
		minutes_str = str("%.2f" % minutes)		
		print("duration " +minutes_str)
		
		# self.printGrid()

		self.saveDuration(duration, minutes_str)
		
		return population

	def eaLoop(self, population, start_gen, ngen, stats=None, verbose=__debug__):

		max_gen = ngen
		gen = start_gen
		
		# for gen in range(start_gen + 1, max_gen + 1):
		while (gen < max_gen):
			
			gen += 1
		
			self.params.configure()
			max_gen = self.params.generations

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
			
			

			# best = self.getBestHDAll(population)
			# self.logFitness(best)
			
			self.printScores(elites, self.params.printEliteScores)
			self.printScores(offspring, self.params.printFitnessScores)
			self.printIndividuals(self.utilities.getBestAll(population), self.params.printBestIndividuals)
			
			self.saveCheckpoint(gen, population)
			self.saveCSV(gen, population)
			if gen % self.params.csv_save_period == 0: self.utilities.saveArchive(self.redundancy)
			if gen % self.params.best_save_period == 0: self.utilities.saveBestIndividuals(population)


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

	def unpackSubBehaviours(self, individual):
		
		packed_size = len(individual)
		unpacked_size = len(individual)
		
		for node in individual:
			for sub_behaviour in self.subBehaviourNodes:
				if node.name == sub_behaviour:
					unpacked_size -= 1
					unpacked_size += self.subBehaviourSizes[sub_behaviour]
		
		return unpacked_size
	
	def loadSubBehaviours(self):
	
		pset = local.PrimitiveSetExtended("MAIN", 0)
		self.params.addUnpackedNodes(pset)

		f = open("../txt/sub-behaviours.txt", "r")
		
		for line in f:
			name = line[0:line.find(" ")]
			chromosome = line[line.find(" ")+1:]
			individual = [creator.Individual.from_string(chromosome, pset)]
			sub_behaviour_size = len(individual[0])
			self.subBehaviourSizes[name] = sub_behaviour_size

	def deratingFactorForForaging(self, individual):
		
		length = float(self.unpackSubBehaviours(individual))
		
		usage = length - 100 if length > 100 else 0
		usage = usage / 9900 if length <= 10000 else 1
		usage = 1 - usage
		
		return usage

	def logFirst(self):
		
		# save parameters to the output
		
		self.output = self.params.description+","
		self.output += str(time.time())[0:10]+","
		self.output += str(self.params.deapSeed)+","
		self.output += str(self.params.sqrtRobots)+","
		self.output += str(self.params.populationSize)+","
		self.output += str(self.params.tournamentSize)+","
		
		self.output += str(self.params.iterations)+","

		for param in self.params.arenaParams:
			self.output += str(param)+" "
		self.output += ","
		
		# self.output += str(self.params.unseenIterations)+", "

		# for param in self.params.unseenParams:
			# self.output += str(param)+" "
		# self.output += ","
		
		# self.output += "\""
		# for node in sorted(self.params.nodes):
			# if (self.params.nodes[node]):
				# self.output += node+", "
		# self.output += "\","
		
		self.output += ","

	def logFitness(self, best):
		for i in range(self.params.features):
			self.output += str("%.6f" % best[i].fitness.values[i])+" "
		self.output += ","

	def logChromosomes(self, allBest):
		chromosomes = ",\""
		for best in allBest:
			chromosomes += ""+str(best)+" + "
		chromosomes = chromosomes[0:-3]
		chromosomes += "\","
		self.output += chromosomes

	def logNodes(self):
		for node in self.params.nodes:
			if node: self.output += node+" "
		self.output += ","

	def setUpGrid(self):

		def genEmpty():
			return []

		self.grids = []

		toolbox = base.Toolbox()

		pset = local.PrimitiveSetExtended("MAIN", 0)
		self.params.addNodes(pset)

		creator.create("Single_Objective_Fitness", base.Fitness, weights=(1.0,))
		creator.create("Single_Objective_Individual", gp.PrimitiveTree, fitness=creator.Single_Objective_Fitness, features=list)
		toolbox.register("expr_init", genEmpty)
		toolbox.register("Single_Objective_Individual", tools.initIterate, creator.Individual, toolbox.expr_init)
		toolbox.register("Single_Objective_Population", tools.initRepeat, list, toolbox.Single_Objective_Individual)

		self.qdpy_toolbox = toolbox

		self.grids = []

		for objective in self.params.indexes:

			fitness_domain = [(0.,1.0),]

			self.grids.append(Grid(shape = [8,8,8],
							  max_items_per_bin = 1,
							  fitness_domain = fitness_domain,
							  features_domain = [(-40.0, 40.0), (-40.0, 40.0), (0.0, 1.0)],
							  storage_type=list))

	def convertDEAPtoGrid(self, population):

		for i in range(self.params.features):

			pop = self.qdpy_toolbox.Single_Objective_Population(n=len(population))

			for j in range(len(population)):

				pop[j] = creator.Single_Objective_Individual(population[j])

				fitness = [population[j].fitness.values[i]]

				features = []
				features.append(population[j].fitness.values[-3])
				features.append(population[j].fitness.values[-2])
				features.append(population[j].fitness.values[-1])

				pop[j].fitness.values = tuple(fitness)
				# print(pop[j].fitness.values)
				pop[j].features = tuple(features)

			grid = self.grids[i]
			self.utilities.removeDuplicates(pop, grid)
			nb_updated = grid.update(pop, issue_warning = True)


	def printGrid(self):

		for i in range(len(self.grids)):

			grid = self.grids[i]

			filename = "./test/"+self.params.description+"/"+str(self.params.deapSeed)+"/"
			filename += self.params.objectives[self.params.indexes[i]]+".pkl"
			print(filename)

			with open(filename, "wb") as f:
				pickle.dump(grid, f)
