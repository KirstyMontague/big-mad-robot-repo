

import random
import time
import subprocess
import pickle
import threading
import sys
import os

from deap import gp
from deap import tools
from deap import base
from deap import creator

from redundancy import Redundancy
from utilities import Utilities


class EA():
	
	sequenceNodes = ["seqm2", "seqm3", "seqm4"]
	fallbackNodes = ["selm2", "selm3", "selm4"]
	probabilityNodes = ["probm2", "probm3", "probm4"]
	conditionNodes = ["ifNestToLeft", "ifNestToRight", "ifFoodToLeft", "ifFoodToRight", "ifGotFood", "ifInNest", "ifRobotToRight", "ifRobotToLeft"]
	compositeNodes = ["ifgevar", "ifltvar", "ifgecon", "ifltcon", "set"]
	decoratorNodes = ["successd", "failured", "repeat"]
	actionNodes = ["f", "fr", "fl", "r", "rr", "rl", "stop"]
	actuationNodes = ["f", "fr", "fl", "r", "rr", "rl", "stop"]
	successNodes = ["successl", "successd", "f", "fr", "fl", "r", "rr", "rl", "stop"]
	failureNodes = ["failurel", "failured"]
	
	output = ""
	
	
	def __init__(self):
		self.redundancy = Redundancy()
		# random.seed(self.params.deapSeed)
	
	def setParams(self, params):
		self.params = params
		self.utilities = Utilities(params)
		

		toolbox = base.Toolbox()

		pset = gp.PrimitiveSet("MAIN", 0)
		self.params.addNodes(pset)

		weights = []
		for i in range(self.params.features): weights.append(1.0)
		# qdpy optimisation
		weights.append(1.0)
		weights.append(1.0)
		weights.append(1.0)
		# end qdpy
		weights2 = (weights)
		creator.create("Fitness", base.Fitness, weights=weights2)
		creator.create("Individual", gp.PrimitiveTree, fitness=creator.Fitness)

		toolbox.register("expr_init", gp.genFull, pset=pset, min_=1, max_=4)

		toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr_init)
		toolbox.register("population", tools.initRepeat, list, toolbox.individual)

		toolbox.register("evaluate", self.utilities.evaluateRobot, thread_index=1)
		toolbox.register("evaluate1", self.utilities.evaluateRobot, thread_index=1)
		toolbox.register("evaluate2", self.utilities.evaluateRobot, thread_index=2)
		toolbox.register("evaluate3", self.utilities.evaluateRobot, thread_index=3)
		toolbox.register("evaluate4", self.utilities.evaluateRobot, thread_index=4)
		toolbox.register("select", self.selTournament, tournsize=self.params.tournamentSize)

		toolbox.register("mate", gp.cxOnePoint)
		toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
		toolbox.register("mutSubtreeReplace", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)
		toolbox.register("mutSubtreeShrink", gp.mutShrink)
		toolbox.register("mutNodeReplace", gp.mutNodeReplacement, pset=pset)

		self.toolbox = toolbox

	def selTournament(self, individuals, k, tournsize, fit_attr="fitness"):		
		chosen = []
		for i in range(k):
			aspirants = tools.selRandom(individuals, tournsize)
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
				f.write("loadCheckpoint: "+("yes" if self.params.loadCheckpoint else "no") + "\n")
				f.write("start_gen: "+str(self.params.start_gen) + "\n")
				f.write("generations: "+str(self.params.generations) + "\n")
				f.write("arenaParams: "+str(self.params.arenaParams[0])+", "+str(self.params.arenaParams[1])+"\n")

	def saveDuration(self, duration, minutes_str):
		
		if self.params.saveOutput:
			with open(self.params.path()+"params.txt", 'a') as f:
				f.write("duration: "+str(duration)+" ("+minutes_str+") minutes\n")
	
	def loadArchives(self):
		
		archive = self.redundancy.getArchive()
		cumulative_archive = self.redundancy.getCumulativeArchive()
		# archive_filename = "./test/"+self.params.description+"/archive.txt"
		
		for i in range(self.params.deapSeed - 1):
			archive_path = "./test/"+self.params.description+"/"+str(i+1)+"/archive.pkl"
			if os.path.exists(archive_path):
				with open(archive_path, "rb") as archive_file:
					cumulative_archive.update(pickle.load(archive_file))
		
		temp_archive = {}
		if os.path.exists(self.params.path()+"archive.pkl"):
			with open(self.params.path()+"archive.pkl", "rb") as archive_file:
				temp_archive = pickle.load(archive_file)
		
		print (len(temp_archive))
		i = 0
		for chromosome, scores in temp_archive.items():
			if i < len(temp_archive) - 0:
				archive.update({str(chromosome) : scores})
				i += 1
			
		self.redundancy.setArchive(archive)
		self.redundancy.setCumulativeArchive(cumulative_archive)
			
		# if os.path.exists(self.params.path()+"archive.txt"):
			# f = open(self.params.path()+"archive.txt", "r")
			# for line in f:
				# items = line.split("+")
				# fitness_strings = items[1].split(",")
				# fitness = []
				# for f in fitness_strings:
					# fitness.append(float(f))
				# self.redundancy.addToLibrary(items[0], tuple(fitness))
		
		print("archive length "+str(len(archive)))
		print("cumulative archive length "+str(len(cumulative_archive)))
	
	def saveArchive(self):
		
		if self.params.saveOutput:
			archive = self.redundancy.getArchive()
			verbose_archive = self.redundancy.getVerboseArchive()
			archive_string = ""
			archive_dict = {}
			
			for chromosome, fitness in archive.items():
				archive_dict.update({str(chromosome) : fitness})

			for chromosome, fitness in verbose_archive.items():
				archive_string += str(chromosome)+"+"
				for f in fitness:
					archive_string += str(f)+","
				archive_string = archive_string[0:-1]
				archive_string += "\n"

			with open(self.params.path()+"archive.txt", 'w') as f:
				f.write(archive_string)
				
			with open(self.params.path()+"archive.pkl", "wb") as archive_file:
				 pickle.dump(archive_dict, archive_file)

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
		
		self.printIndividuals(self.getBestHDAll(population), True)
		
		# print(output)
		return population
		
		self.params.features = 1
		for i in range(len(population)):
			self.evaluateRobot(population[i], 5)
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
		
		
		
		population = self.toolbox.population(n=self.params.populationSize)
	
		self.params.start_gen = 0	
		
		matched = self.evaluateNewPopulation(True, self.params.start_gen, population)
				
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
				bestThisPop = self.getBestHDRandom(population, i)
				allBest.append(bestThisPop)		
				performance = ""
				for f in bestThisPop.fitness.values:
					performance += str("%.5f" % f) + " \t"

			chromosomes = ",\""
			for bestThisPop in allBest:
				chromosomes += ""+self.printTree(bestThisPop)+" + "
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
		invalid_ind = self.assignDuplicateFitness(invalid_ind, matched)
		
		invalid_ind = [ind for ind in population if not ind.fitness.valid]
		invalid_new = len(invalid_ind)
		
		self.evaluate(self.toolbox, invalid_ind)
		
		for ind in invalid_ind:
			self.redundancy.addToLibrary(str(ind), ind.fitness.values)
		
		best = self.getBestHDAll(population)
		# self.printIndividuals(best, True)
					
		scores = ""
		for i in range(self.params.features):
			scores += str("%.7f" % best[i].fitness.values[i]) + " \t"
		
		print ("\t"+str(self.params.deapSeed)+" - "+str(generation)+" - "+str(scores)+str(len(best[0]))+"\tinvalid "+str(invalid_new)+" / "+str(invalid_orig)+" (matched "+str(matched[0])+" & "+str(matched[1])+")")

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
				print (b.fitness)
				print (b)
				print (self.formatChromosome(b))
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
					print (self.formatChromosome(ind))
			print ("")
					

	def eaInit(self, population, stats=None, halloffame=None, verbose=__debug__):

		start_time = round(time.time() * 1000)
		
		self.loadArchives()
		
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
		
		self.saveParams()
		
		# begin evolution
		self.eaLoop(population, self.params.start_gen, self.params.generations, stats)

		# get the best individual at the end of the evolutionary run
		best = self.getBestHDAll(population)
		for ind in best:
			self.printIndividual(ind)
		
		# log chromosome and test performance in different environments
		self.logChromosomes(best)
		self.logNodes()
		
		self.saveCheckpoint(self.params.generations, population)
		self.saveArchive()
		
		end_time = round(time.time() * 1000)
		duration = end_time - start_time
		minutes = (duration / 1000) / 60
		minutes_str = str("%.2f" % minutes)		
		print("duration " +minutes_str)
		
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
				elite = self.getBestHDRandom(population, i)
				elites.append(elite)	
			
			offspring = self.toolbox.select(population, len(population)-self.params.features)			
			offspring = self.varAnd(offspring, self.toolbox)	
			
			newPop = elites + offspring
			population[:] = newPop
			
			self.evaluateNewPopulation(False, gen, population)
			
			

			# best = self.getBestHDAll(population)
			# self.logFitness(best)
			
			self.printScores(elites, self.params.printEliteScores)
			self.printScores(offspring, self.params.printFitnessScores)
			self.printIndividuals(self.getBestHDAll(population), self.params.printBestIndividuals)
			
			self.saveCheckpoint(gen, population)
			self.saveCSV(gen, population)


	def assignDuplicateFitness(self, offspring, matched):
		
		# print ("population chromosomes\n")
		
		# population_chromosomes = []
		# for ind in population:
			# trimmed = self.redundancy.removeRedundancy(str(ind))
			# population_chromosomes.append(trimmed)
			# print("")
			# print(trimmed)
		
		# print ("\noffspring chromosomes\n")
		offspring_chromosomes = []
		for ind in offspring:
			# print("")
			# print(str(ind))
			trimmed = self.redundancy.removeRedundancy(str(ind))
			trimmed = self.redundancy.mapNodesToArchive(trimmed)
			offspring_chromosomes.append(trimmed)
			# print(trimmed)
		
		
		archive = self.redundancy.getArchive()
		cumulative_archive = self.redundancy.getCumulativeArchive()
		
		# for chromosome, fitness in archive.items():
			# print(chromosome)
		# print ("\n\n")
		
		# print ("check duplicates")
		archive_count = 0
		cumulative_count = 0
		for i in range(len(offspring)):
			if offspring_chromosomes[i] in archive:
				offspring[i].fitness.values = archive.get(offspring_chromosomes[i])
				archive_count += 1
			elif offspring_chromosomes[i] in cumulative_archive:
				offspring[i].fitness.values = cumulative_archive.get(offspring_chromosomes[i])
				cumulative_count += 1
			# for j in range(len(archive[0])):				
				# print("==")
				# print(offspring_chromosomes[i])
				# print(archive[0][j])
				# if str(offspring_chromosomes[i]) == str(archive[0][j]):
					# print("matched\n")
					# break
			# print("\n====================================\n")
		# print("==")			
		# print("\tmatched "+str(archive_count)+" and "+str(cumulative_count))
		matched[0] = archive_count
		matched[1] = cumulative_count
		
		# redundancy.checkRedundancy()
		# redundancy.removeRedundancy("probm3(selm4(seqm2(ifRobotToRight, rr), rl, selm2(rr, ifRobotToRight), probm2(seqm2(seqm2(seqm2(ifNestToRight, seqm2(ifRobotToRight, selm2(rl, rr))), ifInNest), rl), ifOnFood)), selm4(seqm2(selm2(ifRobotToRight, seqm2(ifOnFood, seqm2(seqm2(seqm2(seqm2(rl, seqm2(ifRobotToRight, rr)), fr), seqm2(ifOnFood, rr)), rr))), rr), rl, rr, seqm2(selm4(seqm2(rr, ifRobotToRight), ifInNest, selm2(fr, ifRobotToLeft), probm2(seqm2(rl, seqm2(selm2(ifRobotToRight, seqm2(rl, rr)), rr)), rr)), probm2(rl, seqm2(ifRobotToRight, rr)))), r)")
		return offspring

	def evaluate(self, toolbox, invalid_ind):
		
		# fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
		# for ind, fit in zip(invalid_ind, fitnesses):
			# print(fit)
			# ind.fitness.values = fit
		fitnesses = self.split(toolbox, invalid_ind)

	def split(self, toolbox, population):

		pop1 = []
		pop2 = []
		# ~ pop3 = []
		# ~ pop4 = []
		fitnesses1 = []
		fitnesses2 = []
		# ~ fitnesses3 = []
		# ~ fitnesses4 = []
		for i in range(len(population)):
			if i % 2 == 0: pop1.append(population[i])
			else: pop2.append(population[i])
			# ~ if i % 4 == 0: pop1.append(population[i])
			# ~ elif i % 4 == 1: pop2.append(population[i])
			# ~ elif i % 4 == 2: pop3.append(population[i])
			# ~ else: pop4.append(population[i])

		trd1 = threading.Thread(target=self.evaluate1, args=(toolbox, [pop1]))
		trd2 = threading.Thread(target=self.evaluate2, args=(toolbox, [pop2]))
		# ~ trd3 = threading.Thread(target=self.evaluate3, args=(toolbox, [pop3]))
		# ~ trd4 = threading.Thread(target=self.evaluate4, args=(toolbox, [pop4]))
		trd1.start()
		trd2.start()
		# ~ trd3.start()
		# ~ trd4.start()
		trd1.join()
		trd2.join()
		# ~ trd3.join()
		# ~ trd4.join()
		# ~ return fitnesses1 + fitnesses2 + fitnesses3 + fitnesses4
		return fitnesses1 + fitnesses2

	def evaluate1(self, toolbox, population):
		fitnesses = toolbox.map(toolbox.evaluate1, population[0])
		for ind, fit in zip(population[0], fitnesses):
			ind.fitness.values = fit

	def evaluate2(self, toolbox, population):
		fitnesses = toolbox.map(toolbox.evaluate2, population[0])
		for ind, fit in zip(population[0], fitnesses):
			ind.fitness.values = fit

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
			
			objective_multiplier = self.params.objective_index * self.params.iterations
			
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
							index = objective_multiplier + (j * self.params.iterations) + k + 2
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

	def collectFitnessScore(self, robots, feature, maxScore = 1.0):

		thisFitness = 0.0
		fitnessString = ""
		
		# get food collected by each robot and add to cumulative total
		for r in (range(len(robots))):
			# print (robots[r])
			for i in range(self.params.iterations):
				index = (feature * self.params.iterations) + i
				thisFitness += float(robots[r][index])
				fitnessString += "," + str(robots[r][index])
		# print (fitnessString)
		# print (thisFitness)
		
		# divide to get average for this iteration, normalise and add to running total
		thisFitness /= self.params.sqrtRobots * self.params.sqrtRobots
		thisFitness /= maxScore
		# print (thisFitness)
		# print ("----")
		return thisFitness
	
	def getAvgAndDerate(self, score, individual, deratingFactor):
		# print (score)
		fitness = score / self.params.iterations
		fitness = fitness / len(self.params.arenaParams)
		# print (fitness)
		fitness /= deratingFactor
		return fitness

	def jonesDeratingFactor(self, individual):
		
		height = float(individual.height)
		length = float(len(individual))
		
		rUsage = height / 30
		if (length / 140 > rUsage):
			rUsage = length / 140
			
		factor = 1
		if rUsage > .75:
			rUsage -= .75
			factor = 1 - (rUsage * 4)
			if factor < 0:
				factor = 0
		
		return factor
		
	def deratingFactor(self, individual):
		
		length = float(len(individual))
		
		usage = length - 10 if length > 10 else 0
		usage = usage / 990 if length <= 1000 else 1		
		usage = 1 - usage
		
		return usage
		
		

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

	def getBestHDAll(self, population):
		
		allBest = []
		
		for i in range(self.params.features):
			
			first = True
			
			for individual in population:		
				
				thisFitness = individual.fitness.getValues()[i]
				thisFitness *= self.deratingFactor(individual)
				
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
		
		return allBest

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
		
		with open(self.params.csvOutputFilename(self.params.generations), 'a') as f:
			f.write(logHeaders)
			f.write("\n")
			f.write(self.output)
		
	def saveBestToFile(self, best):
		
		with open('./best.txt', 'w') as f:
			f.write(str(self.params.sqrtRobots))
			f.write("\n")
			f.write(str(best))
			
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

