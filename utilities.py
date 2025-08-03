
import subprocess
import time
import pickle
import threading

from deap import gp
from deap import tools
from deap import base
from deap import creator

import local

# QD2
from containers import *
# from extended_containers import *

# === heatmap =======

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt

from qdpy.plots import *

import scipy

# ====================

class Utilities():
	
	sequenceNodes = ["seqm2", "seqm3", "seqm4"]
	fallbackNodes = ["selm2", "selm3", "selm4"]
	probabilityNodes = ["probm2", "probm3", "probm4"]
	conditionNodes = ["ifNestToLeft", "ifNestToRight", "ifFoodToLeft", "ifFoodToRight", "ifGotFood", "ifOnFood", "ifInNest", "ifRobotToRight", "ifRobotToLeft"]
	compositeNodes = ["ifgevar", "ifltvar", "ifgecon", "ifltcon", "set"]
	decoratorNodes = ["successd", "failured", "repeat"]
	actionNodes = ["f", "fr", "fl", "r", "rr", "rl", "stop"]
	actuationNodes = ["f", "fr", "fl", "r", "rr", "rl", "stop"]
	successNodes = ["successl", "successd", "f", "fr", "fl", "r", "rr", "rl", "stop"]
	failureNodes = ["failurel", "failured"]
	
	def __init__(self, params, behaviours = None):
		self.params = params
		self.behaviours = behaviours
	
	def setupToolbox(self, tournament):

		toolbox = base.Toolbox()

		pset = local.PrimitiveSetExtended("MAIN", 0)
		self.params.addNodes(pset)

		weights = [] if self.params.is_qdpy else [(1.0),(1.0),(1.0)]
		for i in range(self.params.features): weights.append(1.0)

		creator.create("Fitness", base.Fitness, weights=(weights))
		creator.create("Individual", gp.PrimitiveTree, fitness=creator.Fitness)

		toolbox.register("expr_init", local.genFull, pset=pset, min_=1, max_=4)

		toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr_init)
		toolbox.register("population", tools.initRepeat, list, toolbox.individual)

		toolbox.register("evaluate", self.evaluateRobot, thread_index=1)
		toolbox.register("select", tournament, tournsize=self.params.tournamentSize)

		self.evaluation_functions = []
		for i in range(1,9):
			toolbox.register("evaluate"+str(i), self.evaluateRobot, thread_index=i)
			self.evaluation_functions.append(self.makeEvaluationFunction("evaluate"+str(i)))

		toolbox.register("mate", gp.cxOnePoint)
		toolbox.register("expr_mut", local.genFull, min_=0, max_=2)
		toolbox.register("mutSubtreeReplace", local.mutUniform, expr=toolbox.expr_mut, pset=pset)
		toolbox.register("mutSubtreeShrink", local.mutShrink)
		toolbox.register("mutNodeReplace", local.mutNodeReplacement, pset=pset)

		# for creating trimmed population
		toolbox.register("expr_empty", local.genEmpty, pset=pset, min_=1, max_=4)
		toolbox.register("empty_individual", tools.initIterate, creator.Individual, toolbox.expr_empty)
		toolbox.register("empty_population", tools.initRepeat, list, toolbox.empty_individual)

		self.toolbox = toolbox

	def evaluateRobot(self, individual, thread_index):
		
		# print ("")
		# print (individual)
		
		# save number of robots and chromosome to file
		with open('../txt/chromosome'+str(thread_index)+'.txt', 'w') as f:
			f.write(str(self.params.sqrtRobots))
			f.write("\n")
			f.write(str(individual))
		
		totals = []
		# qdpy optimisation
		# for i in range(self.params.features):
		for i in range(self.params.features + 3):
			# end qdpy
			totals.append(0.0)
		
		fitness = []
		features = []
		robots = {}
		seed = 0
		
		for i in self.params.arenaParams:
			
			# get maximum food available with the current gap between the nest and food
			# maxFood = self.calculateMaxFood(i)
			
			# for j in range(self.params.iterations):
			
			# write seed to file
			seed += 1
			with open('../txt/seed'+str(thread_index)+'.txt', 'w') as f:
				f.write(str(seed))
				f.write("\n")
				f.write(str(i))

			# run argos
			subprocess.call(["/bin/bash", "../evaluate"+str(thread_index), "", "./"])
			
			# result from file
			f = open("../txt/result"+str(thread_index)+".txt", "r")
			
			# print ("")
			for line in f:
				first = line[0:line.find(" ")]
				if (first == "result"):
					# print (line[0:-1])
					lines = line.split()
					robotId = int(float(lines[1]))
					robots[robotId] = []
					for j in range(7): # all objectives are saved to the result file
						for k in range(self.params.iterations):
							if j in self.params.indexes:
								index = (j * self.params.iterations) + k + 2
								robots[robotId].append(float(lines[index]))
					# qdpy optimisation
					for j in range(3):
						for k in range(self.params.iterations):
							# hard coded 7 because foraging is included in footbot controller objectives
							index = (j * self.params.iterations) + (7 * self.params.iterations) + k + 2
							robots[robotId].append(float(lines[index]))
					# end qdpy
					# string = str(robotId)+" "
					# for s in robots[robotId]:
						# string += str(s)+" "
					# print (string)
					# string = str(robotId)+" "
					# for s in robots[robotId][5:20]:
						# string += str(s)+" "
					# print (string)
			
			# get scores for each robot and add to cumulative total
			# qdpy optimisation
			# for k in range(self.params.features):
			for k in range(self.params.features + 3):
				# end qdpy
				totals[k] += self.collectFitnessScore(robots, k)
				# print (totals[k])
			
			# increment counter and pause to free up CPU
			time.sleep(self.params.trialSleep)
		
		# divide to get average per seed and arena configuration then apply derating factor
		# deratingFactor = self.deratingFactor(individual)
		deratingFactor = 1.0
		features = []
		# qdpy optimisation
		# for i in range(self.params.features):
		# for i in range(self.params.features + 3):
			# end qdpy
			# features.append(self.getAvgAndDerate(totals[i], individual, deratingFactor))
		
		for i in range(self.params.features):
			fitness.append(self.getAvgAndDerate(totals[i], individual, deratingFactor))
		for i in range(self.params.characteristics):
			features.append(self.getAvgAndDerate(totals[i + self.params.features], individual, deratingFactor))
		
		# pause to free up CPU
		time.sleep(self.params.evalSleep)
		
		# output = ""
		# for f in features:
			# output += str("%.9f" % f) + " \t"
		# print (output)
		
		if self.params.is_qdpy:
			return (fitness, features)
		else:
			return (fitness + features)

	def collectFitnessScore(self, robots, feature, maxScore = 1.0):

		thisFitness = 0.0
		
		# get food collected by each robot and add to cumulative total
		for r in (range(len(robots))):
			for i in range(self.params.iterations):
				index = (feature * self.params.iterations) + i
				thisFitness += float(robots[r][index])
		# divide to get average for this iteration, normalise and add to running total
		thisFitness /= self.params.sqrtRobots * self.params.sqrtRobots
		thisFitness /= maxScore
		
		return thisFitness
	
	def getAvgAndDerate(self, score, individual, deratingFactor):
		# print (score)
		fitness = score / self.params.iterations
		fitness = fitness / len(self.params.arenaParams)
		# print (fitness)
		fitness /= deratingFactor
		return fitness

	def deratingFactor(self, individual):

		length = float(len(individual))

		# usage = length - 64 if length > 64 else 0
		# usage = usage / 6930 if length <= 6994 else 1
		usage = length - 10 if length > 10 else 0
		usage = usage / 990 if length <= 1000 else 1
		usage = 1 - usage

		return usage

	def deratingFactorForForaging(self, individual):
		
		length = float(self.behaviours.unpack(individual))
		
		usage = length - 100 if length > 100 else 0
		usage = usage / 9900 if length <= 10000 else 1
		usage = 1 - usage
		
		return usage

	def getTrimmedPopulation(self, offspring, redundancy):

		primitivetree = gp.PrimitiveTree([])
		pset = local.PrimitiveSetExtended("MAIN", 0)
		trimmed = self.toolbox.empty_population(n=len(offspring))

		for i in range(len(offspring)):
			trimmed_str = redundancy.removeRedundancy(str(offspring[i]))
			trimmed_tree = primitivetree.from_string(trimmed_str, redundancy.pset)
			trimmed_ind = creator.Individual(trimmed_tree)
			trimmed[i] = trimmed_ind
		
		return trimmed

	def printContainer(self, container):
		
		for idx, inds in container.solutions.items():
			if len(inds) == 0:
				continue
			for ind in inds:
				performance = ""
				for fitness in ind.fitness.values:
					performance += str("%.9f" % fitness) + "  \t"
				for f in ind.features:
					performance += str("%.4f" % f) + " \t"
				print (performance)
				# print (self.printTree(ind))
			print ("---")

	def printBestMax(self, container, qty = 1):
		
		best = []
		for ind in container:
			if len(best) < qty:
				best.append(ind)
			else:
				# worst = 0.0
				worst = 1.0
				worstIndex = qty
				for i in range(qty):
					if best[i].fitness.values[0] < worst:
						worst = best[i].fitness.values[0]
						worstIndex = i
				
				if ind.fitness.values[0] > worst:
					best[worstIndex] = ind
			
		# for ind in best:			
			# performance = str("%.5f" % ind.fitness.values[0]) + "  \t"
			# for f in ind.features:
				# performance += str("%.5f" % f) + " \t"
			# print (performance)
			# print (self.formatChromosome(ind))
		
			
		print ("")
		print ("Print best individual(s)")
		print ("")
		for ind in best:			
			performance = str("%.9f" % ind.fitness.values[0]) + "  \t"
			for f in ind.features:
				performance += str("%.4f" % f) + " \t"
			print (performance)
			print (ind)
		
		print ("")
	
	def getBestMax(self, container, qty = 1):
		
		best = []
		for ind in container:
			if len(best) < qty:
				best.append(ind)
			else:
				# worst = 0.0
				worst = 1.0
				worstIndex = qty
				for i in range(qty):
					if best[i].fitness.values[0] < worst:
						worst = best[i].fitness.values[0]
						worstIndex = i
				
				if ind.fitness.values[0] > worst:
					best[worstIndex] = ind
		return best
	
	def printBestMin(self, container, qty = 1):
		
		best = []
		for ind in container:
			if len(best) < qty:
				best.append(ind)
			else:
				worst = 0.0
				worstIndex = qty
				for i in range(qty):
					if best[i].fitness.values[0] > worst:
						worst = best[i].fitness.values[0]
						worstIndex = i
				
				if ind.fitness.values[0] < worst:
					best[worstIndex] = ind
		
		for ind in best:			
			performance = str("%.9f" % ind.fitness.values[0]) + "  \t"
			for f in ind.features:
				performance += str("%.4f" % f) + " \t"
			print (performance)
		
		print ("")
	
	def printExtrema(self, container):
		
		minVals = [1.0,1.0,1.0]
		maxVals = [0.0,0.0,0.0]
		minIndividuals = [None, None, None]
		maxIndividuals = [None, None, None]
		
		for idx, inds in container.solutions.items():
			if len(inds) == 0:
				continue
			
			for i in range(len(self.params.nb_bins)):
				for ind in inds:
					if minVals[i] > ind.features[i]:
						minVals[i] = ind.features[i]
						minIndividuals[i] = ind
					if maxVals[i] < ind.features[i]:
						maxVals[i] = ind.features[i]
						maxIndividuals[i] = ind
			
		# for ind in minIndividuals:
			# performance = str("%.5f" % ind.fitness.values[0]) + "  \t"
			# for f in ind.features:
				# performance += str("%.5f" % f) + " \t"
			# print (performance)
		# print ("---")

		# for ind in maxIndividuals:
			# performance = str("%.5f" % ind.fitness.values[0]) + "  \t"
			# for f in ind.features:
				# performance += str("%.5f" % f) + " \t"
			# print (performance)
		# print ("---")
		# print ("=============")

		# print ("== extrema ==")
		vals = ""
		for i in minVals:
			vals += str("%.5f" % i)+"\t\t"
		vals += "\n"
		for i in maxVals:
			vals += str("%.5f" % i)+"\t\t"
		print (vals)

	def getBestHDRandom(self, population, feature = -1, derate = True):

		if (feature == -1):
			feature = random.randint(0, self.params.features - 1)

		for individual in population:

			thisFitness = individual.fitness.getValues()[feature]

			if derate:
				if self.params.description == "foraging":
					thisFitness *= self.deratingFactorForForaging(individual)
				else:
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

	def getBestAll(self, population, derate = True):

		allBest = []
		for feature in range(self.params.features):
			allBest.append(self.getBestHDRandom(population, feature, derate))
		return allBest


	def removeDuplicates(self, offspring, container):
		# print ("\ncheck for duplicates\n")
		for i in reversed(range(len(offspring))):
			ind = offspring[i]
			duplicate = ""
			if ind in container.items:
				duplicate = "DUPLICATE container"
			else:
				for j in reversed(range(i)):
					if offspring[j] == ind:
						duplicate = "DUPLICATE offspring"
						break
			performance = str("%.5f" % ind.fitness.values[0]) + "  \t"
			for f in ind.features:
				performance += str("%.5f" % f) + " \t"
			
			if len(duplicate) > 0: 
				output = duplicate + "\t" + performance
				# print (output)
				offspring.pop(i)

	def convertToNewGrid(self, container, objective, objective_index, features, shape, fitness_domain, features_domain):
		
		# from deap import base, creator, tools, gp
		# weights = (1.0,)
		# if features == 3: weights = (1.0,1.0,1.0,)

		# creator.create("Fitness", base.Fitness, weights=weights)
		# creator.create("Individual", gp.PrimitiveTree, fitness=creator.Fitness, features=list)
		# pset = gp.PrimitiveSet("MAIN", 0)

		fittest_flat = []
		for idx, inds in container.solutions.items():
			if len(inds) == 0:
				continue
			best = None
			for ind in inds:
				if best is None:
					best = ind
				elif features > 1:
					if ind.fitness.values[objective_index] > best.fitness.values[objective_index]:
						best = ind
				elif ind.fitness.values[0] > best.fitness.values[0]:
					best = ind
			if features > 1:
				fitness = []
				for i in range(features):
					fitness.append(best.fitness.values[objective_index])
				best.fitness.values = fitness
			fittest_flat.append(best)

		grid = Grid(shape = shape,
					max_items_per_bin = 1,
					fitness_domain = fitness_domain,
					features_domain = features_domain,
					storage_type=list)

		nb_updated = grid.update(fittest_flat, issue_warning = True)
		return grid

	def saveQdResults(self, container):
		
		with open('QD-'+str(self.params.generations)+'.csv', 'a') as f:
			for idx, inds in container.solutions.items():
				if len(inds) == 0:
					continue
				for ind in inds:
					performance = str("%.5f" % ind.fitness.values[0]) + "  \t"
					for feature in ind.features:
						performance += str("%.5f" % feature) + ","
					f.write(performance)
					f.write(",\""+str(ind)+"\"")
					f.write("\n")
				f.write("\n")

	def saveBestToFile(self, best):
		
		with open('../best.txt', 'w') as f:
			f.write(str(self.params.sqrtRobots))
			f.write("\n")
			f.write(str(best))

	def saveBestIndividuals(self, population):

		if self.params.saveBestIndividuals or self.params.saveAllIndividuals:

			if not self.params.saveAllIndividuals:
				population = self.getBestAll(population)

			with open('../txt/current.txt', 'w') as f:
				f.write("\n")

			for b in population:

				with open('../txt/current.txt', 'a') as f:
					f.write("\n")
					f.write(str(b.fitness))
					f.write("\n\n")
					f.write(self.formatChromosome(b))
					f.write("\n============================================\n")

	def formatChromosome(self, chromosome):
		
		tree = ""
		indent = ""
		lineEnding = "\n"
		
		childrenRemaining = []
		insideComposite = 0
		insideSubtree = True
		
		for i in range(len(chromosome)):
			
			node = chromosome[i].name
			
			# ======= inner nodes =======
			
			if node.lower() in self.sequenceNodes + self.fallbackNodes + self.probabilityNodes + self.decoratorNodes:
				
				if len(childrenRemaining) > 0: childrenRemaining[-1] -= 1
				
				if node.lower() == "repeat": childrenRemaining.append(2)
				elif node.lower() in self.decoratorNodes: childrenRemaining.append(1)
				else: childrenRemaining.append(int(node[-1]))
				
				# check if any children are inner nodes
				insideSubtree = False
				composites = 0
				j = i + 1
				limit = j + childrenRemaining[-1]
				while j < limit:
					if chromosome[j].name.lower() in self.sequenceNodes + self.fallbackNodes + self.probabilityNodes + self.decoratorNodes:
						insideSubtree = True
						break
					# if chromosome[j].lower() in self.compositeNodes:
						# limit += 2
					j += 1
				
				# if all children are terminals print them on one line
				if insideSubtree:
					tree += indent + node +"(" + lineEnding
					indent += "   "
				else:
					lineEnding = ""
					tree += indent + node +"("
			
			# ==== composite nodes ====
			
			# elif node.lower() in self.compositeNodes:
				# if len(childrenRemaining) > 0: childrenRemaining[-1] -= 1
				# if insideSubtree: tree += indent
				# tree += node + "(" + chromosome[i+1] + ", " + chromosome[i+2] + ")"
				# if len(childrenRemaining) > 0 and childrenRemaining[-1] > 0: tree += ", "
				# tree += lineEnding
				# insideComposite = 2
				
			# elif insideComposite > 0:
				# insideComposite -= 1
				# continue
			
			# ======= terminals =======
			
			else:
				comma = ", " if len(childrenRemaining) > 0 and childrenRemaining[-1] > 1 else ""
				if insideSubtree: tree += indent
				tree += node + comma + lineEnding
				if len(childrenRemaining) > 0: childrenRemaining[-1] -= 1
			
			# ==== closing brackets ====
			
			if len(childrenRemaining) == 0 or childrenRemaining[-1] == 0:
				for i in range(len(childrenRemaining) - 1, -1, -1):
					if childrenRemaining[i] == 0: 
						childrenRemaining.pop()
						if insideSubtree: 
							indent = indent[0:-3]
							tree += indent
						insideSubtree = True
						lineEnding = "\n"
						comma = "" if i == 0 or childrenRemaining[i-1] == 0 else ", "
						tree += ")" + comma + lineEnding
					else: break
		
		return tree

	def getCoverage(self, container):
		
		""" get the ratio of filled vs empty bins, returns a value between 0 and 1"""
		
		filled_bins = 0.0
		for i in range(len(container.nb_items_per_bin)):
			for j in range(len(container.nb_items_per_bin[i])):
				for k in range(len(container.nb_items_per_bin[i][j])):
					if container.nb_items_per_bin[i][j][k] > 0:
						filled_bins += 1
		shape = self.params.nb_bins
		filled_bins /= shape[0]*shape[1]*shape[2]
		# print(container.nb_items_per_bin)
		return filled_bins

	def getQDScore(self, container):
		
		# can only handle one objective
		
		shape = self.params.nb_bins
				
		grid = self.convertToNewGrid(container,
								     self.params.description,
								     self.params.indexes[0],
								     self.params.features,
								     shape,
								     self.params.fitness_domain,
								     self.params.features_domain)
		
		total_fitness = 0.0		
		for idx, inds in grid.solutions.items():
			if len(inds) == 0:
				continue
			for ind in inds:
				# print (ind.fitness.values[0])
				total_fitness += ind.fitness.values[0]
		total_fitness /= shape[0]*shape[1]*shape[2]
		
		return total_fitness

	def saveQDScore(self, container, iteration, mode="a"):
				
		# shape = self.params.nb_bins
				
		# grid = self.convertToNewGrid(container,
								     # self.params.objective,
								     # self.params.objective_index,
								     # self.params.features,
								     # shape,
								     # self.params.fitness_domain,
								     # self.params.features_domain)
		# print("\n\nflat grid\n")
		# self.printContainer(grid)
		
		# total_fitness = 0.0		
		# for idx, inds in grid.solutions.items():
			# if len(inds) == 0:
				# continue
			# for ind in inds:
				# print (ind.fitness.values[0])
				# total_fitness += ind.fitness.values[0]
		# total_fitness /= shape[0]*shape[0]*shape[0]
		
		
		total_fitness = self.getQDScore(container)
		
		output = str(iteration)+","+str(total_fitness)+"\n"

		filename = self.params.path() + "csvs/qd-scores-"+str(self.params.deapSeed)+".csv"
		with open(filename, mode) as f:
			f.write(output)

	def saveBestToCsv(self, container, iteration, mode="a"):
		
		filename = self.params.path() + "csvs/best-"+str(self.params.deapSeed)+".csv"
		best = self.getBestMax(container)
		
		output = str(iteration)
		for i in range(self.params.features):
			output += ","+str(best[i].fitness.values[i])
		output += "\n"

		with open(filename, mode) as f:
			f.write(output)

	def saveCoverage(self, container, iteration, mode="a"):

		filename = self.params.path() + "csvs/coverage-"+str(self.params.deapSeed)+".csv"
		coverage = self.getCoverage(container)

		output = str(iteration) + "," + str(coverage) + "\n"

		with open(filename, mode) as f:
			f.write(output)

	def saveHeatmap(self, container, iteration):

		plot_path = self.params.path() + "heatmaps/heatmap-"+str(self.params.deapSeed)+"-iteration"+str(iteration)+".png"
		plotGridSubplots(container.quality_array[... ,0],
						 plot_path,
						 plt.get_cmap("nipy_spectral"),
						 container.features_domain,
						 container.fitness_extrema[0],
						 nbTicks=None)

	def saveConfigurationFile(self):

		experiment_length = 500 if self.params.description == "foraging" else 100
		with open('../txt/configuration.txt', 'w') as f:
			f.write("experimentLength:"+str(experiment_length))

	def saveParams(self):

		if self.params.saveOutput:
			with open(self.params.path()+"params.txt", 'a') as f:
				f.write("\n")
				f.write("time: "+str(time.ctime()) + "\n")
				f.write("deapSeed: "+str(self.params.deapSeed) + "\n")
				f.write("populationSize: "+str(self.params.populationSize) + "\n")
				f.write("tournamentSize: "+str(self.params.tournamentSize) + "\n")
				f.write("features: "+str(self.params.features) + "\n")
				f.write("description: "+self.params.description + "\n")

	def saveDuration(self, start_time, end_time):

		duration = end_time - start_time
		minutes = (duration / 1000) / 60
		minutes_str = str("%.2f" % minutes)
		print("Duration " +minutes_str+"\n")

		if self.params.saveOutput:
			with open(self.params.path()+"params.txt", 'a') as f:
				f.write("generations: "+str(self.params.generations) + "\n")
				f.write("duration: "+str(duration) + " ms ("+minutes_str+" minutes)\n")



	def evaluate(self, assign_fitness, invalid_ind):

		# fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
		# assign_fitness(invalid_ind, fitnesses)

		self.split(assign_fitness, invalid_ind)


	def split(self, assign_fitness, population):

		num_threads = self.params.num_threads

		pop = []
		for i in range(num_threads):
			pop.append([])

		for i in range(len(population)):
			for j in range(num_threads):
				if i % num_threads == j:
					pop[j].append(population[i])
					continue

		threads = []
		for i in range(num_threads):
			threads.append(threading.Thread(target=self.evaluation_functions[i], args=(assign_fitness, [pop[i]], getattr(self.toolbox, "evaluate"+str(i+1)))))

		for thread in threads:
			thread.start()

		for thread in threads:
			thread.join()


	def makeEvaluationFunction(self, name):

		def _method(assign_fitness, population, evaluation_function):
			toolbox_function = getattr(self.toolbox, name)
			fitnesses = self.toolbox.map(toolbox_function, population[0])
			assign_fitness(population[0], fitnesses)

		return _method
