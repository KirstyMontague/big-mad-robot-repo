import math
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import pickle
import time

import sys
sys.path.insert(0, '..')

from containers import *
from params import eaParams
from utilities import Utilities
from redundancy import Redundancy

from functools import reduce
from operator import mul
from qdpy.utils import is_iterable

import matplotlib
import matplotlib as mpl


class Heatmaps():

    def __init__(self):
        self.params = eaParams()
        self.params.is_qdpy = True
        self.objective = self.params.indexes[0]
        self.generations = self.params.generations
        self.input = "separate"
        self.seeds = []
        self.runs = 0
        self.bins = [8,8,8]
        self.domain = [(-40.0, 40.0), (-40.0, 40.0), (0.0, 1.0)]

        self.pause = 20.0
        self.save = False
        self.save_combined = False

        self.cancelled = False
        self.configure()
        print()

        self.seeds = self.seedsList()

        self.utilities = Utilities(self.params, None)
        self.utilities.toolbox = self.utilities.setupToolboxGP(None)

        self.redundancy = Redundancy(self.params)

    def configure(self):
        permitted = ["input", "project", "objective", "experiment", "generations", "seeds", "runs", "bins", "domain", "save", "save_combined", "pause"]
        with open(self.params.shared_path+"/heatmaps.txt", 'r') as f:
            for line in f:
                data = line.split()
                if len(data) > 0:
                    if data[0] in permitted:
                        print(line.strip('\t\n\r'))
                        self.update(data)
                    else:
                        print("\nconfig entry not recognised: "+data[0]+"\n")
                        self.cancelled = True

    def update(self, data):

        if data[0] == "input":
            types = ["separate", "combined", "accumulate"]
            if data[1] in types:
                self.input = data[1]
            else:
                print("input type not recognised")
                self.cancelled = True

        if data[0] == "objective":
            self.objective = int(data[1])
            self.params.indexes = [self.objective]
            self.params.description = self.params.objectives[self.objective]

        if data[0] == "bins" and len(data) > 1:
            self.bins = []
            for b in data[1:]:
                self.bins.append(int(b))

        if data[0] == "domain" and len(data) > 1:
            self.domain = []
            for i in range(1, len(data), 2):
                self.domain.append((float(data[i]), float(data[i+1])))

        if data[0] == "seeds" and len(data) > 1:
            self.seeds = []
            for seed in data[1:]:
                self.seeds.append(int(seed))

        if data[0] == "project": self.params.project = data[1]
        if data[0] == "experiment" and len(data) > 1: self.params.experiment = data[1]
        if data[0] == "generations": self.generations = int(data[1])
        if data[0] == "runs": self.runs = int(data[1])
        if data[0] == "save": self.save = True if data[1] == "True" else False
        if data[0] == "save_combined": self.save_combined = True if data[1] == "True" else False
        if data[0] == "pause": self.pause = float(data[1])

    def seedsList(self):
        seeds = []
        if self.runs > 0:
            for i in range(1, self.runs + 1):
                seeds.append(i)
        else:
            seeds = self.seeds
        return seeds

    def getData(self, algorithm):

        container = self.utilities.createContainer(self.bins, self.domain, 1)
        if self.params.usingNewGrid:
            container.discardOutOfBounds(True)

        algorithm_type = "qdpy" if algorithm == "qdpy" else "gp"
        description = self.utilities.getExperimentDescription(self.objective, algorithm)

        input_dir = self.params.input_path+"/"+algorithm_type+self.params.directoryPath(description)
        output_dir = self.params.output_path+"/"+algorithm_type+self.params.directoryPath(description)
        output_file = self.params.description+"-with-all-seeds-small-bins.txt"

        if self.params.project == "legacy":
            if self.input == "separate":
                for seed in self.seeds:
                    filename = self.utilities.getLegacyCheckpointFilename(input_dir, algorithm, seed, self.objective, self.generations)
                    self.utilities.getLegacyCheckpointContainer(container, algorithm, filename, self.objective)
                if self.save_combined:
                    self.utilities.saveContainer(container, output_dir, output_dir+"/"+output_file)
            elif self.input == "combined":
                filename = input_dir+"/"+output_file
                self.utilities.updateContainerFromString(self.redundancy, self.utilities.toolbox, container, filename)
            else:
                print("input type not supported")
                return

        else:
            if self.input == "accumulate":
                cumulative_file = output_dir+"/"+output_file
                print("cumulative "+cumulative_file)
                self.utilities.updateContainerFromString(self.redundancy, self.utilities.toolbox, container, cumulative_file, 0, 0)
                print("pausing for "+str(self.pause)+"s\n")
                time.sleep(self.pause)

            if self.input == "combined":
                filename = input_dir+"/"+output_file
                print("combined "+filename)
                self.utilities.updateContainerFromString(self.redundancy, self.utilities.toolbox, container, filename, 0, 0)
            else:
                for seed in self.seeds:
                    filename = input_dir+"/"+str(seed)+"/checkpoint-"
                    filename += self.params.description+"-"+str(seed)+"-"+str(self.generations)+"-"+self.params.description+".txt"
                    print("seed file "+filename)
                    self.utilities.updateContainerFromString(self.redundancy, self.utilities.toolbox, container, filename, 0, 0)
                    print("pausing for "+str(self.pause)+"s\n")
                    time.sleep(self.pause)

            print("output "+output_dir+"/"+output_file)
            if self.save_combined:
                self.utilities.saveContainer(container, output_dir, output_dir+"/"+output_file)

        return container

    def flattenFitnessScores(self, data):
        for x in range(len(data)):
            for y in range(len(data[0])):
                for z in range(len(data[0][0])):
                    for w in range(len(data[0][0][0])):
                        if not math.isnan(data[x][y][z][w]):
                            data[x][y][z][w] = 1.0

    def rotateDomain(self):
        if self.params.project == "legacy":
            shape = [self.domain[2], self.domain[1], self.domain[0]]
            self.domain = shape

    def rotateGrid(self, population):

        for i in range(len(population)):
            for j in range(len(population[i])):
                output = ""
                for k in range(len(population[i][j])):
                    output += str(population[i,j,k])+" "
                # print(output+"\n")

        # population shape = movement, rotations (x), conditionality (y)
        # population shape = density, nest, food

        if self.params.project == "legacy":
            rotated_population = np.zeros((population.shape[2], population.shape[1], population.shape[0]))
        else:
            rotated_population = np.zeros((population.shape[0], population.shape[1], population.shape[2]))

        for i in range(population.shape[0]):
            for j in range(population.shape[1]):
                for k in range(population.shape[2]):
                    if self.params.project == "legacy":
                        rotated_population[i,j,k] = population[k,j,i]
                    else:
                        rotated_population[i,j,k] = population[i,j,k]

        # rotated_population shape = conditionality, rotations (x), movement (y)
        # rotated_population shape = food, nest, density

        return rotated_population

    def drawColourBar(self, fig, ax, cax, figure_size):

        fig.subplots_adjust(right=0.9, wspace=0.40)
        colour_bar_axes = fig.add_axes([0.92, 0.3, 0.01, 0.4])
        cbar = fig.colorbar(cax, cax=colour_bar_axes, format="%.2f")
        cbar.ax.tick_params(labelsize=12)

    def writeZTitle(self, index):
        domain = self.domain[0]
        domain_max = domain[1] - domain[0]
        start = ((domain_max / self.bins[0]) * index) + domain[0]
        end = ((domain_max / self.bins[0]) * (index + 1)) + domain[0]
        title = str("%1.3f" % start)+"  -  "+str("%1.3f" % end)
        return title

    def getQualityArray(self, container):
        if self.params.usingNewGrid:
            return container.quality_array()
        else:
            return container.quality_array[..., 0]

    def drawHeatmap(self, algorithms):

        start_time = round(time.time() * 1000)

        all_data = []
        try:
            for algorithm in algorithms:
                container = self.getData(algorithm)
                quality_array = self.getQualityArray(container)
                all_data.append(self.rotateGrid(quality_array))
                print(self.utilities.printExtrema(container))
        except FileNotFoundError as e:
            print("\n"+str(e)+"\n")
            return

        end_time = round(time.time() * 1000)
        duration = end_time - start_time
        print("\nLoading time: " +self.utilities.formatDuration(duration)+"\n")
        start_time = round(time.time() * 1000)

        if self.params.project == "legacy":
            fitness_min = -0.5
            fitness_max = 1.0
            for data in all_data:
                fitness_min = np.max([fitness_min, np.nanmin(data)])
                fitness_max = np.min([fitness_max, np.nanmax(data)])
            bin_size_inches = 0.2
            ticks = 4
            self.rotateDomain()
        else:
            fitness_min = 0.0
            fitness_max = 1.8
            bin_size_inches = 0.04
            ticks = 8
            self.flattenFitnessScores(all_data)

        colour_map="YlGnBu"
        colour_bar_label="Fitness"
        features_domain = self.domain
        fitness_domain = (fitness_min, fitness_max)

        if len(all_data[0].shape) % 2 == 1:
            for i in range(len(all_data)):
                all_data[i] = all_data[i].reshape((all_data[i].shape[0], 1) + all_data[i].shape[1:])
            features_domain = (features_domain[0], (0., 0.)) + tuple(features_domain[1:])
        bins = all_data[0].shape

        if self.params.project == "legacy":
            section_start = 0
        else:
            section_start = 15
            section_end = 20
            section_size = section_end - section_start
            bins = (section_size, 1, bins[2], bins[3])

        horizontal_bins = bins[::2]
        vertical_bins = bins[1::2]
        horizontal_bins_total = reduce(mul, horizontal_bins, 1)
        vertical_bins_total = reduce(mul, vertical_bins, 1)
        vertical_bins_total *= len(all_data)

        figure_size = [3.1 + horizontal_bins_total * bin_size_inches, 1. + vertical_bins_total * bin_size_inches]

        fig, ax = plt.subplots(nrows=len(all_data), ncols=bins[0], figsize=figure_size)

        for x in range(bins[0]):
            for y in range(len(all_data)):
                data = all_data[y]
                ax = plt.subplot(len(all_data), bins[0], y * bins[0] + x + 1)
                z_index = x + section_start
                if x == 0 and self.params.project == "legacy":
                    ax.set_ylabel(algorithms[y].upper(), fontsize=15, rotation='horizontal')
                    ax.yaxis.set_label_coords(-0.7,0.4)
                cax = self.drawSubplot(ax,
                                       data[x, 0, 0:bins[2], 0:bins[3]],
                                       data_t = data[x, 0, 0:bins[2], 0:bins[3]].T,
                                       colour_map=colour_map,
                                       features_domain=features_domain[-2:],
                                       fitness_domain=fitness_domain[-2:],
                                       z_index=z_index, bins=(bins[2], bins[3]), ticks=ticks)

        plt.tight_layout()
        self.drawColourBar(fig, ax, cax, figure_size)

        output_filename = "./heatmaps/temp.png"
        if self.save:
            print("\nWriting to "+output_filename+"\n")
            fig.savefig(output_filename)
        else:
            print("\nOutput file: "+output_filename+"\n")

        end_time = round(time.time() * 1000)
        duration = end_time - start_time
        print("\nProcessing time: " +self.utilities.formatDuration(duration)+"\n")

        plt.show()

    def drawSubplot(self, ax, data, data_t, colour_map, features_domain, fitness_domain, z_index=0, bins=None, ticks = 4):

        vertical_min = fitness_domain[0]
        if np.isnan(vertical_min) or np.isinf(vertical_min):
            vertical_min = np.nanmin(data)

        vertical_max = fitness_domain[1]
        if np.isnan(vertical_max) or np.isinf(vertical_max):
            vertical_max = np.nanmax(data)

        cax = ax.imshow(data_t, interpolation="none", cmap=colour_map, vmin=vertical_min, vmax=vertical_max, aspect="equal")

        ax.set_title(self.writeZTitle(z_index),fontsize=10)

        ax.xaxis.set_tick_params(which='major', left=True, bottom=True, top=False, right=False)
        ax.yaxis.set_tick_params(which='major', left=True, bottom=True, top=False, right=False)

        ax.xaxis.set_tick_params(which='minor', direction="in", left=False, bottom=False, top=False, right=False)
        ax.yaxis.set_tick_params(which='minor', direction="in", left=False, bottom=False, top=False, right=False)

        xticks = list(np.arange(0, len(data)    + 1, len(data)    / ticks))
        yticks = list(np.arange(0, len(data[0]) + 1, len(data[0]) / ticks))

        ax.set_xticks(xticks)
        ax.set_yticks(yticks)

        delta_x = features_domain[0][1] - features_domain[0][0]
        delta_y = features_domain[1][1] - features_domain[1][0]

        if self.params.project == "legacy":
            ax.set_xticklabels([f'{round(float(x / float(len(data))    * delta_x + features_domain[0][0]), 2):1.0f}' for x in xticks], fontsize=10)
            ax.set_yticklabels([f'{round(float(y / float(len(data[0])) * delta_y + features_domain[1][0]), 2):1.0f}' for y in yticks], fontsize=10)
        else:
            ax.set_xticklabels([f'{round(float(x / float(len(data))    * delta_x + features_domain[0][0]), 2):1.1f}' for x in xticks], fontsize=10)
            ax.set_yticklabels([f'{round(float(y / float(len(data[0])) * delta_y + features_domain[1][0]), 2):1.1f}' for y in yticks], fontsize=10)

        if bins[1] == 1:
            yticks = []

        plt.xticks(xticks, rotation='vertical')
        plt.yticks(yticks)

        ax.invert_yaxis()

        ax.autoscale_view()

        return cax

if __name__ == "__main__":

    # algorithms = ["gp", "mtc", "mti", "qdpy"]
    algorithms = ["qdpy"]

    heatmaps = Heatmaps()

    if not heatmaps.cancelled:
        heatmaps.drawHeatmap(algorithms)


