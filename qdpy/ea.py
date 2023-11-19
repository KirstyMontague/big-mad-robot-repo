
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
from timeit import default_timer as timer

from qdpy.phenotype import *
# from qdpy.containers import *

from containers import *

from deap import tools

from params import eaParams
from utilities import Utilities
from redundancy import Redundancy
import local



class EA():
	
	def __init__(self, params):
		self.params = params
		self.params.is_qdpy = True
		self.utilities = Utilities(params)
		self.utilities.setupToolbox(self.selTournament)
		self.redundancy = Redundancy()

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

	def gen_init_batch(self):
		self.init_batch = self.toolbox.population(n = self.params.populationSize)

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
		time.sleep(self.params.genSleep)

		self.current_iteration = iteration + 1

	def saveDuration(self):
		self.total_elapsed = timer() - self.start_time
		
		minutes = self.total_elapsed / 60
		minutes_str = str("%.2f" % minutes)
		print("Duration " +minutes_str+"\n")

		if self.params.saveOutput:
			with open(self.params.path()+"params.txt", 'a') as f:
				f.write("generations: "+str(self.params.generations) + "\n")
				f.write("duration: "+str(self.total_elapsed) + "\n")

	def run(self, init_batch = None, **kwargs):
		
		self.utilities.getArchives(self.redundancy)
		
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

		if not hasattr(self, "start_time") or self.start_time == None:
			self.start_time = timer()
			
		if init_batch == None:
			if not hasattr(self, "init_batch") or self.init_batch == None:
				self.gen_init_batch()
		else:
			self.init_batch = init_batch
		
		# ======
		batch = self.qdSimple(self.init_batch, self.toolbox, self.container, iteration_callback = self._iteration_callback)
		# ======
		
		self.utilities.saveArchive(self.redundancy)
		self.saveDuration()
		
		
		return self.total_elapsed


	def qdSimple(self, init_batch, toolbox, container, stats = None, halloffame = None, start_time = None, iteration_callback = None):

		if start_time == None:
			start_time = timer()

		if len(init_batch) == 0:
			raise ValueError("``init_batch`` must not be empty.")

		invalid_ind = [ind for ind in init_batch if not ind.fitness.valid]
		invalid_orig = len(invalid_ind)	
		
		matched = [0,0]
		invalid_ind = self.utilities.assignDuplicateFitness(self.redundancy, invalid_ind, self.assignFitness, matched)
		
		invalid_ind = [ind for ind in init_batch if not ind.fitness.valid]
		invalid_new = len(invalid_ind)

		self.utilities.evaluate(self.assignPopulationFitness, invalid_ind)

		for ind in invalid_ind:
			self.addToArchive(str(ind), ind.fitness.values, ind.features)
				
		if halloffame is not None:
			halloffame.update(init_batch)

		print ("\nupdating\n")
		nb_updated = 0
		if not self.params.loadCheckpoint:
			nb_updated = container.update(init_batch, issue_warning = self.params.show_warnings)
			if nb_updated == 0:
				raise ValueError("No individual could be added to the container !")
		
		# print ("\nPrint all individuals in container\n")
		# self.utilities.printContainer(container)
		
		batch = init_batch

		self.printOutput(self.start_gen, invalid_new, invalid_orig, matched)
		
		if self.params.saveOutput:
			if not self.params.fitness_grid: self.utilities.saveQDScore(container, 0, "w")
			self.utilities.saveCoverage(container, 0, "w")
			if not self.params.fitness_grid: self.utilities.saveBestIndividuals(container, 0, "w")
			# else: self.utilities.saveExtrema(container, i)
		
		
		max_gen = self.params.generations + 1
		i = self.start_gen + 1
		
		# for i in range(self.start_gen + 1, self.params.generations + 1):
		while (i < max_gen):			
			self.params.configure()
			max_gen = self.params.generations + 1
			self.eaLoop(toolbox, container, i, iteration_callback)
			i += 1

		print("\nEnd the generational process\n")
		print ("\n\n")
		# for x in self.container:
			# print(x)
			# print("\n")
		# print ("\n\n")
	
		return batch

	def eaLoop(self, toolbox, container, i, iteration_callback):

		batch = toolbox.select(container, self.params.populationSize)
		offspring = self.varAnd(batch, toolbox)
		
		invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
		invalid_orig = len(invalid_ind)			
		
		matched = [0,0]
		invalid_ind = self.utilities.assignDuplicateFitness(self.redundancy, invalid_ind, self.assignFitness, matched)
			
		invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
		invalid_new = len(invalid_ind)
		
		# print ("\t"+str(self.params.deapSeed)+" - "+str(i)+" | invalid "+str(invalid_new)+" / "+str(invalid_orig)+" (matched "+str(matched[0])+" & "+str(matched[1])+")")

		self.utilities.evaluate(self.assignPopulationFitness, invalid_ind)

		for ind in invalid_ind:
			self.addToArchive(str(ind), ind.fitness.values, ind.features)
			
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
		# print ("number updated, rejected, discarded " + str(nb_updated) + ", "+str(container.nb_rejected) + ", " + str(container.nb_discarded))
		# print ("== " + str(self.params.deapSeed) + " == generation " + str(i) + " / "+ str(self.params.generations) +" ==========================================================")
		
		self.printOutput(i, invalid_new, invalid_orig, matched)
		
		if (self.params.printContainer):
			print ("\nPrint all individuals in container\n")
			self.utilities.printContainer(container)

		if (self.params.printBestIndividuals):
			# print ("\nPrint best individuals\n")
			if self.params.fitness_grid:
				self.utilities.printExtrema(container)
			else:
				self.utilities.printBestMax(container)
				qdscore = self.utilities.getQDScore(container)
				coverage = self.utilities.getCoverage(container)
				print("QD Score: "+str("%.9f" % qdscore))
				print("Coverage: "+str("%.9f" % coverage))
				print("")
		
		if self.params.saveOutput:
			if not self.params.fitness_grid: self.utilities.saveQDScore(container, i)
			self.utilities.saveCoverage(container, i)
			if not self.params.fitness_grid: self.utilities.saveBestIndividuals(container, i)
			else: self.utilities.saveExtrema(container, i)

		if i % self.params.best_save_period == 0: self.saveBestIndividuals(container)

		if iteration_callback != None:
			iteration_callback(i, offspring, container)

	def printOutput(self, generation, invalid_new, invalid_orig, matched):
		
		avg = 0
		for x in self.container:
			avg += len(x)
		avg = avg / len(self.container)
		avg_string = str("%.1f" % avg)
		
		# no repro after this change because using RNG
		best = self.utilities.getBestHDRandom(self.container, random.randint(0, self.params.features - 1))
		best_length = str(len(best))
		best_fitness = str("%.6f" % best.fitness.values[0])
		derated = best.fitness.values[0] * self.utilities.deratingFactor(best)
		fitness = str("%.6f" % derated)+" ("+best_fitness+")"
		
		output_string = "\t"+str(self.params.deapSeed)+" - "+str(generation)+"\t| "
		output_string += avg_string+" | "+fitness+" - "+best_length
		output_string += "\t| invalid "+str(invalid_new)+" / "+str(invalid_orig)
		output_string += " (matched "+str(matched[0])+" & "+str(matched[1])+")"
		
		print (output_string)

	def saveBestIndividuals(self, container):

		if self.params.saveBestIndividuals:

			with open('../txt/current.txt', 'w') as f:
				f.write("\n")

			best = self.utilities.getBestMax(container, 10)

			for b in best:

				with open('../txt/current.txt', 'a') as f:
					f.write("\n")
					f.write(str(b.fitness.values[0]))
					f.write("\n\n")
					f.write(self.utilities.formatChromosome(b))
					f.write("\n============================================\n")

	def addToArchive(self, chromosome, fitness, features):
		
		new_chromosome = self.redundancy.trim(chromosome)
		
		if new_chromosome in self.redundancy.archive:
			expected = self.redundancy.archive[new_chromosome]
			if expected[0] != fitness[0] or expected[1] != features[0] or expected[2] != features[1]:
				print ("\nWRONG FITNESS\n")
				print (chromosome)
				print (new_chromosome)
				print (self.archive[new_chromosome])
				print (fitness)
				print (features)
		
		scores_list = [fitness[0]] + features
		scores = tuple(scores_list)
		self.redundancy.archive.update({new_chromosome : scores})	

	def assignFitness(self, offspring, fitness):
		offspring.fitness.values = (fitness[0],)
		offspring.features = [fitness[1], fitness[2], fitness[3]]

	def assignPopulationFitness(self, population, fitnesses):
		for ind, fit in zip(population, fitnesses):
			ind.fitness.values = fit[0]
			ind.features = fit[1]

	def selTournament(self, individuals, k, tournsize, fit_attr="fitness"):		
		
		# if self.params.fitness_grid:
			# return tools.selRandom(individuals, k)
		
		chosen = []
		for i in range(k):
			aspirants = tools.selRandom(individuals, tournsize)
			if self.params.fitness_grid:
				feature = random.randint(0, self.params.characteristics - 1)
				best = self.getExtremis(aspirants, feature)
				# feature = random.randint(0, self.params.features - 1)
				# best = self.getBestHDRandomMin(aspirants, 0)
				# best = aspirants[0]
			else:
				feature = int(random.random() * self.params.features)
				# best = self.getBestHDRandom(aspirants, i % self.params.features)
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

	def getExtremis(self, population, feature = -1):
		
		if (feature == -1):
			feature = random.randint(0, self.params.characteristics - 1)
		invert = True if random.randint(0, 1) < 0.5 else False
		
		# print ("\n\nfeature "+str(feature))
		# self.utilities.printIndividuals(population)
			
		# get the best member of the population
		
		for individual in population:		
			
			thisFitness = individual.features[feature]
			# if thisFitness < .5:
			if invert:
				thisFitness = 1.0 - thisFitness
			# print (thisFitness)
			
			currentBest = False
			
			if ('best' not in locals()):
				currentBest = True
			
			elif (thisFitness > bestFitness):
				currentBest = True
			
			elif (thisFitness == bestFitness and bestHeight > 3 and individual.height < bestHeight):
				currentBest = True
				
			if (currentBest):
				best = individual
				bestFitness = thisFitness	
				bestHeight = individual.height
		
		# print (best.features[feature])
		# print("\n\n")
		return best



