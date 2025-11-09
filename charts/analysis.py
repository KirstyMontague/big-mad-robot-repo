
import sys
sys.path.insert(0, '..')

import matplotlib.pyplot as plt

from scipy.stats import ttest_ind
from scipy.stats import shapiro
from scipy.stats import mannwhitneyu
import statistics

import pickle
import numpy

from deap import base, creator, tools, gp

from algorithms import Algorithms
from objectives import Objectives
from queries import Queries

from params import eaParams
from utilities import Utilities
import local


class Analysis():

	def __init__(self):
		self.params = eaParams()
		self.utilities = Utilities(self.params)
		
		self.algorithms = Algorithms()
		self.objectives = Objectives()
		self.queries = Queries()

	def getData(self, query, deap_algorithms, qdpy_algorithms, objective, generation, runs):

		# getData is currently only used for drawing one generation so we use that as the interval
		interval = generation
		index = int(generation/interval)

		deap = []
		for algorithm in deap_algorithms:

			features = 3 if "mt" in algorithm["name"] else 1
			csv_index = self.getCsvIndex(objective, algorithm["name"])

			data = self.getDataFromCSV(query, algorithm["file_index"], generation, interval, objective, runs, objective[algorithm["name"]+"_url"])
			data = data[csv_index][index] if "mt" in algorithm["name"] and query["name"] != "coverage" else data[0][index]
			deap.append(data)

		features = 1
		qdpy = []
		for algorithm in qdpy_algorithms:
			data = self.getDataFromCSV(query, algorithm["file_index"], generation, interval, objective, runs, objective[algorithm["name"]+"_url"])
			data = data[0][index]
			qdpy.append(data)

		return deap + qdpy

	def getDataFromCSV(self, query, file_index, generations, interval, objective, runs, filename):

		# returns scores for every seed per generation for each feature converted from
		# [seed][gen][feature] in horizontal_data to [feature][gen][seed] in vertical_data

		filename = filename + query["name"] + str(file_index)+".csv"

		with open(filename, "r") as f:

			indexes = []
			horizontal_data = []

			for line in f:
				
				data = []
				columns = line.split(",")

				if columns[0] in ["Type", "Objective"]:
					for i in range(9, len(columns)):
						if columns[i].isdigit() and int(columns[i]) <= generations and int(columns[i]) % interval == 0:
							indexes.append(i)

				elif columns[0] not in ["Type", "Objective"] and len(indexes) > 0 and len(horizontal_data) < runs:
					for i in range(generations+1):
						index = i + 9
						if index in indexes:
							if query["name"] == "coverage":
								# coverage is represented by only one value even for MT 
								score = columns[index]
								if score[0] == "[":
									# adjustment for qdpy output format for coverage
									score = float(score[1:-1])
								else:
									score = float(score)
								data.append([score])
							else:
								scores = columns[index]
								scoresList = scores.split(" ")
								if (scoresList[-1] == ""):
									data.append(scoresList[0:-1])
								else:
									data.append(scoresList)

					horizontal_data.append(data)
			
		# print ("")
		# print(len(horizontal_data))
		# print(len(horizontal_data[0]))
		# print(len(horizontal_data[0][0]))
		# for data in horizontal_data:
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
		# print(len(vertical_data))
		# print(len(vertical_data[0]))
		# print(len(vertical_data[0][0]))
		# for data in vertical_data:
			# print (data[-1])
		# print ("")

		return vertical_data

	def checkHypothesis(self, data1, data2):
		
		data1_normal = shapiro(data1)
		data2_normal = shapiro(data2)
		
		both_normal = True if data1_normal.pvalue > 0.05 and data2_normal.pvalue > 0.05 else False
		
		if both_normal:
			ttest = ttest_ind(data1, data2)
			print ("ttest "+str(ttest.pvalue))
		else:
			ttest = mannwhitneyu(data1, data2)
			print ("mwu "+str(ttest.pvalue))

		return ttest

	def drawOneGeneration(self, query, objective_name, deap_algorithms, qdpy_algorithms, generation, runs):

		objective = self.objectives.info[objective_name]
		data = self.getData(query, deap_algorithms, qdpy_algorithms, objective, generation, runs)

		if len(data) == 2:
			if len(data[0]) > 2 and len(data[1]) > 2:
				ttest = self.checkHypothesis(data[0], data[1])

		if len(data) > 2:
			print ("")
			for i in range(1, len(data)):
				self.checkHypothesis(data[0], data[i])
				ttest = ttest_ind(data[0], data[i])
			print ("")

		consistent = True
		for d in data:
			if len(d) != len(data[0]):
				consistent = False

		if objective["name"] == "foraging": filename = "./"+query["name"]+"/foraging/temp.png"
		else:
			if query["name"] == "best": filename = "./"+query["name"]+"/sub-behaviours/"+objective["name"]+".png"
			else: filename = "./"+query["name"]+"/"+objective["name"]+".png"

		suptitle = objective["description"]+"\n"
		if consistent: title = str(len(data[0]))+' runs at '+str(generation)+' generations\n'
		else: title = query["ylabel"]+' at '+str(generation)+' generations over a mixed number of runs\n'
		
		labels = []
		for algorithm in deap_algorithms + qdpy_algorithms:
			label = algorithm["code"]
			if "foraging" in algorithm["name"]:
				generation = algorithm["generations"]
				if generation != 1000:
					label += "\n("+str(generation)+" generations)\n"
			labels.append(label)

		self.drawPlotsBigLabels(data, suptitle, title, labels, query["ylabel"], filename)

	def drawPlotsForaging(self, data, suptitle, title, labels, ylabel, filename):

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

	def drawPlotsBigLabels(self, data, suptitle, title, labels, ylabel, filename):

		# plot_width = 4 + len(data) # by nest
		plot_width = 6 + len(data) # by algorithm

		fig, ax = plt.subplots(figsize=(plot_width, 6))
		plt.subplots_adjust(wspace=.3, hspace=0.4, bottom=0.1, top=0.85, left=0.15)

		plots = ax.boxplot(data, medianprops=dict(color='#000000'), patch_artist=True, labels=labels)

		if len(data) == 4:
			colors = ['lightgray', 'pink', 'lightblue', 'lightgray']
			for patch, color in zip(plots['boxes'], colors):
				patch.set_facecolor(color)

		for patch in plots['boxes']:
			patch.set_facecolor('lightblue')

		# fig.suptitle(suptitle,fontsize=15,x=0.53, y=0.97)
		ax.set_title(title,fontsize=18)
		ax.title.set_position([0.5,1.0])

		ax.set_ylabel(ylabel, color='#222222', fontsize=18)

		ax.yaxis.set_label_coords(-0.14,0.5)
		ax.xaxis.set_label_coords(0.5,-0.09)

		ax.tick_params(axis='x', labelsize=15) # by algorithm
		# ax.tick_params(axis='x', labelsize=16) # by nest
		ax.tick_params(axis='y', labelsize=16)

		# plt.savefig(filename)
		print(filename)
		plt.show()

	def drawOneGenerationCombo(self, query, objective_name, deap_algorithms, qdpy_algorithms, generation, runs):

		objective = self.objectives.info[objective_name]
		data = self.getData(query, deap_algorithms, qdpy_algorithms, objective, generation, runs)

		if len(data) > 2:
			print ("")
			for i in range(1, len(data)):
				self.checkHypothesis(data[0], data[i])
				ttest = ttest_ind(data[0], data[i])
			print ("")

		consistent = True
		for d in data:
			if len(d) != len(data[0]):
				consistent = False

		filename = "./"+query["name"]+"/no-labels/foraging/temp.png"

		suptitle = objective["description"]+"\n"
		if consistent: title = str(len(data[0]))+' runs at '+str(generation)+' generations\n'
		else: title = query["ylabel"]+' at '+str(generation)+' generations over a mixed number of runs\n'

		labels = ["Baseline  ", "QD1", "QD8", "QD64"]

		fig, ax = plt.subplots(figsize=(11, 6), sharey=True)
		plt.subplots_adjust(wspace=.25, hspace=0.4, bottom=0.1, top=0.9, left=0.1, right=0.95)

		ax.yaxis.grid(True)
		ax.tick_params(axis='both',
					   which='both',
					   bottom=False,
					   labelleft=False,
					   labelbottom=False,
					   left=False,
					   grid_alpha=0.5)

		vertical_min = numpy.nanmin(data)
		vertical_max = numpy.nanmax(data) + 0.1

		# max fitness from max-fitness-calculator.py for nests with radius 40cm,
		# 50cm and 60cm and food boundary at 100cm and 120cm from arena centre
		self.normaliseFitness(data[0:4], 2.3745)
		self.normaliseFitness(data[4:8], 2.6032)
		self.normaliseFitness(data[8:12], 2.8811)

		self.drawSubPlot(data[0:4], 1, "80cm\n", labels, vertical_min, vertical_max)
		self.drawSubPlot(data[4:8], 2, "100cm\n", labels, vertical_min, vertical_max)
		self.drawSubPlot(data[8:12], 3, "120cm\n", labels, vertical_min, vertical_max)

		# plt.savefig(filename)
		print(filename)
		plt.show()

	def drawSubPlot(self, data, index, title, labels, vertical_min, vertical_max):

		ax = plt.subplot(1, 3, index, frameon=False)
		plots = ax.boxplot(data, medianprops=dict(color='#000000'), patch_artist=True, labels=labels, widths=0.8)

		if index == 1:
			ax.tick_params(
				axis='y',
				which='both',
				labelsize=13)
			ax.set_ylabel("Best fitness", color='#222222', fontsize=18, rotation='vertical')
			ax.yaxis.set_label_coords(-0.2,0.5)

		else:
			ax.tick_params(
				axis='y',
				which='both',
				labelleft=False,
				left=False)

		for patch in plots['boxes']:
			patch.set_facecolor('lightblue')

		ax.set_title(title,fontsize=18)
		ax.title.set_position([0.5,1.0])

		# ax.set_ylim([0, vertical_max])
		ax.set_ylim([0, 0.9])

		ax.tick_params(axis='x', labelsize=13)
		ax.xaxis.set_label_coords(0.5,0.09)

	def drawEvolution(self, algorithm, query, objective_name, runs, min_gen, max_gen, increment, x_axis_increment):

		objective = self.objectives.info[objective_name]
		url = objective[algorithm["name"]+"_url"]

		raw_data = None

		csv_index = self.getCsvIndex(objective, algorithm["name"])
		features = 3 if algorithm["type"] in ["MTC", "MTI"] else 1

		raw_data = self.getDataFromCSV(query, max_gen, max_gen, increment, objective, runs, url)
		raw_data = raw_data[csv_index]

		data = []
		for i in range(len(raw_data)):
			if (i >= min_gen and i <= max_gen):
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

		fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 6))
		plt.subplots_adjust(wspace=.3, hspace=.4, bottom=0.1, top=0.8)
		fig.suptitle(title, y=.925, fontsize=16, color='#333333')

		c = "#222222"
		plots = ax.boxplot(data,
						   vert=True,
						   patch_artist=True,
						   labels=labels,
						   boxprops=dict(color=c),
						   # boxprops=dict(facecolor=c, color=c),
						   capprops=dict(color=c),
						   whiskerprops=dict(color=c),
						   flierprops=dict(color=c, markeredgecolor=c),
						   medianprops=dict(color=c))

		for patch in plots['boxes']:
			patch.set_facecolor('lightblue')
		ax.title.set_position([0.5,1.05])
		ax.yaxis.grid(True)
		ax.set_ylim(query["ylim"][objective["index"]])
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

	def drawLineGraph(self, objective, algorithm_name, algorithm_url, query, generations, runs, ylim):

		csv_data = []
		csv_index = self.getCsvIndex(objective, algorithm_name)

		input_file = objective[algorithm_url]+query["name"]+str(generations)+".csv"
		with open(input_file, "r") as f:
			for line in f:
				columns = line.split(",")
				if algorithm_name in ["mtc", "mti"]:
					if columns[0] in ["density-nest-food", "density-nest-ifood", "food-idensity-inest", "idensity-inest-ifood"]:
						data = []
						for scores in columns[9:generations+10]:
							score = scores.split(" ")
							data.append(float(score[csv_index]))
						csv_data.append(data)
				else:
					if columns[0] == objective["name"]:
						csv_data.append(columns[9:generations+10])

		xlabel = "Generations"

		data = self.rotateData2D(csv_data)
		vals = self.getMinMaxMed(data)

		self.drawLineChart(vals, objective, query, self.algorithms.info[algorithm_name], runs, xlabel, ylim)

	def drawLineChart(self, vals, objective, query, algorithm, runs, xlabel, ylim):

		ylabel = query["ylabel"]
		title = objective["description"]+" - "+algorithm["name"]+" algorithm over "+str(runs)+" runs\n"
		if objective["name"] == "foraging":
			title = "Foraging with 64 of each sub-behaviour ("+algorithm["code"]+")\n\n"
		else:
			title = objective["description"]+" over "+str(runs)+" runs\n\n"
		title += "Minimum, median and maximum " + query["description"]

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

		if objective["name"] == "foraging":
			output_file = "./"+query["name"]+"/line-charts/foraging/"+algorithm["code"]+".png"
		else:
			output_file = "./"+query["name"]+"/line-charts/sub-behaviours/"+objective["name"]+"-"+algorithm["code"]+".png"
		print("output_file")
		print(output_file)
		# plt.savefig(output_file)

		plt.show()




	def normaliseFitness(self, data, max_fitness):

		for i in range(len(data)):
			for j in range(len(data[i])):
				fitness = data[i][j]
				data[i][j] = fitness / max_fitness

	def getCsvIndex(self, objective, algorithm_name):
		if algorithm_name == "mtc":
			return self.getMtcIndex(objective["index"])
		elif algorithm_name == "mti":
			return self.getMtiIndex(objective["index"])
		else:
			return 0

	def getMtcIndex(self, objective):
		mtc_index = -1
		if objective in [0, 2]: mtc_index = 0
		if objective in [1, 3]: mtc_index = 1
		if objective in [4, 5]: mtc_index = 2
		return mtc_index

	def getMtiIndex(self, objective):
		mti_index = -1
		if objective in [0, 3]: mti_index = 0
		if objective in [1, 4]: mti_index = 1
		if objective in [2, 5]: mti_index = 2
		return mti_index

	def getObjectivesCombination(self, objective, compatible):
		if compatible:
			if objective in [0, 1, 5]: return "density-nest-ifood"
			if objective in [2, 3, 4]: return "food-idensity-inest"
		else:
			if objective in [0, 1, 2]: return "density-nest-food"
			if objective in [3, 4, 5]: return "idensity-inest-ifood"

