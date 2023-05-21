
import sys
sys.path.insert(0, '..')

import matplotlib.pyplot as plt
from pathlib import Path

from scipy.stats import ttest_ind
from scipy.stats import shapiro
from scipy.stats import mannwhitneyu

import os
import numpy
import pickle

from containers import *

from deap import base, creator, tools, gp

from params import eaParams
from utilities import Utilities


class Analysis():
	
	objectives = ["density", "nest", "food", "idensity", "inest", "ifood"]
	
	def __init__(self):
		self.params = eaParams()
		self.utilities = Utilities(self.params)
		

	def setupDeapToolbox(self):
		
		self.pset = gp.PrimitiveSet("MAIN", 0)
		self.params.addNodes(self.pset)
		self.toolbox = base.Toolbox()

		weights_algorithm = (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, )
		creator.create("Fitness", base.Fitness, weights=weights_algorithm)
		creator.create("Individual", gp.PrimitiveTree, fitness=creator.Fitness, features=list)
		
		weights_objective = (1.0,)
		creator.create("Fitness_objective", base.Fitness, weights=weights_objective)
		creator.create("Individual_objective", gp.PrimitiveTree, fitness=creator.Fitness_objective, features=list)
			
		self.toolbox.register("expr_init", gp.genFull, pset=self.pset, min_=1, max_=4)
		
		self.toolbox.register("individual", tools.initIterate, creator.Individual, self.toolbox.expr_init)
		self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
		
		self.toolbox.register("individual_objective", tools.initIterate, creator.Individual_objective, self.toolbox.expr_init)
		self.toolbox.register("population_objective", tools.initRepeat, list, self.toolbox.individual_objective)
		
		self.toolbox.register("evaluate", self.utilities.evaluateRobot, thread_index=5)
		self.toolbox.register("evaluate1", self.utilities.evaluateRobot, thread_index=1)
		self.toolbox.register("evaluate2", self.utilities.evaluateRobot, thread_index=2)
		self.toolbox.register("evaluate3", self.utilities.evaluateRobot, thread_index=3)
		self.toolbox.register("evaluate4", self.utilities.evaluateRobot, thread_index=4)
	
	def getDataFromGridForCSV(self, grid, features, objective_index, csv_filename, generation): # only works for one feature and 8*8*8 bins
		
		best_individual = None
		fittest_flat = []
		# print ("")
		for idx, inds in grid.solutions.items():
			if len(inds) == 0:
				continue
			best = None
			for ind in inds:
				if best is None:
					best = ind
				elif ind.fitness.values[0] > best.fitness.values[0]:
					best = ind
			
			fittest_flat.append(best)
			
			if best_individual is None:
				best_individual = ind
			elif best.fitness.values[0] > best_individual.fitness.values[0]:
				best_individual = best
		
		qd_score = 0.0		
		for ind in fittest_flat:
			qd_score += ind.fitness.values[0]
		qd_score /= 8*8*8
		
		coverage = len(fittest_flat) / (8*8*8)
		
		string = str(generation)+","+str(best_individual.fitness.values[0])+","+str(qd_score)+","+str(coverage)
		
		print(string)
		return string
		# csv_data = str(generation)+","+str(best_individual.fitness.values[0])+","+str(qd_score)+","+str(coverage)+"\n"	

	def convertDEAPtoGridWholeRun(self, algorithm, objective_index, seed, start, generations, features, path):
		
		self.setupDeapToolbox()
		
		objective = self.objectives[objective_index]
		population_size = features * 25
		
		Path("./conversions/"+algorithm+"/"+str(seed)).mkdir(parents=False, exist_ok=True)
		
		input_path = path+algorithm+"/"+str(seed)+"/"
		output_path = "./conversions/"+algorithm+"/"+str(seed)+"/"
		csv_filename = output_path + "scores.csv" if features == 1 else output_path + objective + "-scores.csv"
		
		print(input_path)
		
		fitness_domain = [(0., numpy.inf),]
		# for i in range(1, features):
			# fitness_domain.append((0., numpy.inf))
		grid = Grid(shape = [8,8,8],
					max_items_per_bin = 1,
					fitness_domain = fitness_domain,
					features_domain = [(-40.0, 40.0), (-40.0, 40.0), (0.0, 1.0)],
					storage_type=list)
		
		csv_data = []
		for i in range(start, generations + 1):
			
			self.params.configure()
			if self.params.stop:
				generations = i - 1
				break
			
			inputFilename = input_path + "checkpoint-"+algorithm+"-"+str(seed)+"-"+str(i)+".pkl"
			# print ("# "+inputFilename)
			# print ("# "+outputFilename)
			
				
			pop = self.toolbox.population_objective(n=population_size)

			# print("# create qdpy population from deap population")
			with open(inputFilename, "rb") as checkpoint_file:
				checkpoint = pickle.load(checkpoint_file)
			population = checkpoint["population"]
			
			for j in range(population_size):
				pop[j] = creator.Individual_objective(population[j])
				
				# fitness = [population[j].fitness.values[objective_index]] # hack for old data
				fitness = [population[j].fitness.values[objective_index]] # could be this is meant to be 0 for one objective
				
				features = []
				# hack for old data
				
				# six objectives
				features.append(population[j].fitness.values[6])
				features.append(population[j].fitness.values[7])
				features.append(population[j].fitness.values[8])
				
				# for one objective
				# features.append(population[j].fitness.values[1])
				# features.append(population[j].fitness.values[2])
				# features.append(population[j].fitness.values[3])
				
				# three objectives
				# features.append(population[j].fitness.values[3])
				# features.append(population[j].fitness.values[4])
				# features.append(population[j].fitness.values[5])
				
				pop[j].fitness.values = tuple(fitness)
				pop[j].features = tuple(features)
				
				# print(population[j].fitness)
				# print(pop[j].fitness)
				# print("")
				
			self.utilities.removeDuplicates(pop, grid)
			nb_updated = grid.update(pop, issue_warning = True)
				
			csv_data.append(self.getDataFromGridForCSV(grid, features, objective_index, csv_filename, i))
		
		string = ""
		for data in csv_data:	
			string += data+"\n"
		
		print (csv_filename)
		print (output_path + self.objectives[objective_index]+"-"+str(seed)+"-"+str(generations)+".pkl")
		
		with open(csv_filename, "w") as f:
			f.write ("generation,best,qd score,coverage\n")
		with open(csv_filename, "a") as f:
			f.write(string)
		
		outputFilename = output_path + self.objectives[objective_index]+"-"+str(seed)+"-"+str(generations)+".pkl"
		with open(outputFilename, "wb") as f:
			pickle.dump(grid, f)

	def readQDpyFile(self, objective, seed, iteration): # load pkl file from qdpy run into grid
		
		inputFilename = "../../QDPY/NewDEAP/test/"+objective+"/batch-100-50/seed"+str(seed)+"-iteration"+str(iteration)+".p"
		
		with open(inputFilename, "rb") as f:
			data = pickle.load(f)
		for i in data:
			if str(i) == "container":
				container = data[i]
		
		return container

	def readConvertedFile(self, filename): # load pkl file generated from deap into grid
		
		with open(filename, "rb") as f:
			data = pickle.load(f)
		grid = data
		
		return grid

	
	def getBestFromCSV(self, generations, objective, features, filename): 
		
		# returns every generation for each feature data[feature][gen][seed]

		f = open(filename, "r")

		horizontal_data = []

		for line in f:
			
			data = []
			columns = line.split(",")
			
			if columns[0] == objective:
				for i in range(generations+1):
					fitnessList = columns[i+9]
					fitness = fitnessList.split(" ")
					if (fitness[-1] == ""):
						data.append(fitness[0:-1])
					else:
						data.append(fitness)
				horizontal_data.append(data)
		
		# print ("")
		# for d in horizontal_data:
			# print(d)
		# print ("")
		
		vertical_data = []
		for i in range(len(horizontal_data[0][0])):
			featureData = []
			for j in range(len(horizontal_data[0])):
				populationsData = []
				for k in range(len(horizontal_data)):
					populationsData.append(float(horizontal_data[k][j][i]))
				featureData.append(populationsData)
			vertical_data.append(featureData)

		# print ("")
		# print (vertical_data)
		# for d in vertical_data:
			# print (d)
		# print ("")
		
		return vertical_data

	def getBestFromPkl(self, objective, iterations, runs):

		# returns every generation data[gen][seed]
		
		horizontal_data = []
		
		for i in range(runs):
			
			scores = []
			index = i + 1
			
			file_name = "../../QDPY/NewDEAP/test/"+objective+"/batch-100-50/csvs/best-"+str(index)+".csv"
			# print(file_name)
			# if carrying_food_bug: file_name = "./test-with-broken-carrying-food-node/"+objective+"/batch-100-50/csvs/best-"+str(index)+".csv"
		
			f = open(file_name, "r")

			for line in f:
				columns = line.split(",")
				if int(columns[0]) <= iterations:
					scores.append(float(columns[1]))
			horizontal_data.append(scores)
		
		# print ("")
		# print (len(horizontal_data))
		# for d in horizontal_data:
			# print (len(d))
		# for d in horizontal_data:
			# print(d)
		# print ("")
		
		vertical_data = []
		for i in range(len(horizontal_data[0])):
			data = []
			for j in range(len(horizontal_data)):
				data.append(horizontal_data[j][i])
			vertical_data.append(data)
			
		# print ("")
		# for d in vertical_data:
			# print (d)
		# print ("")
		
		return vertical_data

	def checkHypothesis(self, data1, data2):
		
		data1_normal = shapiro(data1)
		data2_normal = shapiro(data2)
		# print(data1_normal.pvalue)
		# print(data2_normal.pvalue)
		
		both_normal = True if data1_normal.pvalue > 0.05 and data2_normal.pvalue > 0.05 else False
		
		if both_normal:
			ttest = ttest_ind(data1, data2)
			print ("ttest "+str(ttest.pvalue))
		else:
			ttest = mannwhitneyu(data1, data2)
			print ("mwu "+str(ttest.pvalue))
	
	def drawOneGeneration(self, title, filename, labels, deap_scores, qdpy_scores, generation):
		
		data = deap_scores + qdpy_scores
		# data = getFitnessComparison(deap_scores, generation)
		# data = getFitnessComparison([scores[0]], generation)
		# data.append(scores[1])
		# for score in qdpy_scores:
			# data.append(score)
		
		for d in data:
			print(len(d))
		
		if len(data) == 2: ttest = ttest_ind(data[0], data[1])
		
		if len(data) > 2:
			print ("")
			for i in range(1, len(data)):
				self.checkHypothesis(data[0], data[i])
				ttest = ttest_ind(data[0], data[i])
				# print ("pvalue = " +str("%.4f" % ttest.pvalue))
			print ("")
			
				
		
		# if carrying_food_bug: filename = "./test-with-broken-carrying-food-node/charts/best/box-plots-"+filename +"-gen"+ str(generation)+".png"
		# else: filename = "./test/charts/best/box-plots-"+filename +"-gen"+ str(generation)+".png"
		
		filename = "./best/box-plots-"+filename+".png"
		# if carrying_food_bug: filename = "./test-with-broken-carrying-food-node/charts/best/box-plots-"+filename+".png"
		# else: filename = "./test/charts/best/box-plots-"+filename+".png"
		
		# title += " - generation "+str(generation)+"\n\n"
		title += " - " + str(generation * 25)+" evaluations per objective\n"
		# title += "t-test result (statistic = "+str("%.4f" % ttest.statistic)+ ", pvalue = " +str("%.4f" % ttest.pvalue)+")\n\n"
		if len(data) == 2: title += "pvalue = " +str("%.4f" % ttest.pvalue)+"\n\n"
		
		num = -1
		consistent = True
		for d in data:
			if (num == -1): num = len(d)
			elif num != len(d): consistent = False
		
		ylabel = ""
		if consistent: ylabel = 'Fitness over '+str(len(data[0]))+' runs'
		else: ylabel = 'Mixed number of runs'
		
		plot_width = 4 + len(data)	
		
		fig, ax = plt.subplots(figsize=(plot_width, 6))
		plt.subplots_adjust(wspace=.3, hspace=1.4, bottom=0.12, top=0.85, left=0.15)
		ax.boxplot(data, medianprops=dict(color='#000000'), labels=labels)
		
		ax.set_title(title,fontsize=13)
		ax.title.set_position([0.5,-1.5])
		
		ax.set_xlabel("Algorithm", color='#222222', fontsize=12)
		ax.set_ylabel(ylabel, color='#222222', fontsize=12)
		
		ax.xaxis.set_label_coords(0.5,-0.09)
		ax.yaxis.set_label_coords(-0.12,0.5)
		
		# plt.savefig(filename)
		print(filename)
		plt.show()

	def drawOneGenerationQD(self, title, filename, labels, scores, generation):
		
		# data = getFitnessComparison([scores[0], scores[1]], generation)

		if len(scores) > 2:
			print ("")
			for i in range(1, len(scores)):
				ttest = ttest_ind(scores[0], scores[i])
				print ("pvalue = " +str("%.16f" % ttest.pvalue))
			print ("")
		
		filename = filename +".png"

		title += " - " + str(generation * 25)+" evaluations\n"
		# title += "pvalue = " +str("%.8f" % ttest.pvalue)+"\n\n"
		
		num = -1
		consistent = True
		for s in scores:
			if (num == -1): num = len(s)
			elif num != len(s): consistent = False
		
		ylabel = ""
		if consistent: ylabel = str(len(scores[0]))+' runs'
		else: ylabel = 'Mixed number of runs'
		
		fig, ax = plt.subplots(figsize=(6, 6))
		plt.subplots_adjust(wspace=.3, hspace=1.4, bottom=0.1, top=0.9, left=0.2)
		ax.boxplot(scores, medianprops=dict(color='#000000'), labels=labels)
		ax.set_title(title,fontsize=13)
		ax.title.set_position([0.5,2.0])
		ax.set_ylabel(ylabel,color='#222222', fontsize=12)
		ax.yaxis.set_label_coords(-0.16,0.5)
		print(filename)
		# plt.savefig(filename)

	def bestIndividuals(self):

		
		generation = 1000

		deap_density = self.getBestFromCSV(generation, "density", 1, "../../Backups/AutoDecomposition/density/combined1000.csv")
		deap_nest = self.getBestFromCSV(generation, "nest", 1, "../../Backups/AutoDecomposition/nest/combined1000.csv")
		deap_food = self.getBestFromCSV(generation, "food", 1, "../../Backups/AutoDecomposition/food/combined1000.csv")
		deap_idensity = self.getBestFromCSV(generation, "idensity", 1, "../AutoDecomposition/test/idensity/checkpoint1000.csv")
		deap_inest = self.getBestFromCSV(generation, "inest", 1, "../AutoDecomposition/test/inest/checkpoint1000.csv")
		deap_ifood = self.getBestFromCSV(generation, "ifood", 1, "../AutoDecomposition/test/ifood/checkpoint1000.csv")
		# deap_density = self.getBestFromCSV(generation, "density", 1, "../../AutoDecomposition/checkpoints/test/density/combined1000.csv")
		# deap_nest = self.getBestFromCSV(generation, "nest", 1, "../../AutoDecomposition/checkpoints/test/nest/combined1000.csv")
		# deap_food = self.getBestFromCSV(generation, "food", 1, "../../AutoDecomposition/checkpoints/test/food/combined1000.csv")
		# deap_idensity = self.getBestFromCSV(generation, "idensity", 1, "../Extended/test/idensity/checkpoint1000.csv")
		# deap_inest = self.getBestFromCSV(generation, "inest", 1, "../Extended/test/inest-with-archive/checkpoint1000.csv")
		# deap_ifood = self.getBestFromCSV(generation, "ifood", 1, "../Extended/test/ifood-with-archive/checkpoint1000.csv")
		
		# deap_three = self.getBestFromCSV(generation, "density-nest-food", 3, "../../AutoDecomposition/checkpoints/test/density-nest-food/combined1000.csv")
		# deap_six = self.getBestFromCSV(generation, "density-nest-food-idensity-inest-ifood", 6, "../Extended/test/density-nest-food-idensity-inest-ifood/combined1000.csv")
		
		# qdpy_density = self.getBestFromPkl("density", 500, 10)
		# qdpy_nest = self.getBestFromPkl("nest", 500, 10)
		# qdpy_food = self.getBestFromPkl("food", 500, 10)
		
		derated_density = self.getBestFromCSV(generation, "density", 1, "../AutoDecomposition/test/density/checkpoint1000.csv")
		derated_nest = self.getBestFromCSV(generation, "nest", 1, "../AutoDecomposition/test/nest/checkpoint1000.csv")
		derated_food = self.getBestFromCSV(generation, "food", 1, "../AutoDecomposition/test/food/checkpoint1000.csv")
		
		derated_idensity = self.getBestFromCSV(generation, "idensity", 1, "../AutoDecomposition/test/idensity/checkpoint1000.csv")
		derated_inest = self.getBestFromCSV(generation, "inest", 1, "../AutoDecomposition/test/inest/checkpoint1000.csv")
		derated_ifood = self.getBestFromCSV(generation, "ifood", 1, "../AutoDecomposition/test/ifood/checkpoint1000.csv")
		
		# self.drawOneGeneration('Increase density', 'density-vs-derated', ['$GP_d$', 'derated $GP_d$'], [deap_density[0][generation], derated_density[0][generation]], [], generation)
		# self.drawOneGeneration('Go to nest', 'nest-vs-derated', ['$GP_n$', 'derated $GP_n$'], [deap_nest[0][generation], derated_nest[0][generation]], [], generation)
		# self.drawOneGeneration('Go to food', 'food-vs-derated', ['$GP_f$', 'derated $GP_f$'], [deap_food[0][generation], derated_food[0][generation]], [], generation)
		self.drawOneGeneration('Decrease density', 'idensity-vs-derated', ['$GP_id$', 'derated $GP_id$'], [deap_idensity[0][generation], derated_idensity[0][generation]], [], generation)
		# self.drawOneGeneration('Go away from nest', 'inest-vs-derated', ['$GP_in$', 'derated $GP_in$'], [deap_inest[0][generation], derated_inest[0][generation]], [], generation)
		# self.drawOneGeneration('Go away from food', 'ifood-vs-derated', ['$GP_if$', 'derated $GP_if$'], [deap_ifood[0][generation], derated_ifood[0][generation]], [], generation)
		# self.drawOneGeneration('Increase density', 'density', ['$GP_d$', '$GP_{f,n,d}$', '$GP_{i,f,n,d}$', '$QD_d$'], [deap_density[0][generation], deap_three[0][generation], deap_six[0][generation]], [qdpy_density[int(generation/2)-1]], generation)
		# self.drawOneGeneration('Go to nest', 'nest', ['$GP_n$', '$GP_{f,n,d}$', '$GP_{i,f,n,d}$', '$QD_n$'], [deap_nest[0][generation], deap_three[1][generation], deap_six[1][generation]], [qdpy_nest[int(generation/2)-1]], generation)
		# self.drawOneGeneration('Go to food', 'food', ['$GP_f$', '$GP_{f,n,d}$', '$GP_{i,f,n,d}$', '$QD_f$'], [deap_food[0][generation], deap_three[2][generation], deap_six[2][generation]], [qdpy_food[int(generation/2)-1]], generation)
		# self.drawOneGeneration('Reduce density', 'idensity', ['$GP_id$', '$GP_{i,f,n,d}$'], [deap_idensity[0][generation], deap_six[3][generation]], [], generation)
		# self.drawOneGeneration('Go away from nest', 'inest', ['$GP_in$', '$GP_{i,f,n,d}$'], [deap_inest[0][generation], deap_six[4][generation]], [], generation)
		# self.drawOneGeneration('Go away from food', 'ifood', ['$GP_if$', '$GP_{i,f,n,d}$'], [deap_ifood[0][generation], deap_six[5][generation]], [], generation)
		return
		
		print("")


	def getCoverage(self, container): # ratio of filled vs empty bins
		
		""" get the ratio of filled vs empty bins, returns a value between 0 and 1"""
		
		filled_bins = 0.0
		for i in range(len(container.nb_items_per_bin)):
			for j in range(len(container.nb_items_per_bin[i])):
				for k in range(len(container.nb_items_per_bin[i][j])):
					if container.nb_items_per_bin[i][j][k] > 0:
						filled_bins += 1
		filled_bins /= 8*8*8
		# print(container.nb_items_per_bin)
		return filled_bins

	def drawCoverageGraph(self, objective, objective_name, is_old_data):
		
		self.setupDeapToolbox()
		
		scores = []
		
		is_qdpy = False
		generations = 1000
		scores.append(self.combineCoverage(objective, objective, generations, is_qdpy, is_old_data))
		# scores.append(self.combineCoverage("density-nest-food", objective, generations, is_qdpy, True))
		scores.append(self.combineCoverage("density-nest-food-idensity-inest-ifood", objective, generations, is_qdpy, False))
		
		is_qdpy = True
		generations = 500
		# scores.append(self.combineCoverage(objective, objective, generations, is_qdpy, True))
		# scores.append(combineCoverage("density-nest-food", generations, is_qdpy))

		title = 'Grid coverage ('+objective_name+')'
		filename = './coverage/box-plots-'+objective
		labels = ['DEAP\nBenchmark', 'DEAP\n3 objectives', 'DEAP\n6 objectives', 'QDPY\n1 objective']
		labels = ['DEAP\nBenchmark', 'DEAP\n6 objectives']
		generation = 1000
		self.drawOneGenerationQD(title, filename, labels, scores, generation)

	def combineCoverage(self, algorithm, objective, iteration, is_qdpy, is_old_data): # coverage for several runs
		
		scores = []
		
		if is_qdpy:
			for i in range(12):
				seed = i + 1
				scores.append(self.getCoverage(self.readQDpyFile(objective, seed, iteration)))
		else:
			if is_old_data:
				for i in range(12):
					seed = i + 9
					if seed == 16: continue
					filename = "./conversions/"+algorithm+"/"+str(seed)+"/"+objective+"-"+str(seed)+"-"+str(iteration)+".pkl"
					scores.append(self.getCoverage(self.readConvertedFile(filename)))
			else:
				for i in range(10):
					seed = i + 1
					filename = "./conversions/"+algorithm+"/"+str(seed)+"/"+objective+"-"+str(seed)+"-"+str(iteration)+".pkl"
					scores.append(self.getCoverage(self.readConvertedFile(filename)))
		
		return scores



	def getQDScore(self, grid, features, objective, objective_index): # sum fitnesses of all individuals
		
		"""sums the fitnesses of every individual in the grid and divides by the maximum possible number of individuals"""
		
		fittest_flat = []
		for idx, inds in grid.solutions.items():
			if len(inds) == 0:
				continue
			best = None
			for ind in inds:
				if best is None:
					best = ind
				elif ind.fitness.values[0] > best.fitness.values[0]:
					best = ind
			
			fittest_flat.append(best)
			
		qd_score = 0.0		
		for ind in fittest_flat:
			qd_score += ind.fitness.values[0]
		qd_score /= 8*8*8
		
		return qd_score
		
		best_individual = None
		fittest_flat = []
		for idx, inds in container.solutions.items():
			if len(inds) == 0:
				continue
			best = None
			for ind in inds:
				if best is None:
					best = ind
				elif ind.fitness.values[0] > best.fitness.values[0]:
					best = ind
			if features > 1:
				print("not implemented")
			fittest_flat.append(best)
			if best_individual is None:
				best_individual = ind
			elif best.fitness.values[0] > best_individual.fitness.values[0]:
				best_individual = best
		
		qd_score = 0.0		
		for ind in fittest_flat:
			qd_score += ind.fitness.values[0]
		qd_score /= 8*8*8
		
		return qd_score

	def combineQDScores(self, algorithm, objective, objective_index, features, iteration, is_qdpy, is_old_data): # collects the scores for several runs
		
		scores = []
		
		if is_qdpy:
			for i in range(12):
				seed = i + 1
				scores.append(self.getQDScore(self.readQDpyFile(objective, seed, iteration), 1, objective, objective_index))
		else:
			if is_old_data:
				for i in range(12):
					seed = i + 9
					if seed == 16: continue
					filename = "./conversions/"+algorithm+"/"+str(seed)+"/"+objective+"-"+str(seed)+"-"+str(iteration)+".pkl"
					scores.append(self.getQDScore(self.readConvertedFile(filename), features, objective, objective_index))
			else:
				for i in range(10):
					seed = i + 1
					filename = "./conversions/"+algorithm+"/"+str(seed)+"/"+objective+"-"+str(seed)+"-"+str(iteration)+".pkl"
					scores.append(self.getQDScore(self.readConvertedFile(filename), features, objective, objective_index))
		
		return scores

	def drawQDScoresGraph(self, objective_index, objective, objective_name, is_old_data):
		
		self.setupDeapToolbox()
		
		scores = []
		
		is_qdpy = False
		generations = 1000
		scores.append(self.combineQDScores(objective, objective, objective_index, 1, generations, is_qdpy, is_old_data))
		# scores.append(self.combineQDScores("density-nest-food", objective, objective_index, 3, generations, is_qdpy, True))
		scores.append(self.combineQDScores("density-nest-food-idensity-inest-ifood", objective, objective_index, 6, generations, is_qdpy, False))
		
		is_qdpy = True
		generations = 500
		# scores.append(self.combineQDScores(objective, objective, objective_index, 1, generations, is_qdpy, True))

		title = 'QD scores ('+objective_name+')'
		filename = './qd-scores/box-plots-'+objective
		labels = ['DEAP\nBenchmark', 'DEAP\n3 objectives', 'DEAP\n6 objectives', 'QDPY\n1 objective']
		labels = ['DEAP\nBenchmark', 'DEAP\n6 objectives']
		generation = 1000
		self.drawOneGenerationQD(title, filename, labels, scores, generation)
		
		return
		
		scores = []

		is_qdpy = False
		generations = 1000
		scores.append(combineQDScores(objective, objective_index, 1, generations, is_qdpy))
		# scores.append(combineQDScores("density-nest-food", objective_index, 3, generations, is_qdpy))

		is_qdpy = True
		generations = 500
		scores.append(combineQDScores(objective, objective_index, 1, generations, is_qdpy))

		title = 'QD scores ('+objective_name+')'
		filename = 'charts/qd-scores/box-plots-'+objective
		labels = ['EA1'+suffix, 'EA2', 'QD1'+suffix]
		generation = 1000
		drawOneGeneration(title, filename, labels, scores, generation)
	


	def getArchiveSizes(self):
		
		for i in range(10):
			print(os.path.getsize("../AutoDecomposition/test/density/"+str(i+1)+"/archive.pkl"))

