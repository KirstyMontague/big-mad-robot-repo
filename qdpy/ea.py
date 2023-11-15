
__all__ = ["qdSimple", "Kilobots"]

import time
import copy
import random
import os
import threading

import numpy

from functools import partial

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

# ====================

# import os
import deap.tools
import deap.algorithms
import numpy as np
from timeit import default_timer as timer
import pickle
import copy

from qdpy.phenotype import *
# from qdpy.containers import *

# QD2
from containers import *
# from extended_containers import *

from redundancy import Redundancy



# ====================

from pathlib import Path

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

from qdpy.plots import *

import scipy

# ====================

from params import eaParams
from utilities import Utilities


def qdSimple(init_batch, toolbox, container, batch_size, niter, cxpb = 0.0, mutpb = 1.0, stats = None, halloffame = None, verbose = False, show_warnings = False, start_time = None, iteration_callback = None):

    print ("================================================= qdsimple ================================================= ")


class EA():
	
	def __init__(self, params):
		self.params = params
		# random.seed(self.params.deapSeed)
		self.utilities = Utilities(params)
		self.redundancy = Redundancy()
		# Path(self.params.path()).mkdir(parents=False, exist_ok=True)
		# Path(self.params.path()+"/csvs").mkdir(parents=False, exist_ok=True)
		
	def config(self, toolbox, start_gen, container = None, stats = None, halloffame = None,
					ea_fn = qdSimple, results_infos = None,					
					iteration_callback_fn = None, **kwargs):
		self._update_params(**kwargs)
		self.toolbox = toolbox
		self.halloffame = halloffame
		self.ea_fn = ea_fn
		self.iteration_callback_fn = iteration_callback_fn
		self.start_gen = start_gen
		self.current_iteration = start_gen
		self._init_container(container)
		self._init_stats(stats)
		self._results_infos = {}
		if results_infos != None:
			self.add_results_infos(results_infos)
		self.total_elapsed = 0.
		random.seed(self.params.deapSeed)
		if self.params.saveOutput:
			Path(self.params.path()).mkdir(parents=False, exist_ok=True)
			Path(self.params.path()+"/csvs").mkdir(parents=False, exist_ok=True)
	
	def setParams(self, params):
		self.params = params

	def _init_container(self, container = None):
		if container == None:
			self.container = Container()
		else:
			self.container = container
			

	def _init_stats(self, stats = None):
		if stats == None:
			# Default stats
			self.stats = deap.tools.Statistics(lambda ind: ind.fitness.values)
			self.stats.register("avg", np.mean, axis=0)
			self.stats.register("std", np.std, axis=0)
			self.stats.register("min", np.min, axis=0)
			self.stats.register("max", np.max, axis=0)
		else:
			self.stats = stats

	def gen_init_batch(self):
		self.init_batch = self.toolbox.population(n = self.params.init_batch_size)

	def save(self, outputFile):
		if (self.params.saveOutput):
			results = {}
			results['current_iteration'] = self.current_iteration
			results['container'] = self.container
			results['random_state'] = random.getstate()
			results = {**results, **self._results_infos}
			
			# print("\n saving container \n")
			# print(self.current_iteration)
			# print("")
			# print(self.utilities.printContainer(self.container))
			
			# for ind in self.container:
				# performance = str("%.5f" % ind.fitness.values[0]) + "  \t"
				# for f in ind.features:
					# performance += str("%.5f" % f) + " \t"
				# print (performance)
			
			with open(outputFile, "wb") as f:
				pickle.dump(results, f)

	def _update_params(self, **kwargs):
		for k,v in kwargs.items():
			if v != None:
				if k == "start_time":
					setattr(self, k, v)

	def add_results_infos(self, *args):
		if len(args) == 1:
			self._results_infos = {**self._results_infos, **args[0]}
		elif len(args) == 2:
			self._results_infos[args[0]] = args[1]
		else:
			raise ValueError("Please either pass a dictionary or key, value as parameter.")

	def _iteration_callback(self, iteration, batch, container):
		self.current_iteration = iteration
		self.current_batch = batch
		if self.params.final_filename() != None and self.params.final_filename() != "":
			self.save(self.params.final_filename())
		if self.iteration_callback_fn is not None:
			self.iteration_callback_fn(iteration, batch, container)
		if self.params.save_period == None or self.params.save_period == 0:
			return
		if iteration % self.params.save_period == 0 and self.params.iteration_filename() != None and self.params.iteration_filename() != "":
			self.save(self.params.iteration_filename() % iteration)			
			# Create plots
			# plot_path = self.params.path+"performance"+str(self.params.deapSeed)+"-iteration"+str(iteration)+".pdf"
			# plotGridSubplots(self.container.quality_array[... ,0], plot_path, plt.get_cmap("nipy_spectral"), self.container.features_domain, self.container.fitness_extrema[0], nbTicks=None)
			if self.params.saveHeatmap: self.utilities.saveHeatmap(self.container, self.current_iteration)
			# print("\nA plot of the performance grid was saved in '%s'." % os.path.abspath(plot_path))
			time.sleep(self.params.genSleep)

		self.current_iteration = iteration + 1

	def saveParams(self):
		
		if self.params.saveOutput:
			with open(self.params.path()+"params.txt", 'a') as f:
				f.write("\n")
				f.write("time: "+str(time.ctime()) + "\n")
				f.write("deapSeed: "+str(self.params.deapSeed) + "\n")
				f.write("tournamentSize: "+str(self.params.tournamentSize) + "\n")
				f.write("features: "+str(self.params.features) + "\n")
				f.write("characteristics: "+str(self.params.characteristics) + "\n")
				f.write("objective: "+str(self.params.description) + "\n")
				f.write("objective_index: "+str(self.params.indexes[0]) + "\n")
				f.write("loadCheckpoint: "+("yes" if self.params.loadCheckpoint else "no") + "\n")
				f.write("start_point: "+str(self.params.start_point) + "\n")
				f.write("init_batch_size: "+str(self.params.init_batch_size) + "\n")
				f.write("batch_size: "+str(self.params.batch_size) + "\n")
				f.write("max_items_per_bin: "+str(self.params.max_items_per_bin) + "\n")
				f.write("nb_bins: "+str(self.params.nb_bins[0])+", "+str(self.params.nb_bins[1])+", "+str(self.params.nb_bins[2])+"\n")
				f.write("features_domain: "+str(self.params.features_domain[0])+", "+str(self.params.features_domain[1])+", "+str(self.params.features_domain[2])+"\n")
				f.write("arenaParams: "+str(self.params.arenaParams[0])+", "+str(self.params.arenaParams[1])+"\n")

	def saveDuration(self):
		self.total_elapsed = timer() - self.start_time
		
		minutes = self.total_elapsed / 60
		minutes_str = str("%.2f" % minutes)
		print("Duration " +minutes_str+"\n")

		if self.params.saveOutput:
			with open(self.params.path()+"params.txt", 'a') as f:
				f.write("generations: "+str(self.params.generations) + "\n")
				f.write("duration: "+str(self.total_elapsed) + "\n")
	
	def collectArchive(self):
	
		archive = self.redundancy.getArchive()
		cumulative_archive = self.redundancy.getCumulativeArchive()
		
		for i in range(10):
			archive_path = "../gp/test/"+self.params.description+"/"+str(i+1)+"/archive.pkl"
			if os.path.exists(archive_path):
				print("reading from "+archive_path)
				with open(archive_path, "rb") as archive_file:
					cumulative_archive.update(pickle.load(archive_file))
		
		for i in range(10):
			archive_path = "../qdpy/test/"+self.params.description+"/"+str(i+1)+"/archive.pkl"
			if i + 1 != self.params.deapSeed and os.path.exists(archive_path):
				print("reading from "+archive_path)
				with open(archive_path, "rb") as archive_file:
					cumulative_archive.update(pickle.load(archive_file))
		
		if os.path.exists(self.params.path()+"archive.pkl"):
			with open(self.params.path()+"archive.pkl", "rb") as archive_file:
				archive = pickle.load(archive_file)
		
		self.redundancy.setArchive(archive)
		self.redundancy.setCumulativeArchive(cumulative_archive)
		
		print("archive length "+str(len(archive)))
		print("cumulative archive length "+str(len(cumulative_archive)))
	
	def saveArchive(self):
		
		if self.params.saveOutput:
			
			archive = self.redundancy.getArchive()
			archive_dict = {}
			archive_string = ""
			for chromosome, scores in archive.items():
				archive_dict.update({str(chromosome) : scores})
				archive_string += str(chromosome)+"+"
				for f in scores:
					archive_string += str(f)+","
				archive_string = archive_string[0:-1]
				archive_string += "\n"
				
			# with open(self.params.path()+"archive.txt", 'w') as f:
				# f.write(archive_string)
				
			with open(self.params.path()+"archive.pkl", "wb") as archive_file:
				 pickle.dump(archive_dict, archive_file)

	def run(self, init_batch = None, **kwargs):
		
		self.collectArchive()
		
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

		self.saveParams()

		self._update_params(**kwargs)
		
		if not hasattr(self, "start_time") or self.start_time == None:
			self.start_time = timer()
			
		if init_batch == None:
			if not hasattr(self, "init_batch") or self.init_batch == None:
				self.gen_init_batch()
		else:
			self.init_batch = init_batch
		
		# ======
		batch, logbook = self.qdSimple(self.init_batch, self.toolbox, self.container, iteration_callback = self._iteration_callback)
		# ======
		
		self.saveArchive()
		self.saveDuration()
		
		
		return self.total_elapsed


	def qdSimple(self, init_batch, toolbox, container, stats = None, halloffame = None, start_time = None, iteration_callback = None):

		if start_time == None:
			start_time = timer()
		logbook = deap.tools.Logbook()
		logbook.header = ["iteration", "containerSize", "evals", "nbUpdated"] + (stats.fields if stats else []) + ["elapsed"]

		if len(init_batch) == 0:
			raise ValueError("``init_batch`` must not be empty.")

		invalid_ind = [ind for ind in init_batch if not ind.fitness.valid]
		invalid_orig = len(invalid_ind)	
		
		matched = [0,0]
		invalid_ind = self.assignDuplicateFitness(container.items, invalid_ind, matched)
		
		invalid_ind = [ind for ind in init_batch if not ind.fitness.valid]
		invalid_new = len(invalid_ind)
			
		self.evaluate(toolbox, invalid_ind)

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
	
		return batch, logbook

	def eaLoop(self, toolbox, container, i, iteration_callback):

		batch = toolbox.select(container, self.params.batch_size)
		offspring = self.varAnd(batch, toolbox)
		
		invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
		invalid_orig = len(invalid_ind)			
		
		matched = [0,0]
		invalid_ind = self.assignDuplicateFitness(container.items, invalid_ind, matched)
			
		invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
		invalid_new = len(invalid_ind)
		
		# print ("\t"+str(self.params.deapSeed)+" - "+str(i)+" | invalid "+str(invalid_new)+" / "+str(invalid_orig)+" (matched "+str(matched[0])+" & "+str(matched[1])+")")
		
		self.evaluate(toolbox, invalid_ind)

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
		best = self.getBestHDRandom(self.container)
		best_length = str(len(best))
		best_fitness = str("%.6f" % best.fitness.values[0])
		derated = best.fitness.values[0] * self.deratingFactor(best)
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

	def assignDuplicateFitness(self, population, offspring, matched):
		
		offspring_chromosomes = []
		for ind in offspring:
			trimmed = self.redundancy.removeRedundancy(str(ind))
			trimmed = self.redundancy.mapNodesToArchive(trimmed)
			offspring_chromosomes.append(trimmed)
		
		
		archive = self.redundancy.getArchive()
		cumulative_archive = self.redundancy.getCumulativeArchive()
		
		archive_count = 0
		cumulative_count = 0
		for i in range(len(offspring)):
			if offspring_chromosomes[i] in archive:
				scores = archive.get(offspring_chromosomes[i])
				offspring[i].fitness.values = (scores[0],)
				offspring[i].features = [scores[1], scores[2], scores[3]]
				# print(str(offspring[i].fitness.values)+" - "+str(offspring[i].features))
				archive_count += 1
			elif offspring_chromosomes[i] in cumulative_archive:
				scores = cumulative_archive.get(offspring_chromosomes[i])
				offspring[i].fitness.values = (scores[0],)
				offspring[i].features = [scores[1], scores[2], scores[3]]
				# print(str(offspring[i].fitness.values)+" - "+str(offspring[i].features))
				cumulative_count += 1
		
		matched[0] = archive_count
		matched[1] = cumulative_count
		
		return offspring

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


	def evaluate(self, toolbox, invalid_ind):
		
		# fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
		# for ind, fit in zip(invalid_ind, fitnesses):
			# ind.fitness.values = fit[0]
			# ind.features = fit[1]
			# print(str(ind.fitness.values)+" - "+str(ind.features))
		self.split(toolbox, invalid_ind)


	def split(self, toolbox, population):

		num_threads = 8

		pop = []
		for i in range(num_threads):
			pop.append([])

		for i in range(len(population)):
			for j in range(num_threads):
				if i % num_threads == j:
					pop[j].append(population[i])
					continue

		threads = []
		threads.append(threading.Thread(target=self.evaluate1, args=(toolbox, [pop[0]])))
		threads.append(threading.Thread(target=self.evaluate2, args=(toolbox, [pop[1]])))
		threads.append(threading.Thread(target=self.evaluate3, args=(toolbox, [pop[2]])))
		threads.append(threading.Thread(target=self.evaluate4, args=(toolbox, [pop[3]])))
		threads.append(threading.Thread(target=self.evaluate5, args=(toolbox, [pop[4]])))
		threads.append(threading.Thread(target=self.evaluate6, args=(toolbox, [pop[5]])))
		threads.append(threading.Thread(target=self.evaluate7, args=(toolbox, [pop[6]])))
		threads.append(threading.Thread(target=self.evaluate8, args=(toolbox, [pop[7]])))

		for thread in threads:
			thread.start()

		for thread in threads:
			thread.join()

	def evaluate1(self, toolbox, population):
		fitnesses = toolbox.map(toolbox.evaluate1, population[0])
		self.assignFitness(population[0], fitnesses)

	def evaluate2(self, toolbox, population):
		fitnesses = toolbox.map(toolbox.evaluate2, population[0])
		self.assignFitness(population[0], fitnesses)

	def evaluate3(self, toolbox, population):
		fitnesses = toolbox.map(toolbox.evaluate3, population[0])
		self.assignFitness(population[0], fitnesses)

	def evaluate4(self, toolbox, population):
		fitnesses = toolbox.map(toolbox.evaluate4, population[0])
		self.assignFitness(population[0], fitnesses)

	def evaluate5(self, toolbox, population):
		fitnesses = toolbox.map(toolbox.evaluate5, population[0])
		self.assignFitness(population[0], fitnesses)

	def evaluate6(self, toolbox, population):
		fitnesses = toolbox.map(toolbox.evaluate6, population[0])
		self.assignFitness(population[0], fitnesses)

	def evaluate7(self, toolbox, population):
		fitnesses = toolbox.map(toolbox.evaluate7, population[0])
		self.assignFitness(population[0], fitnesses)

	def evaluate8(self, toolbox, population):
		fitnesses = toolbox.map(toolbox.evaluate8, population[0])
		self.assignFitness(population[0], fitnesses)

	def assignFitness(self, population, fitnesses):
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
				best = self.getBestHDRandom(aspirants, feature)
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

	def getBestHDRandom(self, population, feature = -1):
		if (feature == -1):
			feature = random.randint(0, self.params.features - 1)
		
		# get the best member of the population
		
		for individual in population:		
			
			thisFitness = individual.fitness.getValues()[feature]
			thisFitness *= self.deratingFactor(individual)
			
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
				
		return best

	def getBestHDRandomMin(self, population, feature = -1):
		if (feature == -1):
			feature = random.randint(0, self.params.features - 1)
		
		# get the best member of the population
		
		for individual in population:		
			
			thisFitness = individual.fitness.getValues()[feature]
			
			currentBest = False
			
			if ('best' not in locals()):
				currentBest = True
			
			elif (thisFitness < bestFitness):
				currentBest = True
			
			elif (thisFitness == bestFitness and bestHeight > 3 and individual.height < bestHeight):
				currentBest = True
				
			if (currentBest):
				best = individual
				bestFitness = thisFitness	
				bestHeight = individual.height
				
		return best

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

	def getBestHDAllOld(self, population):
		
		allBest = []
		
		for i in range(self.params.features):
			
			first = True
			
			for individual in population:		
				
				thisFitness = individual.fitness.getValues()[i]
				
				currentBest = False
				
				if (first):
					currentBest = True
					first = False
				
				elif (thisFitness > bestFitness):
					currentBest = True
				
				elif (thisFitness == bestFitness and bestHeight > 3 and individual.height < bestHeight):
					currentBest = True
					
				if (currentBest):
					best = individual
					bestFitness = thisFitness	
					bestHeight = individual.height
				
			allBest.append(best)
		print ("")
		return allBest

	def deratingFactor(self, individual):
		
		length = float(len(individual))
		
		usage = length - 10 if length > 10 else 0
		usage = usage / 990 if length <= 1000 else 1		
		usage = 1 - usage
		
		return usage



