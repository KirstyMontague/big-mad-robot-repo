
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

    def getDataFromCSV(self, query, file_index, generations, interval, objective, runs, filename):

        # returns scores for every seed per generation for each feature converted from
        # [seed][gen][feature] in horizontal_data to [feature][gen][seed] in vertical_data

        print("Loading from: "+filename)

        try:
            with open(filename, "r") as f:

                indexes = []
                horizontal_data = []
                first_gen_column = 0

                for line in f:

                    data = []
                    sections = line.split("\"")
                    columns = sections[0].split(",")

                    if columns[0] in ["Type", "Objective", "Time"]:
                        for i in range(0, len(columns)):
                            if columns[i].isdigit():
                                if first_gen_column == 0:
                                    first_gen_column = i
                            if columns[i].strip('\t\n\r').isdigit() and int(columns[i]) <= generations and int(columns[i]) % interval == 0:
                                indexes.append(i)

                    elif columns[0] not in ["Type", "Objective", "Time"] and len(indexes) > 0 and len(horizontal_data) < runs:
                        for i in range(generations+1):
                            index = i + first_gen_column
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

        except FileNotFoundError as e:
            print("\n"+str(e)+"\n")
            raise ValueError(e)
            return

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

    def checkHypothesis(self, data):

        try:
            mwu_string = "\n"
            for i in range(len(data) - 1):
                for j in range(i + 1, len(data)):
                    mwu = mannwhitneyu(data[i], data[j])
                    mwu_string += "mwu "+str(mwu.pvalue)+"\n"
                if i != len(data) - 2:
                     mwu_string += "\n"
            return mwu_string
        except ValueError as e:
            print("\nCheck hypothesis failed, not enough data (minimum 3 seeds)")
            print("\n"+str(e)+"\n")
            return

    def drawPlotsForaging(self, data, title, labels, ylabel):

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

        return plt

    def drawPlotsBigLabels(self, data, title, labels, query_name, query_label, objective_index):

        plot_width = 8 + len(data)

        fig, ax = plt.subplots(figsize=(plot_width, 6))
        plt.subplots_adjust(wspace=0.0, hspace=0.0, bottom=0.15, top=0.97, left=0.14, right=0.97)

        plots = ax.boxplot(data, medianprops=dict(color='#000000'), patch_artist=True, labels=labels)

        if len(data) == 7:
            colors = ['lightgray', 'lightblue', 'lightblue', 'lightblue', 'pink', 'pink', 'pink']
            for patch, color in zip(plots['boxes'], colors):
                patch.set_facecolor(color)

        for patch in plots['boxes']:
            patch.set_facecolor('lightblue')

        ax.set_title(title,fontsize=18)
        ax.title.set_position([0.5,1.0])

        ylim = self.queries.info[query_name]["ylim"]
        ax.set_ylim(ylim[objective_index])

        ax.set_ylabel(query_label, color='#222222', fontsize=24)

        ax.yaxis.set_label_coords(-0.11,0.5)
        ax.xaxis.set_label_coords(0.5,-0.09)

        ax.tick_params(axis='x', labelsize=22)
        ax.tick_params(axis='y', labelsize=19)

        return plt

    def drawPlotsTwoExperiments(self, data, title, labels, query_name, query_label, objective_index):

        plot_width = 6 + len(data)

        fig, ax = plt.subplots(figsize=(plot_width, 6))
        plt.subplots_adjust(wspace=0.0, hspace=0.0, bottom=0.15, top=0.97, left=0.14, right=0.97)

        plots = ax.boxplot(data, medianprops=dict(color='#000000'), patch_artist=True, labels=labels, widths=0.45)

        for patch in plots['boxes']:
            patch.set_facecolor('lightblue')

        ax.set_title(title,fontsize=18)
        ax.title.set_position([0.5,1.0])

        ylim = self.queries.info[query_name]["ylim"]
        ax.set_ylim(ylim[objective_index])

        ax.set_ylabel(query_label, color='#222222', fontsize=24)

        ax.yaxis.set_label_coords(-0.11,0.5)
        ax.xaxis.set_label_coords(0.5,-0.09)

        ax.tick_params(axis='x', labelsize=22)
        ax.tick_params(axis='y', labelsize=19)

        return plt

    def drawPlotsNoLabels(self, data, title, labels, query_name, objective_index):

        plot_width = 6 + len(data)

        fig, ax = plt.subplots(figsize=(plot_width, 6))
        plt.subplots_adjust(wspace=0.0, hspace=0.0, bottom=0.1, top=0.97, left=0.1)
        plots = ax.boxplot(data, medianprops=dict(color='#000000'), patch_artist=True, labels=labels)

        ylim = self.queries.info[query_name]["ylim"]
        ax.set_ylim(ylim[objective_index])

        for i in range(len(plots['boxes'])):
            plots['boxes'][i].set_facecolor('lightblue')

        ax.yaxis.set_label_coords(-0.14,0.5)
        ax.xaxis.set_label_coords(0.5,-0.09)

        ax.tick_params(axis='x', labelsize=20)
        ax.tick_params(axis='y', labelsize=18)

        return plt

    def drawOneGenerationCombo(self, path, filename, query_name, objective_index, parameters, runs, generation = 0):

        objective = self.objectives.info[self.objectives.index[objective_index]]
        query = self.queries.info[query_name]

        result = []
        labels = []
        sources = []

        for param in parameters:

            algorithm = param["algorithm"]
            experiment = param["experiment"]
            repertoire = param["repertoire"]
            if "generation" in param:
                generation = param["generation"]

            axis = 0
            if query_name == "extrema":
                axis = param["axis"]

            subdirectory = ""
            if "subdirectory" in param:
                subdirectory = param["subdirectory"]

            generations = self.getGeneration(generation, objective["name"], repertoire)
            interval = generations
            index = 0 if algorithm == "cma-es" else int(generations/interval)

            if "file_index" in param:
                file_index = param["file_index"]
            else:
                file_index = generations

            # if objective["name"] == "foraging" and repertoire == "baseline":
                # generations = self.getGeneration(generation, objective["name"], repertoire)
                # param["label"] += "\n("+str(generations)+" gen)\n"
            labels.append(param["label"])

            csv_path = self.getCsvPath(self.algorithms.info[algorithm], experiment, objective, repertoire, subdirectory)
            csv_filename = csv_path+"/"+self.getCsvFilename(file_index, query_name, axis)
            csv_index = self.utilities.getCsvIndex(objective["index"], algorithm)

            try:
                data = self.getDataFromCSV(query, file_index, generations, interval, objective, runs, csv_filename)
                data = data[csv_index] if "mt" in algorithm and query["name"] != "coverage" else data[0]
                sources.append(csv_filename)
            except ValueError as e:
                return

            if query["name"] == "coverage":
                for i in range(len(data)):
                    for j in range(len(data[i])):
                        data[i][j] = data[i][j] * 1000000

            if query["name"] == "avg-quality":
                try:
                    coverage_filename = csv_path+"/coverage"+str(file_index)+".csv"
                    coverage = self.getDataFromCSV(self.queries.info["coverage"], generations, generations, generations, objective, runs, coverage_filename)
                    coverage = coverage[0]
                    sources.append(coverage_filename)
                except ValueError as e:
                    return
                data = self.calculateAvgQuality(coverage, data, 1000000)

            result.append(data)

        data = [r[-1] for r in result]

        mwu_string = self.checkHypothesis(data)

        consistent = True
        for d in data:
            if len(d) != len(data[0]):
                consistent = False

        suptitle = objective["description"]+"\n"
        if consistent: title = str(len(data[0]))+' runs at '+str(generation)+' generations\n'
        else: title = query["ylabel"]+' at '+str(generation)+' generations over a mixed number of runs\n'
        title = objective["description"]+"\n"

        if False:
            plt = self.drawSubPlots(data, labels)
        elif len(labels) == 2:
            plt = self.drawPlotsTwoExperiments(data, title, labels, query_name, query["ylabel"], objective_index)
        else:
            plt = self.drawPlotsBigLabels(data, title, labels, query_name, query["ylabel"], objective_index)

        print(mwu_string)
        print("Output file: "+path+"/"+filename)

        params_string = self.writeParameterString(sources, parameters, mwu_string, path+"/"+filename)
        self.saveImage(path, filename, params_string)

    def drawOneGenerationKilobots(self, path, filename, query_name, objective_index, parameters, runs, generation = 0):

        objective = self.objectives.info[self.objectives.index[objective_index]]
        query = self.queries.info[query_name]

        result = []
        labels = []
        sources = []

        for param in parameters:
            algorithm = param["algorithm"]
            experiment = param["experiment"]
            labels.append(param["label"])

            generations = generation
            interval = generations
            file_index = generations
            data_index = 1

            description = self.utilities.getExperimentDescription(objective["index"], algorithm)
            csv_path = self.algorithms.info[algorithm]["path"]

            csv_filename = self.params.input_path+"/"+csv_path+"/"+experiment+"/"+param["filename"]+".csv"

            try:
                data = self.getDataFromCSV(query, file_index, generations, interval, objective, runs, csv_filename)
                data = data[0][data_index]
                sources.append(csv_filename)
            except ValueError as e:
                return

            result.append(data)

        data = result

        mwu_string = self.checkHypothesis(data)

        consistent = True
        for d in data:
            if len(d) != len(data[0]):
                consistent = False

        suptitle = objective["description"]+"\n"
        if consistent: title = str(len(data[0]))+' runs at '+str(generation)+' generations\n'
        else: title = query["ylabel"]+' at '+str(generation)+' generations over a mixed number of runs\n'
        title = objective["description"]+"\n"

        self.drawPlotsBigLabels(data, title, labels, query["name"], query["ylabel"], objective_index)

        print(mwu_string)
        print("Output file: "+path+"/"+filename)

        params_string = self.writeParameterString(sources, parameters, mwu_string, path+"/"+filename)
        self.saveImage(path, filename, params_string)

    def drawSubPlots(self, data, labels):

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

        self.drawSubPlot(data[0:3], 1, "Plot 1\n", labels[0:3], vertical_min, vertical_max)
        self.drawSubPlot(data[3:6], 2, "Plot 2\n", labels[3:6], vertical_min, vertical_max)
        self.drawSubPlot(data[6:9], 3, "Plot 3\n", labels[6:9], vertical_min, vertical_max)

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

        ax.set_ylim([0, vertical_max])

        ax.tick_params(axis='x', labelsize=13)
        ax.xaxis.set_label_coords(0.5,0.09)

    def drawEvolution(self, experiment, algorithm, query, objective, repertoire, file_index, runs, min_gen, max_gen, increment, x_axis_increment):

        objective = self.objectives.info[objective]

        csv_path = self.getCsvPath(algorithm, experiment, objective, repertoire)
        filename = csv_path+"/"+self.getCsvFilename(file_index, query["name"])

        try:
            data = self.getDataFromCSV(query, file_index, max_gen, increment, objective, runs, filename)
        except ValueError as e:
            return

        data = data[0][int(min_gen/increment):int(max_gen/increment)+1]

        if query["name"] == "coverage":
            for i in range(len(data)):
                for j in range(len(data[i])):
                    data[i][j] *= 1000000

        if query["name"] == "avg-quality":
            try:
                coverage_filename = csv_path+"/coverage"+str(file_index)+".csv"
                coverage = self.getDataFromCSV(self.queries.info["coverage"], file_index, max_gen, increment, objective, runs, coverage_filename)
                coverage = coverage[0][int(min_gen/increment):int(max_gen/increment)+1]
            except ValueError as e:
                return
            data = self.calculateAvgQuality(coverage, data, 1000000)

        labels = []
        for i in range(len(data)):
            gen = min_gen + (i * increment)
            if gen % x_axis_increment == 0:
                labels.append(gen)
            else:
                labels.append("")

        title = objective["description"]+" - "+algorithm["description"]+" algorithm"

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
                           medianprops=dict(color=c),
                           widths=0.8)

        for patch in plots['boxes']:
            patch.set_facecolor('lightblue')
        ax.title.set_position([0.5,1.05])
        ax.yaxis.grid(True)
        ax.set_ylim(query["ylim"][objective["index"]])
        ax.set_ylabel('Fitness over '+str(len(data[0]))+' runs', color=c, fontsize=12)
        ax.set_xlabel('Generations', color=c, fontsize=12)
        ax.yaxis.set_label_coords(-0.09,0.5)
        ax.xaxis.set_label_coords(0.5, -0.1)

        settings = str(min_gen)+"-"+str(max_gen)+"-"+str(increment)
        path = "./evolution-box-plots/straight-to-foraging/"+repertoire
        filename = query["name"]+"-"+settings+".png"
        print("Output file: "+path+"/"+filename)

        self.saveImage(path, filename)

    def getMinMaxMed(self, data):
        vals = [[],[],[]]
        for d in data:
            vals[0].append(min(d))
            vals[1].append(statistics.median(d))
            vals[2].append(max(d))
        return vals

    def drawLineGraph(self, title, experiment, objective, algorithm, repertoire, query, generations, file_index, max_bins, ylim, runs):

        query = self.queries.info[query]
        objective = self.objectives.info[objective]
        algorithm = self.algorithms.info[algorithm]
        generations = self.getGeneration(generations, objective["name"], repertoire)

        csv_path = self.getCsvPath(algorithm, experiment, objective, repertoire)
        input_file = csv_path+"/"+self.getCsvFilename(file_index, query["name"])

        try:
            data = self.getDataFromCSV(query, file_index, generations, 1, objective, runs, input_file)
            data = data[0]
        except ValueError as e:
            return

        if query["name"] == "coverage":
            for i in range(len(data)):
                for j in range(len(data[i])):
                    data[i][j] *= max_bins

        if query["name"] == "avg-quality":
            try:
                coverage_file = csv_path+"/coverage"+str(file_index)+".csv"
                coverage = self.getDataFromCSV(self.queries.info["coverage"], file_index, generations, 1, objective, runs, coverage_file)
                coverage = coverage[0]
            except ValueError as e:
                return
            data = self.calculateAvgQuality(coverage, data, max_bins)

        xlabel = "Generations"

        vals = self.getMinMaxMed(data)

        ylabel = query["ylabel"]

        title += "\n\nMinimum, median and maximum " + query["description"]

        labels = []
        for i in range(len(vals[0])):
            labels.append(i)

        fig, ax = plt.subplots(1, 1, sharex=True, sharey=True, figsize=(15, 5))

        plt.subplots_adjust(wspace=.3, hspace=1.4, bottom=0.17, top=0.95, left=0.1, right=0.98)

        ax.plot(labels, vals[1], lw=2)
        ax.fill_between(labels, vals[0], vals[2], alpha=0.3)

        # ax.set_title(title,fontsize=13)
        # ax.title.set_position([0.5,0.0])

        ax.set_ylabel(ylabel,color='#222222', fontsize=18)
        ax.set_xlabel(xlabel,color='#222222', fontsize=16)

        ax.yaxis.set_label_coords(-0.08, 0.5)
        ax.xaxis.set_label_coords(0.5,-0.14)

        ax.tick_params(axis='x', labelsize=14)
        ax.tick_params(axis='y', labelsize=14)

        ax.set_ylim(ylim)

        path = "./evolution-line-charts/straight-to-foraging/"+repertoire+"-2000gen"
        filename = query["name"]+".png"

        print("Output file: "+path+"/"+filename)

        self.saveImage(path, filename)

    def getCsvPath(self, algorithm, experiment, objective, repertoire, subdirectory = ""):

        path = algorithm["path"]

        if subdirectory != "":
            description = subdirectory
        else:
            if objective["name"] == "foraging":
                description = self.params.foraging_path
                if algorithm["name"] != "cma":
                    description += "/"+repertoire
            else:
                description = self.utilities.getExperimentDescription(objective["index"], algorithm["name"])

            if algorithm["name"] == "cma":
                description = self.utilities.getIfoodCompacted(description)

        return self.params.input_path+"/"+path+"/"+experiment+"/"+description

    def getCsvFilename(self, file_index, query_name, axis = ""):

        query_name = "qd-scores" if query_name == "avg-quality" else query_name
        filename = query_name+str(file_index)

        if query_name == "extrema":
            filename += "-"+str(axis)

        filename += ".csv"
        return filename

    def normaliseFitness(self, data, max_fitness):

        for i in range(len(data)):
            for j in range(len(data[i])):
                fitness = data[i][j]
                data[i][j] = fitness / max_fitness

    def getGeneration(self, generation, objective, repertoire):
        if generation == 0:
            generation = 1000
            if objective == "foraging" and repertoire == "baseline":
                generation = 2200
        return generation

    def calculateAvgQuality(self, coverage, qdscore, max_bins):

        for i in range(len(qdscore)):
            for j in range(len(qdscore[i])):
                coverage[i][j] *= max_bins
                avg_quality = qdscore[i][j] * max_bins
                avg_quality /= float(coverage[i][j])
                qdscore[i][j] = avg_quality

        return qdscore

    def writeParameterString(self, sources, parameters, mwu_string, filename):

        string = "\n"

        for source in sources:
            string += "Loading from "+source+"\n"
        string += "\n"

        for param in parameters:
            string += "{"
            for key, value in param.items():
                if type(value) is str:
                    string += "\""+key+"\" : \""+value+"\", "
                else:
                    string += "\""+key+"\" : \""+str(value)+"\", "
            string = string[0:-2]+"}\n"

        string += mwu_string+"\n"
        string += filename+"\n"
        string += "\n===========================================\n"

        return string

    def saveImage(self, path, filename, string = ""):

        # plt.savefig(path+"/"+filename)

        # if string != "":
            # print("saving notes")
            # print(string)
            # with open(path+"/notes.txt", "a") as f:
                # f.write(string)

        plt.show()
