import sys
sys.path.insert(0, '..')

from params import eaParams
params = eaParams()
params.configure()

if not params.stop:

	import local

	from ea import EA

	import matplotlib as mpl
	mpl.use('Agg')
	import matplotlib.pyplot as plt

	from qdpy.algorithms.deap import *
	# from qdpy.containers import *
	# QD2
	from containers import *
	# from extended_containers import *
	
	from qdpy.benchmarks import *
	from qdpy.plots import *
	from qdpy.base import *

	from deap import base
	from deap import creator
	from deap import tools
	from deap import algorithms
	from deap import gp
	import operator

	import os
	# import numpy as np
	# import random
	import warnings
	import scipy
	import argparse


	def printInfo(grid):
		# print(grid.summary())
		
		# print (len(grid.items))
		# for x in grid.items:
			# print (x)
		# print ("")
		# print("activity_per_bin:\n", grid.activity_per_bin)
		# print("Best ever ind: ", grid.best)
		# print("best_features: ", grid.best_features)
		# print("Best fitness: ", grid.best_fitness)
		# print("best_index: ", grid.best_index)
		# print("capacity: ", grid.capacity)
		# print("depot: ", grid.depot)
		# print("discard_random_on_bin_overload: ", grid.discard_random_on_bin_overload)
		# print("features: ", grid.features)
		# print("features_domain: ", grid.features_domain)
		# print("features_extrema: ", grid.features_extrema)
		# print("filled_bins: ", grid.filled_bins)
		# print("fitness: ", grid.fitness)
		# print("fitness_domain: ", grid.fitness_domain)
		# print("fitness_extrema: ", grid.fitness_extrema)
		# print("free: ", grid.free)
		# print("history_recentness_per_bin: ", grid.history_recentness_per_bin)
		# print("items: ", grid.items)
		# print("max_items_per_bin: ", grid.max_items_per_bin)
		# print("name: ", grid.name)
		# print("nb_added: ", grid.nb_added)
		# print("nb_discarded: ", grid.nb_discarded)
		print("nb_items_per_bin:\n", grid.nb_items_per_bin)
		# print("nb_operations: ", grid.nb_operations)
		# print("nb_rejected: ", grid.nb_rejected)
		# print("quality: ", grid.quality)
		# print("quality_array: ", grid.quality_array)
		# print("recentness: ", grid.recentness)
		# print("recentness_per_bin: ", grid.recentness_per_bin)
		# print("shape: ", grid.shape)
		# print("size (filled bins in the grid): " , (grid.size_str()))
		# print("Solutions found for bins: ", grid.solutions)
		
		# Search for the smallest best in the grid: (refers to tree size, which was originally the first feature)
		# smallest_best = grid.best
		# smallest_best_fitness = grid.best_fitness
		# smallest_best_length = grid.best_features[0]
		# interval_match = 1e-10
		# for ind in grid:
			# if abs(ind.fitness.values[0] - smallest_best_fitness.values[0]) < interval_match:
				# if ind.features[0] < smallest_best_length:
					# smallest_best_length = ind.features[0]
					# smallest_best = ind
		# print("Smallest best:", smallest_best)
		# print("Smallest best fitness:", smallest_best.fitness)
		# print("Smallest best features:", smallest_best.features)
		print("")

	def printBestIndividuals(grid):
		
		# best_to_nest = grid.best
		count = 0
		# for x in grid.best_fitness.getValues():
			# if count == 0: best_to_nest_fitness = x
			# count += 1
		# print (best_to_nest_fitness)
		# interval_match = 1e-10
		# for ind in grid:
			# if abs(ind.fitness.values[0] - best_to_nest_fitness.values[0]) < interval_match:
			# if ind.features[0] == 1:
				# if count == 0:
					# best_to_nest_fitness = ind.fitness.values[0]
					# best_to_nest = ind
					
				# elif ind.fitness.values[0] < best_to_nest_fitness:
					# best_to_nest_fitness = ind.fitness.values[0]
					# best_to_nest = ind
				# count += 1
		# print("Best to nest:", best_to_nest)
		# print("Best to nest fitness:", best_to_nest.fitness)
		# print("")

		# count = 0
		# for ind in grid:
			# if ind.features[1] == 1:
				# if count == 0:
					# best_to_food_fitness = ind.fitness.values[0]
					# best_to_food = ind
				# elif ind.fitness.values[0] < best_to_food_fitness:
					# best_to_food_fitness = ind.fitness.values[0]
					# best_to_food = ind
				# count += 1
		# print("Best to food:", best_to_food)
		# print("Best to food fitness:", best_to_food.fitness)
		# print("")

		# count = 0
		# for ind in grid:
			# if ind.features[2] == 1:
				# if count == 0:
					# best_time_in_nest_fitness = ind.fitness.values[0]
					# best_time_in_nest = ind
				# if ind.fitness.values[0] < best_time_in_nest_fitness:
					# best_time_in_nest_fitness = ind.fitness.values[0]
					# best_time_in_nest = ind
				# count += 1
		# print("Best time in nest:", best_time_in_nest)
		# print("Best time in nest fitness:", best_time_in_nest.fitness)
		print("")

	def parseArguments():
		
		parser = argparse.ArgumentParser()
		parser.add_argument('--seed', type=int, default=None, help="DEAP random seed")
		parser.add_argument('--start', type=int, default=None, help="Start generation")
		parser.add_argument('--end', type=int, default=None, help="Max generations")
		args = parser.parse_args()

		if args.seed != None:
			params.deapSeed = args.seed

		if args.start != None:
			params.start_gen = args.start
			if int(args.start) == 0: params.loadCheckpoint = False
			if int(args.start) > 0: params.loadCheckpoint = True
			# if int(params.start_gen) == 0:
				# params.loadCheckpoint = False

		if args.end != None:
			params.generations = args.end

	fitness_weight = (1.0,)

	parseArguments()
	ea = EA(params)
	print(params.deapSeed)
	
	if params.readCheckpoint:
		
		from deap import base, creator, gp
		import pickle
		creator.create("Fitness", base.Fitness, weights=fitness_weight)
		creator.create("Individual", gp.PrimitiveTree, fitness=creator.Fitness, features=list)
		pset = local.PrimitiveSetExtended("MAIN", 0)
		with open(params.input_filename(), "rb") as f:
			data = pickle.load(f)
		
		print ("\n")
		for i in data:
			if str(i) == "container":
				checkpoint_container = data[i]
			elif str(i) != "random_state":
				print (str(i) + " : " + str(data[i]))
			
			if str(i) == "current_iteration":
				current_iteration = data[i]
		
		print ("")
		
		# ea.utilities.printExtrema(checkpoint_container)

		ea.utilities.printContainer(checkpoint_container)
		if params.saveHeatmap: ea.utilities.saveHeatmap(checkpoint_container, current_iteration)
		
		# printInfo(checkpoint_container)
	   
		# best = []
		# for ind in checkpoint_container:
			# if len(best) < 1:
				# best.append(ind)
			# else:
				# worst = 0.0
				# worst = 1.0
				# worstIndex = 1
				# for i in range(1):
					# if best[i].fitness.values[0] < worst:
						# worst = best[i].fitness.values[0]
						# worstIndex = i
				
				# if ind.fitness.values[0] > worst:
					# best[worstIndex] = ind
			
		# for ind in best:			
			# performance = str("%.5f" % ind.fitness.values[0]) + "  \t"
			# for f in ind.features:
				# performance += str("%.5f" % f) + " \t"
			# print (performance)
			# print (ea.utilities.formatChromosome(ind))
		
			
		# for ind in best:			
			# performance = str("%.5f" % ind.fitness.values[0]) + "  \t"
			# for f in ind.features:
				# performance += str("%.5f" % f) + " \t"
			# print (performance)
		print ("")

	elif params.loadCheckpoint:
		
		from deap import base, creator, gp
		import pickle
		creator.create("Fitness", base.Fitness, weights=fitness_weight)
		creator.create("Individual", gp.PrimitiveTree, fitness=creator.Fitness, features=list)
		pset = local.PrimitiveSetExtended("MAIN", 0)
		print(params.input_filename())
		with open(params.input_filename(), "rb") as f:
			data = pickle.load(f)
		print ("")
		for i in data:
			if str(i) == "container":
				checkpoint_container = data[i]
			elif str(i) == "current_iteration":
				start_gen = data[i]
		
		# print ("read container")
		# print (ea.utilities.printContainer(checkpoint_container))
		# for ind in checkpoint_container:
			# performance = str("%.5f" % ind.fitness.values[0]) + "  \t"
			# for f in ind.features:
				# performance += str("%.5f" % f) + " \t"
			# print (performance)
		

		print ("")

	else:
		start_gen = 0

	if __name__ == "__main__":

		if params.loadCheckpoint:
			grid = checkpoint_container
		else:
			grid = Grid(shape = params.nb_bins, 
							max_items_per_bin = params.max_items_per_bin, 
							fitness_domain = params.fitness_domain, 
							features_domain = params.features_domain, 
							storage_type=list)

		if not params.readCheckpoint:
			
			ea.config(start_gen,
					  grid)

			if params.loadCheckpoint:		
				init_batch = []
				for idx, inds in checkpoint_container.solutions.items():
					if len(inds) == 0:
						continue
					for ind in inds:
						init_batch.append(ind)
				ea.run(init_batch)
			else:
				ea.run()
