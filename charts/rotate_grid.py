import math
import matplotlib.pyplot as plt
import numpy as np
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
        self.objective = self.params.objectives[self.objective]
        self.generations = self.params.generations
        self.input = "separate"
        self.runs = 0
        self.seeds = []
        self.bins = [8,8,8]
        self.domain = [(-40.0, 40.0), (-40.0, 40.0), (0.0, 1.0)]
        self.save = self.params.saveOutput
        self.pause = 20.0

        self.cancelled = False
        self.configure()
        print()

        self.seeds = self.seedsList()

        self.utilities = Utilities(self.params, None)
        self.utilities.toolbox = self.utilities.setupToolboxGP(None)

        self.redundancy = Redundancy(self.params)

    def configure(self):
        permitted = ["input", "project", "objective", "experiment", "generations",
                     "seeds", "runs", "bins", "domain", "save", "save_combined", "pause"]
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
                print(self.input+" input type not supported")
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

    def rotateGrid2D(self, population):

        for i in range(len(population)):
            output = ""
            for j in range(len(population[i])):
                output += str(population[i][j])+" "

        rotated_population = np.zeros((len(population[0]), len(population)))

        for i in range(len(rotated_population)):
            output = ""
            for j in range(len(rotated_population[i])):
                output += str(rotated_population[i][j])+" "

        for i in range(len(population)):
            for j in range(len(population[0])):
                rotated_population[j][i] = population[i][j]

        return rotated_population

    def getQualityArray(self, container):
        if self.params.usingNewGrid:
            return container.quality_array()
        else:
            return container.quality_array[..., 0]

    def drawCollapsedDiagram(self, algorithms):

        start_time = round(time.time() * 1000)

        all_verbose = []
        try:
            for algorithm in algorithms:
                container = self.getData(algorithm)
                all_verbose.append(self.getQualityArray(container))
                print(self.utilities.printExtrema(container))
        except FileNotFoundError as e:
            print("\n"+str(e)+"\n")
            return

        end_time = round(time.time() * 1000)
        duration = end_time - start_time
        print("\nLoading time: " +self.utilities.formatDuration(duration)+"\n")

        if self.params.project == "legacy":
            bin_size_inches = 0.2
            x_string = "Rotations"
            y_string = "Movement"
            z_string = "Conditionality"
        else:
            bin_size_inches = 0.04
            x_string = "X"
            y_string = "Y"
            z_string = "Z"

        verbose = all_verbose[0]

        data = self.collapse(verbose)
        all_data = [data]

        fitness_min = 0.0
        fitness_max = 1.8
        colour_map="YlGnBu"
        colour_bar_label="Fitness"
        features_domain = self.domain
        fitness_domain = (fitness_min, fitness_max)

        bins = self.bins

        horizontal_bins = bins[::2]
        horizontal_bins = [3,10]
        vertical_bins = bins[1::2]
        horizontal_bins_total = reduce(mul, horizontal_bins, 1)
        vertical_bins_total = reduce(mul, vertical_bins, 1)
        vertical_bins_total *= len(all_data)

        figure_size = [2.1 + (bins[0] + bins[1] + bins[2]) * bin_size_inches,
                       1.5 + max(bins) * bin_size_inches]

        fig, ax = plt.subplots(nrows=len(all_data), ncols=len(data), figsize=figure_size)

        for d in range(len(all_data)):
            for x in range(len(data)):
                ax = plt.subplot(len(all_data), len(data), x + 1)
                show_y_tick_labels = False
                if x == 0 or self.params.project == "legacy":
                    show_y_tick_labels = True
                if x == 0:
                    ticks = (bins[0],bins[1])
                    features_domain=[self.domain[0],self.domain[1]]
                    title = x_string+" (x) vs "+y_string+" (y)"
                if x == 1:
                    ticks = (bins[1],bins[2])
                    features_domain=[self.domain[1],self.domain[2]]
                    title = y_string+" (x) vs "+z_string+" (y)"
                if x == 2:
                    ticks = (bins[0],bins[2])
                    features_domain=[self.domain[0],self.domain[2]]
                    title = x_string+" (x) vs "+z_string+" (y)"
                cax = self.draw2DSubplot(ax,
                                         data[x],
                                         self.rotateGrid2D(data[x]),
                                         colour_map=colour_map,
                                         features_domain=features_domain,
                                         fitness_domain=fitness_domain[-2:],
                                         title=title, show_y_tick_labels=show_y_tick_labels,
                                         bins=(len(data[0]), len(data[0][0])))

        plt.tight_layout()

        output_filename = "./heatmaps/temp.png"
        if self.save:
            print("\nWriting to "+output_filename+"\n")
            fig.savefig(output_filename)
        else:
            print("\nOutput file: "+output_filename+"\n")

        plt.show()

    def draw2DSubplot(self, ax, data, data_t, colour_map, features_domain, fitness_domain, title, show_y_tick_labels, bins=None):

        vertical_min = fitness_domain[0]
        vertical_max = fitness_domain[1]

        cax = ax.imshow(data_t, interpolation="none", cmap=colour_map, vmin=vertical_min, vmax=vertical_max, aspect="equal")

        if self.params.project == "legacy":
            num_x_ticks = 4
            num_y_ticks = 4
        else:
            num_x_ticks = len(data) / 10
            num_y_ticks = len(data[0]) / 10

        ax.xaxis.set_tick_params(which='major', left=True, bottom=True, top=False, right=False)
        ax.yaxis.set_tick_params(which='major', left=True, bottom=True, top=False, right=False)

        xticks = list(np.arange(0, len(data) + 1, len(data) / num_x_ticks))

        if not show_y_tick_labels or bins[1] == 1:
            yticks = []
        else:
            yticks = list(np.arange(0, len(data[0]) + 1, len(data[0]) / num_y_ticks))

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

        plt.xticks(xticks, rotation='vertical')
        plt.yticks(yticks)

        ax.xaxis.set_tick_params(which='minor', direction="in", left=False, bottom=False, top=False, right=False)
        ax.yaxis.set_tick_params(which='minor', direction="in", left=False, bottom=False, top=False, right=False)

        ax.invert_yaxis()

        ax.autoscale_view()

        return cax

    def collapse(self, data):

        xy = []
        for i in range(self.bins[1]):
            xy.append([])
            for j in range(self.bins[2]):
                xy[-1].append(None)

        for z in range(len(data)):
            for y in range(len(data[0])):
                for x in range(len(data[0][0])):
                    if not math.isnan(data[z][y][x]):
                        xy[y][x] = 1.0

        xz = []
        for i in range(self.bins[0]):
            xz.append([])
            for j in range(self.bins[2]):
                xz[-1].append(None)

        for y in range(len(data[0])):
            for z in range(len(data)):
                for x in range(len(data[0][0])):
                    if not math.isnan(data[z][y][x]):
                        xz[z][x] = 1.0

        yz = []
        for i in range(self.bins[1]):
            yz.append([])
            for j in range(self.bins[0]):
                yz[-1].append(None)

        for x in range(len(data[0][0])):
            for y in range(len(data[0])):
                for z in range(len(data)):
                    if not math.isnan(data[z][y][x]):
                        yz[y][z] = 1.0

        return [xy, xz, yz]

if __name__ == "__main__":

    algorithms = ["qdpy"]

    heatmaps = Heatmaps()

    if not heatmaps.cancelled:
        heatmaps.drawCollapsedDiagram(algorithms)


