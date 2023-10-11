
import subprocess
import time
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
	
	def __init__(self, params):
		self.params = params
	
	def evaluateRobotHdOnly(self, individual, thread_index):
		
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
					for j in range(self.params.features):
						for k in range(self.params.iterations):
							index = (self.params.objective_index * self.params.iterations) + (j * self.params.iterations) + k + 2
							robots[robotId].append(float(lines[index]))
					# qdpy optimisation
					for j in range(3):
						for k in range(self.params.iterations):
							index = (j * self.params.iterations) + (6 * self.params.iterations) + k + 2
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
		for i in range(self.params.features + 3):
			# end qdpy
			features.append(self.getAvgAndDerate(totals[i], individual, deratingFactor))
		
		# pause to free up CPU
		time.sleep(self.params.evalSleep)
		
		# output = ""
		# for f in features:
			# output += str("%.9f" % f) + " \t"
		# print (output)
		
		return (features)

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

	def printIndividual(self, ind):
		performance = ""
		for fitness in ind.fitness.values:
			performance += str("%.9f" % fitness) + "  \t"
		for f in ind.features:
			performance += str("%.4f" % f) + " \t"
		print (performance)
		# print ("---")

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
		# if objective == "fitness_grid": weights = (-1.0,)

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
				elif objective == "fitness_grid":
					if ind.fitness.values[0] < best.fitness.values[0]:
						best = ind
				# elif self.params.features > 1:
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
						
		if False:
			if objective == "fitness_grid":
				grid = Grid(#shape = [24,20,20],
							# shape = [5,12,12],
							shape = shape,
							max_items_per_bin = 1,
							# fitness_domain = [(0., numpy.inf)],
							fitness_domain = fitness_domain,
							# features_domain = [(0.2, 0.8), (0.0, 1.0), (0.0, 1.0)],
							# features_domain = [(0.45, 0.575), (0.2, 0.8), (0.3, 0.9)],
							features_domain = features_domain,
							storage_type=list)
			else:
				if features == 1:
					grid = Grid(#shape = [8,8,8],
								shape = shape,
								max_items_per_bin = 1,
								# fitness_domain = [(0., numpy.inf)],
								fitness_domain = fitness_domain,
								# features_domain = [(-40.0, 40.0), (-40.0, 40.0), (0.0, 1.0)],
								features_domain = features_domain,
								storage_type=list)
				else:
					grid = Grid(# shape = [8,8,8],
								shape = shape,
								max_items_per_bin = 1,
								# fitness_domain = [(0., numpy.inf),(0., numpy.inf),(0., numpy.inf)],
								fitness_domain = fitness_domain,
								# features_domain = [(-40.0, 40.0), (-40.0, 40.0), (0.0, 1.0)],
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

	def printIndividuals(self, population):
		for ind in population:
			performance = ""
			for f in ind.fitness.values:
				performance += str("%.9f" % f) + " \t"
			for f in ind.features:
				performance += str("%.9f" % f) + " \t"
			print (performance)
			# print (ind)
		print ("=================================")

	def printTree(self, tree):
		
		string = ""
		stack = []
		for node in tree:
			stack.append((node, []))
			while len(stack[-1][1]) == stack[-1][0].arity:
				prim, args = stack.pop()
				string = prim.format(*args)
				if (string[1:4].find(".") >= 0): string = string[0:5]
				if len(stack) == 0:
					break  # If stack is empty, all nodes should have been seen
				stack[-1][1].append(string)

		return string

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
			chromosomes += ""+self.printTree(best)+" + "
		chromosomes = chromosomes[0:-3]
		chromosomes += "\","
		self.output += chromosomes

	def logNodes(self):
		for node in self.params.nodes:
			if node: self.output += node+" "
		self.output += ","

	def saveOutput(self):
		logHeaders = "Type,Time,Seed,Robots,Pop,Tourn,Iterations,Params,,"
		for i in range(self.params.generations + 1):
			logHeaders += str(i)+","
		logHeaders += ",Chromosome,Nodes,"
		
		with open('features'+str(self.params.generations)+'.csv', 'a') as f:
			f.write(logHeaders)
			f.write("\n")
			f.write(self.output)
	
	
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

	def saveBestIndividuals(self, container, iteration, mode="a"):
		
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
		if self.params.fitness_grid:
			shape = self.params.nb_bins
			coverage = len(container.items)
			coverage /= shape[0]*shape[1]*shape[2]
		else:
			coverage = self.getCoverage(container)
		
		output = str(iteration) + "," + str(coverage) + "\n"

		with open(filename, mode) as f:
			f.write(output)
		
	def saveExtrema(self, container, iteration):
		
		filename = self.params.path() + "csvs/extremis-"+str(self.params.deapSeed)+".csv"
		
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
			
		output = str(iteration) + ","
		for i in minVals:
			output += str(i)+","
		for i in maxVals:
			output += str(i)+","
		output += "\n"
		
		with open(filename, 'a') as f:
			f.write(output)
			





	def saveHeatmap(self, container, iteration):

		plot_path = self.params.path() + "heatmaps/heatmap-"+str(self.params.deapSeed)+"-iteration"+str(iteration)+".png"
		plotGridSubplots(container.quality_array[... ,0],
						 plot_path,
						 plt.get_cmap("nipy_spectral"),
						 container.features_domain,
						 container.fitness_extrema[0],
						 nbTicks=None)

