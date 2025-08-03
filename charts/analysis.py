
import sys
sys.path.insert(0, '..')

import matplotlib.pyplot as plt
# from pathlib import Path

from scipy.stats import ttest_ind
from scipy.stats import shapiro
from scipy.stats import mannwhitneyu
import statistics

# import os
# import numpy
import pickle

# from containers import *

from deap import base, creator, tools, gp

from params import eaParams
from utilities import Utilities
import local


class Analysis():
	
	objectives = ["density", "nest", "food", "idensity", "inest", "ifood"]
	objective_descriptions = ["Increase robot density", "Go to nest", "Go to food", "Reduce robot density", "Go away from nest", "Go away from food"]
	
	objectives_info = {
		"density" : {
			"name" : "density",
			"description" : "Increase neighbourhood density",
			"index" : 0,
			"identifier" : "d",
			"gp_url" : "../gp/results/density/",
			"qdpy_url": "../qdpy/test/density/",
			"mtc_url" : "../gp/results/density-nest-ifood/",
			"mti_url" : "../gp/results/density-nest-food/",
		},
		"nest" : {
			"name" : "nest",
			"description" : "Go to nest",
			"index" : 1,
			"identifier" : "n",
			"gp_url" : "../gp/results/nest/",
			"qdpy_url": "../qdpy/test/nest/",
			"mtc_url" : "../gp/results/density-nest-ifood/",
			"mti_url" : "../gp/results/density-nest-food/",
		},
		"food" : {
			"name" : "food",
			"description" : "Go to food",
			"index" : 2,
			"identifier" : "f",
			"gp_url" : "../gp/results/food/",
			"qdpy_url": "../qdpy/test/food/",
			"mtc_url" : "../gp/results/food-idensity-inest/",
			"mti_url" : "../gp/results/density-nest-food/",
		},
		"idensity" : {
			"name" : "idensity",
			"description" : "Reduce density",
			"index" : 3,
			"identifier" : "id",
			"gp_url" : "../gp/results/idensity/",
			"qdpy_url": "../qdpy/test/idensity/",
			"mtc_url": "../gp/results/food-idensity-inest/",
			"mti_url" : "../gp/results/idensity-inest-ifood/",
		},
		"inest" : {
			"name" : "inest",
			"description" : "Go away from nest",
			"index" : 4,
			"identifier" : "in",
			"gp_url" : "../gp/results/inest/",
			"qdpy_url": "../qdpy/test/inest/",
			"mtc_url": "../gp/results/food-idensity-inest/",
			"mti_url" : "../gp/results/idensity-inest-ifood/",
		},
		"ifood" : {
			"name" : "ifood",
			"description" : "Go away from food",
			"index" : 5,
			"identifier" : "if",
			"gp_url": "../gp/results/ifood/",
			"qdpy_url": "../qdpy/test/ifood/",
			"mtc_url": "../gp/results/density-nest-ifood/",
			"mti_url": "../gp/results/idensity-inest-ifood/",
		},
		"density-nest-food" : {
			"name" : "density-nest-food",
			"names" : ["density","nest","food"],
			"description" : ["Increase neighbourhood density", "Go to nest", "Go to food"],
			"mt_url": "../gp/test/density-nest-food/",
		},
		"foraging" : {
			"name" : "foraging",
			"description" : "Foraging",
			"identifier" : "",
			"foraging_baseline_url": "../gp/results/foraging/baseline/",
			"foraging_qd1_url": "../gp/results/foraging/repertoire-qd1-1000gen/",
			"foraging_qd8_url": "../gp/results/foraging/repertoire-qd8-1000gen/",
			"foraging_mt1_url": "../gp/results/foraging/repertoire-mt1-1000gen/",
			"foraging_mt8_url": "../gp/results/foraging/repertoire-mt8-1000gen/",
		},
	}

	algorithms = {
		"gp" : {
			"name" : "gp",
			"display_name" : "GP",
			"type" : "DEAP",
			"code" : "GP",
			"prefix" : "",
			"categories" : ["EA1a", "EA1b", "EA1c"],
			"ylim" : [[0.5, 0.61], [0.6, 0.9], [0.7, 0.9]], # box plots only
		},
		"non_derated_baseline" : {
			"name" : "non_derated_baseline",
			"display_name" : "Baseline",
			"type" : "DEAP",
			"code" : "GP_",
			"prefix" : "Baseline ",
			"categories" : ["EA1a", "EA1b", "EA1c"],
			"ylim" : [[0.5, 0.61], [0.6, 0.9], [0.7, 0.9]],
		},
		"non_derated_qdpy" : {
			"name" : "non_derated_qdpy",
			"type" : "QDPY",
			"code" : "QD_",
			"prefix" : "Non Derated ",
			"categories" : ["QD1a", "QD1b", "QD1c"],
			"ylim" : [[0.5, 0.61], [0.6, 0.9], [0.7, 0.88]],
		},
		"qdpy" : {
			"name" : "qdpy",
			"display_name" : "QDpy",
			"type" : "QDPY",
			"code" : "QD",
			"prefix" : "",
			"categories" : ["QD1a", "QD1b", "QD1c"],
			"ylim" : [[0.5, 0.6], [0.6, 0.9], [0.825, 0.88]],
		},
		"qdpy_50" : {
			"name" : "qdpy_50",
			"display_name" : "QDpy 50",
			"type" : "QDPY",
			"code" : "QD_",
			"prefix" : "Derated 50 ",
			"categories" : ["QD1a", "QD1b", "QD1c"],
			"ylim" : [[0.5, 0.6], [0.6, 0.9], [0.7, 0.9]],
		},
		"qdpy_25" : {
			"name" : "qdpy_25",
			"display_name" : "QDpy 25",
			"type" : "QDPY",
			"code" : "QD_",
			"prefix" : "Derated 25 ",
			"categories" : ["QD1a", "QD1b", "QD1c"],
			"ylim" : [[0.5, 0.6], [0.6, 0.9], [0.7, 0.9]],
		},
		"mt" : {
			"name" : "mtc",
			"display_name" : "Multi-Task",
			"type" : "MTC",
			"code" : "MTC_",
			"prefix" : "",
			# "categories" : ["QD1a", "QD1b", "QD1c"],
			"ylim" : [[0.5, 0.6], [0.6, 0.9], [0.825, 0.88]],
		},
		"mtc" : {
			"name" : "mtc",
			"display_name" : "Multi-Task Compatible",
			"type" : "MTC",
			"code" : "MTC",
			"prefix" : "",
			# "categories" : ["QD1a", "QD1b", "QD1c"],
			"ylim" : [[0.5, 0.6], [0.6, 0.9], [0.825, 0.88]],
		},
		"mti" : {
			"name" : "mti",
			"display_name" : "Multi-Task Incompatible",
			"type" : "MTI",
			"code" : "MTI",
			"prefix" : "",
			# "categories" : ["QD1a", "QD1b", "QD1c"],
			"ylim" : [[0.5, 0.6], [0.6, 0.9], [0.825, 0.88]],
		},
		"foraging_old_derating_baseline" : {
			"name" : "foraging_old_derating_baseline",
			"display_name" : "Baseline",
			"type" : "GP",
			"code" : "GP",
			"prefix" : "",
			"ylim" : [[0.5, 0.6], [0.6, 0.9], [0.825, 0.88]],
		},
		"foraging_old_derating_modular" : {
			"name" : "foraging_old_derating_modular",
			"display_name" : "Modular",
			"type" : "AM",
			"code" : "AM",
			"prefix" : "",
			"ylim" : [[0.5, 0.6], [0.6, 0.9], [0.825, 0.88]],
		},
		"foraging_baseline" : {
			"name" : "foraging_baseline",
			"display_name" : "Baseline",
			"type" : "Baseline",
			"code" : "Baseline",
			"prefix" : "",
			"ylim" : [[0.5, 0.6], [0.6, 0.9], [0.825, 0.88]],
			"generations" : 2200,
			"file_index" : 2500,
		},
		"foraging_qd1" : {
			"name" : "foraging_qd1",
			"display_name" : "QD Repertoire 1",
			"type" : "QD Repertoire 1",
			"code" : "QD1",
			"prefix" : "",
			"ylim" : [[0.5, 0.6], [0.6, 0.9], [0.825, 0.88]],
			"generations" : 1000,
			"file_index" : 1000,
		},
		"foraging_qd8" : {
			"name" : "foraging_qd8",
			"display_name" : "QD Repertoire 8",
			"type" : "QD Repertoire 8",
			"code" : "QD8",
			"prefix" : "",
			"ylim" : [[0.5, 0.6], [0.6, 0.9], [0.825, 0.88]],
			"generations" : 1000,
			"file_index" : 1000,
		},
		"foraging_mt1" : {
			"name" : "foraging_mt1",
			"display_name" : "MT Repertoire 1",
			"type" : "MT Repertoire 1",
			"code" : "MT1",
			"prefix" : "",
			"ylim" : [[0.5, 0.6], [0.6, 0.9], [0.825, 0.88]],
			"generations" : 1000,
			"file_index" : 1000,
		},
		"foraging_mt8" : {
			"name" : "foraging_mt8",
			"display_name" : "MT Repertoire 8",
			"type" : "MT Repertoire 8",
			"code" : "MT8",
			"prefix" : "",
			"ylim" : [[0.5, 0.6], [0.6, 0.9], [0.825, 0.88]],
			"generations" : 1000,
			"file_index" : 1000,
		},
	}

	queries = {
		"best" : {
			"name" : "best",
			"description" : "best individuals",
			"ylabel" : "Best fitness",
			"index" : 1,
			"ylim" : [[0.52, 0.61], [0.6, 0.9], [0.83, 0.88]],
		},
		"qd-score" : {
			"name" : "qd-scores",
			"description" : "QD scores",
			"ylabel" : "QD score",
			"index" : 2,
		},
		"coverage" : {
			"name" : "coverage",
			"description" : "coverage",
			"ylabel" : "Coverage",
			"index" : 3,
		}
	}

	def __init__(self):
		self.params = eaParams()
		self.utilities = Utilities(self.params)
		

	def setupDeapToolbox(self):
		
		self.pset = local.PrimitiveSetExtended("MAIN", 0)
		self.params.addUnpackedNodes(self.pset)
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
		
		inputFilename = objective["qdpy_url"]+str(seed)+"/seed"+str(seed)+"-iteration"+str(iteration)+".p"
		
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

	def getBestData(self, deap_algorithms, qdpy_algorithms, objective, generation, feature, features, runs, mtc_index, mti_index):

		# hard coded for one or three features

		deap = []
		for algorithm in deap_algorithms:

			features = 3 if "mt" in algorithm["name"] else 1

			if "foraging" in algorithm["name"]: generation = algorithm["generations"]

			if "foraging" in algorithm["name"]:
				file_index = algorithm["file_index"]
			else:
				file_index = generation

			if "mti" in algorithm["name"]: feature = mti_index
			if "mtc" in algorithm["name"]: feature = mtc_index

			data = self.getBestFromCSV(file_index, generation, objective, features, runs, objective[algorithm["name"]+"_url"])
			data = data[feature][generation] if "mt" in algorithm["name"]  else data[0][generation]
			deap.append(data)

		features = 1
		qdpy = []
		for algorithm in qdpy_algorithms:
			data = self.getBestFromPkl(features, objective, generation, 10, objective[algorithm["name"]+"_url"])
			# data = data[int(generation)-1]
			qdpy.append(data)

		# quick hack so we can get 1000 gens for batch 50 and 2000 gens for batch 25
		# qdpy = []
		# algorithm = qdpy_algorithms[0]
		# data = self.getBestFromQdpyCsvs(objective, generation, 10, objective[algorithm["name"]+"_url"])
		# data = data[int(generation)-1]
		# qdpy.append(data)
		# algorithm = qdpy_algorithms[1]
		# data = self.getBestFromQdpyCsvs(objective, generation*2, 10, objective[algorithm["name"]+"_url"])
		# data = data[int(generation*2)-1]
		# qdpy.append(data)

		return deap + qdpy
	
	def getBestFromCSV(self, file_index, generations, objective, features, runs, filename):
		
		# needs to be made dynamic - currently hard coded for density-nest-food
		# returns every generation for each feature data[feature][gen][seed]

		if features == 1:
			objective_definition = objective["name"]
		else:
			objective_definition = ""
			for i in range(features):
				index = i + 1
				objective_definition += self.objectives[i]+"-"
			objective_definition = objective_definition[0:-1]
			objective_definition = "density-nest-ifood"

		filename = filename + "checkpoint"+str(file_index)+".csv"
		f = open(filename, "r")

		horizontal_data = []

		for line in f:
			
			data = []
			columns = line.split(",")

			if columns[0] != "Type":
				for i in range(generations+1):
					fitnessList = columns[i+9]
					fitness = fitnessList.split(" ")
					if (fitness[-1] == ""):
						data.append(fitness[0:-1])
					else:
						data.append(fitness)
				if len(horizontal_data) < runs:
					horizontal_data.append(data)
		
		# print ("")
		# print(len(horizontal_data))
		# print(len(horizontal_data[0]))
		# print(len(horizontal_data[0][0]))
		# for data in horizontal_data:
			# for d in data:
				# print(data[-1])
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
		# for d in vertical_data:
			# print (d[-1])
		# print ("")

		return vertical_data

	def getBestFromQdpyCsvs(self, objective, iterations, runs, url):

		# returns every generation data[gen][seed]
		
		horizontal_data = []
		
		for i in range(runs):
			
			scores = []
			index = i + 1
			
			file_name = url+str(index)+"/csvs/best-"+str(index)+".csv"
			# print(file_name)

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
		# for d in horizontal_data:
			# print (d[-1])
		# print ("")
		
		vertical_data = self.rotateData2D(horizontal_data)
			
		return vertical_data

	def getBestFromPkl(self, features, objective, iterations, runs, url):

		self.setupDeapToolbox()

		best = []
		for i in range(runs):

			index = i + 1
			filename = objective["qdpy_url"]+str(index)+"/seed"+str(index)+"-iteration"+str(iterations)+".p"
			container = self.readQDpyFile(objective, index, iterations)
			best.append(container.best.fitness.values[0])
			# print(container.best.fitness.values[0])

		return best

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

		return ttest

	def drawBestOneGeneration(self, feature_index, objective_name, deap_algorithms, qdpy_algorithms, generation, features, runs, mtc_index, mti_index):
		
		objective = self.objectives_info[objective_name]
		data = self.getBestData(deap_algorithms, qdpy_algorithms, objective, generation, feature_index, features, runs, mtc_index, mti_index)
		
		# for d in data:
			# print(len(d))
		
		if len(data) == 2: ttest = self.checkHypothesis(data[0], data[1])
		
		if len(data) > 2:
			print ("")
			for i in range(1, len(data)):
				self.checkHypothesis(data[0], data[i])
				ttest = ttest_ind(data[0], data[i])
			print ("")

		filename = ""
		for algorithm in deap_algorithms + qdpy_algorithms:
			filename += algorithm["name"]+"-vs-"
		filename = filename[0:-4]
		if "foraging" not in algorithm["name"]: filename = "./best/gen"+str(generation)+"/"+objective["name"]+"-"+filename+".png"
		else: filename = "./best/foraging/"+filename+".png"
		
		title = objective["description"]+"\n"
		if "foraging" not in algorithm["name"]: title += str(generation * 25)+" evaluations per objective\n"
		# if len(data) == 2: title += "pvalue = " +str("%.4f" % ttest.pvalue)+"\n\n"
		# if len(data) == 2: print("pvalue = " +str("%.4f" % ttest.pvalue))
		
		labels = []
		for algorithm in deap_algorithms + qdpy_algorithms:
			label = self.algorithmName(algorithm, objective)
			if "foraging" in algorithm["name"]:
				generation = algorithm["generations"]
				label += "\n("+str(generation)+" generations)\n"
			labels.append(label)

		num = -1
		consistent = True
		for d in data:
			if (num == -1): num = len(d)
			elif num != len(d): consistent = False
		
		ylabel = ""
		if consistent: ylabel = 'Fitness over '+str(len(data[0]))+' runs'
		else: ylabel = 'Mixed number of runs'
		
		self.drawPlotsBigLabels(data, title, labels, ylabel, "foraging" in algorithm["name"], len(deap_algorithms) == 3, filename)

	def drawPlotsForaging(self, data, title, labels, ylabel, foraging, mt, filename):

		plot_width = 8 + len(data)

		fig, ax = plt.subplots(figsize=(plot_width, 6))
		plt.subplots_adjust(wspace=.3, hspace=0.4, bottom=0.1, top=0.98, left=0.1)

		plots = ax.boxplot(data, medianprops=dict(color='#000000'), patch_artist=True, labels=labels)

		for patch in plots['boxes']:
			patch.set_facecolor('#eef6ff')

		ax.set_ylabel(ylabel, color='#222222', fontsize=17)

		ax.xaxis.set_label_coords(0.5,-.125)
		ax.yaxis.set_label_coords(-0.08,0.5)

		ax.tick_params(axis='x', labelsize=14)
		ax.tick_params(axis='y', labelsize=14)

		# plt.savefig(filename)
		print(filename)
		plt.show()

	def drawPlotsBigLabels(self, data, title, labels, ylabel, foraging, mt, filename):

		plot_width = 4 + len(data)	
		
		fig, ax = plt.subplots(figsize=(plot_width, 6))
		plt.subplots_adjust(wspace=.3, hspace=0.4, bottom=0.1, top=0.98, left=0.15)
		
		plots = ax.boxplot(data, medianprops=dict(color='#000000'), patch_artist=True, labels=labels)
		
		if len(data) == 4: colors = ['white', 'pink', 'lightblue', 'white']
		if len(data) == 3: colors = ['white', 'pink', 'white']
		if len(data) == 3 or len(data) == 4:
			for patch, color in zip(plots['boxes'], colors):
				patch.set_facecolor(color)
		else:
			for patch in plots['boxes']:
				patch.set_facecolor('white')

		ax.set_ylabel(ylabel, color='#222222', fontsize=15)
		
		if foraging:
			ax.xaxis.set_label_coords(0.5,-.125)
		else:
			ax.xaxis.set_label_coords(0.5,-0.09)
		
		ax.yaxis.set_label_coords(-0.15,0.5)

		ax.tick_params(axis='x', labelsize=15)
		ax.tick_params(axis='y', labelsize=14)

		plt.savefig(filename)
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

	"""
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
		
		# qdpy_density = self.getBestFromQdpyCsvs("density", 500, 10)
		# qdpy_nest = self.getBestFromQdpyCsvs("nest", 500, 10)
		# qdpy_food = self.getBestFromQdpyCsvs("food", 500, 10)
		
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
	"""

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


	# from mpl.py for drawing box plots over time for one algorithm
	"""
	def drawPlotsOverTime(self, plots, objective_index, min_gen, max_gen, increment, x_axis_increment):

		deap = []
		if plots["type"] == "DEAP":
			deap_data = plots["data"][objective_index]
			for i in range(len(deap_data)):
				deap.append([])
				for j in range(min_gen, max_gen+1):
					if (j % increment == 0):
						deap[i].append(deap_data[i][j])

		qdpy = []
		if plots["type"] == "QDPY":
			qdpy_data = plots["data"][objective_index]
			for i in range(len(qdpy_data)):
				qdpy.append([])
				for j in range(len(qdpy_data[i])):
					if (j % increment == 0):
						qdpy[i].append(qdpy_data[i][j])

		data = []
		for d in deap: data.append(d)
		for q in qdpy: data.append(q)

		labels = []
		for i in range(len(data[0])):
			if (i + 1) % x_axis_increment == 0:
				labels.append((i+1)*increment)
			else:
				labels.append("")

		if plots["type"] == "QDPY": max_gen *= 2

		c = "#222222"
		filename = "./test/charts/best/evolution-"+plots["names"][objective_index]+"-"+str(min_gen)+"-"+str(max_gen)+"-"+str(increment)+"-"+plots["file_name"]+".png"
		# if carrying_food_bug: filename = "./test-with-broken-carrying-food-node/charts/best/evolution-"+plots["names"][objective_index]+"-"+str(min_gen)+"-"+str(max_gen)+"-"+str(increment)+"-"+plots["file_name"]+".png"
		print (filename)

		plot_width = len(data[0]) / 5
		fig, ax = plt.subplots(nrows=1, ncols=len(data), figsize=(plot_width, 6))
		plt.subplots_adjust(wspace=.3, hspace=.4, bottom=0.1, top=0.8)
		fig.suptitle(plots["descriptions"][objective_index], y=.925, fontsize=16, color='#333333')

		bplot = []
		for col in range(0,len(data)):
			i = col
			if (len(data) > 1):
				bplot.append(ax[i].boxplot(data[i],
									vert=True,  # vertical box alignment
									patch_artist=False,  # fill with color
									labels=labels,  # will be used to label x-ticks
									boxprops=dict(color=c),
									# boxprops=dict(facecolor=c, color=c),
									capprops=dict(color=c),
									whiskerprops=dict(color=c),
									flierprops=dict(color=c, markeredgecolor=c),
									medianprops=dict(color=c)))

				ax[i].set_title(plots["algorithm_names"][objective_index], color='#222222', fontsize=13)
				ax[i].title.set_position([0.5,1.05])
				# ax[i].yaxis.grid(True)
				ax[i].set_ylim(plots["ylim"][objective_index])
				ax[i].set_ylabel('Fitness over 20 runs', color='#222222', fontsize=12)
				ax[i].yaxis.set_label_coords(-0.14,0.5)
				ax[i].xaxis.set_label_coords(0.5, -0.1)
			else:
				print (str(len(data[i])))
				print (str(len(labels)))
				bplot.append(ax.boxplot(data[i],
							 vert=True,  # vertical box alignment
							 patch_artist=False,  # fill with color
							 labels=labels,  # will be used to label x-ticks
							 boxprops=dict(color=c),
							 # boxprops=dict(facecolor=c, color=c),
							 capprops=dict(color=c),
							 whiskerprops=dict(color=c),
							 flierprops=dict(color=c, markeredgecolor=c),
							 medianprops=dict(color=c)))

				ax.set_title(plots["algorithm_names"][objective_index], color='#222222', fontsize=13)
				ax.title.set_position([0.5,1.05])
				# ax.yaxis.grid(True)
				ax.set_ylim(plots["ylim"][objective_index])
				ax.set_ylabel('Fitness over '+str(len(data[i][0]))+' runs', color='#222222', fontsize=12)
				ax.yaxis.set_label_coords(-0.09,0.5)
				ax.xaxis.set_label_coords(0.5, -0.1)

		plt.show()
	"""
	def drawEvolution(self, algorithm, objective_name, runs, min_gen, max_gen, increment, x_axis_increment):

		objective = self.objectives_info[objective_name]
		url = objective[algorithm["name"]+"_url"]

		raw_data = None

		if algorithm["type"] == "QDPY":
			raw_data = self.getBestFromQdpyCsvs(objective_name, max_gen, runs, url)
		else:
			features = 3 if algorithm["type"] == "MT" else 1
			raw_data = self.getBestFromCSV(max_gen, max_gen, objective, features, runs, url)
			raw_data = raw_data[objective["index"]] if algorithm["type"] == "MT" else raw_data[0]

		data = []
		for i in range(len(raw_data)):
			if (i >= min_gen and i <= max_gen and i % increment == 0):
				one_generation = []
				for j in range(len(raw_data[i])):
					one_generation.append(raw_data[i][j])
				data.append(one_generation)

		labels = []
		for i in range(len(data)):
			gen = min_gen + (i * increment)
			if gen % x_axis_increment == 0:
				labels.append(gen)
			else:
				labels.append("")

		title = objective["description"]+" - "+algorithm["display_name"]+" algorithm"

		settings = str(min_gen)+"-"+str(max_gen)+"-"+str(increment)
		filename = "./evolution/"+settings+"/"+objective_name+"-"+algorithm["name"]+"-"+settings+".png"
		print (filename)

		fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 6))
		plt.subplots_adjust(wspace=.3, hspace=.4, bottom=0.1, top=0.8)
		fig.suptitle(title, y=.925, fontsize=16, color='#333333')

		c = "#222222"
		ax.boxplot(data,
				   vert=True,
				   patch_artist=False,
				   labels=labels,
				   boxprops=dict(color=c),
				   # boxprops=dict(facecolor=c, color=c),
				   capprops=dict(color=c),
				   whiskerprops=dict(color=c),
				   flierprops=dict(color=c, markeredgecolor=c),
				   medianprops=dict(color=c))

		ax.title.set_position([0.5,1.05])
		# ax.yaxis.grid(True)
		ax.set_ylim(self.queries["best"]["ylim"][objective["index"]])
		ax.set_ylabel('Fitness over '+str(len(data[0]))+' runs', color=c, fontsize=12)
		ax.set_xlabel('Generations', color=c, fontsize=12)
		ax.yaxis.set_label_coords(-0.09,0.5)
		ax.xaxis.set_label_coords(0.5, -0.1)

		# plt.savefig(filename)
		plt.show()



	def rotateData2D(self, csv_data):
		data = []
		for i in range(len(csv_data[0])):
			data.append([])
			for j in range(len(csv_data)):
				data[i].append(float(csv_data[j][i]))
		return data

	def getMinMaxMed(self, data):
		vals = [[],[],[]]
		for d in data:
			vals[0].append(min(d))
			vals[1].append(statistics.median(d))
			vals[2].append(max(d))
		return vals

	def drawLineGraphFromDeap(self, objective, query, generations, runs, ylim):

		csv_data = []

		input_file = objective["baseline_url"]+"checkpoint"+str(generations)+".csv"
		f = open(input_file, "r")
		for line in f:
			columns = line.split(",")
			if columns[0] == objective["name"]:
				csv_data.append(columns[9:generations+10])

		xlabel = "Generations (population size 25)"

		data = self.rotateData2D(csv_data)
		vals = self.getMinMaxMed(data)

		self.drawLineChart(vals, objective, query, self.algorithms["baseline"], runs, xlabel, ylim)

	def drawLineGraphFromMT(self, objective, query, generations, runs, ylim):

		csv_data = []

		input_file = objective["mt_url"]+"checkpoint"+str(generations)+".csv"
		f = open(input_file, "r")
		for line in f:
			columns = line.split(",")
			if columns[0] == "density-nest-food":
				data = []
				for scores in columns[9:generations+10]:
					score = scores.split(" ")
					data.append(score[objective["index"]])
				csv_data.append(data)

		xlabel = "Generations (population size 25)"

		data = self.rotateData2D(csv_data)
		vals = self.getMinMaxMed(data)

		self.drawLineChart(vals, objective, query, self.algorithms["mt"], runs, xlabel, ylim)

	def drawLineGraphFromQdpy(self, objective, query, generations, runs, ylim):

		csv_data = []

		for i in range(runs):

			index = i + 1
			input_file = objective["qdpy_url"]+"/"+str(index)+"/csvs/"+query["name"]+"-"+str(index)+".csv"
			f = open(input_file, "r")

			csv_data.append([])
			for line in f:
				items = line.split(",")
				if len(items) > 0 and int(items[0]) <= generations:
					csv_data[i].append(float(items[1][0:5]))

		data = self.rotateData2D(csv_data)
		vals = self.getMinMaxMed(data)

		algorithm = self.algorithms["qdpy"]
		xlabel = "Iterations (batch size 25)"

		self.drawLineChart(vals, objective, query, algorithm, runs, xlabel, ylim)

	def drawLineChart(self, vals, objective, query, algorithm, runs, xlabel, ylim):

		ylabel = query["ylabel"]
		# ea_name = algorithm["identifier"]+objective["identifier"]
		title = objective["description"]+" - "+algorithm["name"]+" algorithm over "+str(runs)+" runs\n"
		title += "Minimum, median and maximum " + query["description"]+"\n"

		labels = []
		for i in range(len(vals[0])):
			labels.append(i)

		fig, ax = plt.subplots(1, 1, sharex=True, sharey=True, figsize=(9, 6.5))

		plt.subplots_adjust(wspace=.3, hspace=1.4, bottom=0.12, top=0.85, left=0.12)

		ax.plot(labels, vals[1], lw=2)
		ax.fill_between(labels, vals[0], vals[2], alpha=0.3)

		ax.set_title(title,fontsize=13)
		ax.set_ylabel(ylabel,color='#222222', fontsize=12)
		ax.set_xlabel(xlabel,color='#222222', fontsize=11)

		ax.title.set_position([0.5,0.0])
		ax.yaxis.set_label_coords(-0.09,0.5)
		ax.xaxis.set_label_coords(0.5,-0.09)

		ax.set_ylim(ylim)

		output_file = "./"+query["name"]+"/line-charts/"+objective["name"]+"-"+algorithm["name"]+".png"
		print("output_file")
		print(output_file)
		# plt.savefig(output_file)

		plt.show()

	def algorithmName(self, algorithm, objective):
		# return algorithm["prefix"]+"$"+algorithm["code"]+objective["identifier"]+"$"
		return algorithm["code"]
