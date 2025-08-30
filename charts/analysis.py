
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

	def getData(self, query, deap_algorithms, qdpy_algorithms, objective, generation, feature, runs, mtc_index, mti_index):

		# hard coded for one or three features

		deap = []
		for algorithm in deap_algorithms:

			features = 3 if "mt" in algorithm["name"] else 1
			if "mti" in algorithm["name"]: feature = mti_index
			if "mtc" in algorithm["name"]: feature = mtc_index

			data = self.getDataFromCSV(query, algorithm["file_index"], generation, objective, runs, objective[algorithm["name"]+"_url"])
			data = data[feature][generation] if "mt" in algorithm["name"] else data[0][generation]
			deap.append(data)

		features = 1
		qdpy = []
		for algorithm in qdpy_algorithms:
			data = self.getDataFromCSV(query, algorithm["file_index"], generation, objective, runs, objective[algorithm["name"]+"_url"])
			data = data[feature][generation] if "mt" in algorithm["name"] else data[0][generation]
			qdpy.append(data)

		return deap + qdpy

	def getDataFromCSV(self, query, file_index, generations, objective, runs, filename):

		# returns scores for every seed per generation for each feature converted from
		# [seed][gen][feature] in horizontal_data to [feature][gen][seed] in vertical_data

		filename = filename + query["name"] + str(file_index)+".csv"

		f = open(filename, "r")

		horizontal_data = []

		for line in f:
			
			data = []
			columns = line.split(",")

			if columns[0] != "Type":
				for i in range(generations+1):

					if query["name"] == "coverage":
						# coverage is represented by only one value even for MT 
						score = columns[i+9]
						if score[0] == "[":
							# adjustment for qdpy output format for coverage
							score = float(score[1:-1])
						else:
							score = float(score)
						data.append([score])
					else:
						scores = columns[i+9]
						scoresList = scores.split(" ")
						if (scoresList[-1] == ""):
							data.append(scoresList[0:-1])
						else:
							data.append(scoresList)

				if len(horizontal_data) < runs:
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

	def drawOneGeneration(self, query, feature_index, objective_name, deap_algorithms, qdpy_algorithms, generation, runs, mtc_index, mti_index):
		
		objective = self.objectives.info[objective_name]
		data = self.getData(query, deap_algorithms, qdpy_algorithms, objective, generation, feature_index, runs, mtc_index, mti_index)

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
		if "foraging" not in algorithm["name"]: filename = "./"+query["name"]+"/gen"+str(generation)+"/"+objective["name"]+"-"+filename+".png"
		else: filename = "./"+query["name"]+"/foraging/"+filename+".png"
		
		title = objective["description"]+"\n"
		# if "foraging" not in algorithm["name"]: title += str(generation * 25)+" evaluations per objective\n"
		# if len(data) == 2: title += "pvalue = " +str("%.4f" % ttest.pvalue)+"\n\n"
		title += query["ylabel"]+" at "+str(generation)+" generations over "+str(runs)+" seeds\n"
		
		labels = []
		for algorithm in deap_algorithms + qdpy_algorithms:
			label = algorithm["code"]
			if "foraging" in algorithm["name"]:
				generation = algorithm["generations"]
				if generation != 1000:
					label += "\n("+str(generation)+" generations)\n"
			labels.append(label)

		num = -1
		consistent = True
		for d in data:
			if (num == -1): num = len(d)
			elif num != len(d): consistent = False
		
		ylabel = ""
		if consistent: ylabel = query["ylabel"]+' over '+str(len(data[0]))+' runs'
		else: ylabel = query["ylabel"]+' over a mixed number of runs'
		
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
		plt.subplots_adjust(wspace=.3, hspace=0.4, bottom=0.1, top=0.85, left=0.15)
		
		plots = ax.boxplot(data, medianprops=dict(color='#000000'), patch_artist=True, labels=labels)
		
		if len(data) == 4: colors = ['white', 'pink', 'lightblue', 'white']
		if len(data) == 3: colors = ['white', 'pink', 'white']
		if len(data) == 3 or len(data) == 4:
			for patch, color in zip(plots['boxes'], colors):
				patch.set_facecolor(color)
		else:
			for patch in plots['boxes']:
				patch.set_facecolor('white')

		ax.set_title(title,fontsize=13)
		ax.title.set_position([0.5,2.0])

		ax.set_ylabel(ylabel, color='#222222', fontsize=15)
		
		if foraging:
			ax.xaxis.set_label_coords(0.5,-.125)
		else:
			ax.xaxis.set_label_coords(0.5,-0.09)
		
		ax.yaxis.set_label_coords(-0.15,0.5)

		ax.tick_params(axis='x', labelsize=15)
		ax.tick_params(axis='y', labelsize=14)

		# plt.savefig(filename)
		print(filename)
		plt.show()

	def drawEvolution(self, algorithm, query, objective_name, runs, min_gen, max_gen, increment, x_axis_increment):

		objective = self.objectives.info[objective_name]
		url = objective[algorithm["name"]+"_url"]

		raw_data = None

		features = 3 if algorithm["type"] in ["MTC", "MTI"] else 1
		raw_data = self.getDataFromCSV(query, max_gen, max_gen, objective, runs, url)
		raw_data = raw_data[objective["index"]] if algorithm["type"] in ["MTC", "MTI"] else raw_data[0]

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

		input_file = objective[algorithm_url]+query["name"]+str(generations)+".csv"
		f = open(input_file, "r")
		for line in f:
			columns = line.split(",")
			if algorithm_name in ["mtc", "mti"]:
				if columns[0] in ["density-nest-food", "density-nest-ifood", "food-idensity-inest", "idensity-inest-ifood"]:
					data = []
					for scores in columns[9:generations+10]:
						score = scores.split(" ")
						data.append(float(score[objective["index"]]))
					csv_data.append(data)
			else:
				if columns[0] == objective["name"]:
					csv_data.append(columns[9:generations+10])

		xlabel = "Generations (population size 25)"

		data = self.rotateData2D(csv_data)
		vals = self.getMinMaxMed(data)

		self.drawLineChart(vals, objective, query, self.algorithms.info[algorithm_name], runs, xlabel, ylim)

	def drawLineChart(self, vals, objective, query, algorithm, runs, xlabel, ylim):

		ylabel = query["ylabel"]
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
