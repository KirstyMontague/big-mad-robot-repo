import math
import matplotlib.pyplot as plt
import numpy as np
import pickle

import sys
sys.path.insert(0, '..')

from containers import *
from analysis import Analysis
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
        self.analyse = Analysis()
        self.params = eaParams()
        self.utilities = Utilities(self.params, None)
        self.redundancy = Redundancy(self.params)

        self.params.is_qdpy = True
        self.utilities.setupToolbox(self.selTournament)

        self.objective = self.params.indexes[0]
        self.generations = self.params.generations
        self.seed = 0
        self.bins = [8,8,8]
        self.domain = [(-0.5, 0.5), (-0.5, 0.5), (-0.5, 0.5)]
        self.save = self.params.saveOutput

        self.cancelled = False
        self.configure()


    def configure(self):
        permitted = ["objective", "experiment", "generations", "seed", "bins", "domain", "save"]
        with open(self.params.local_path+"/heatmaps.txt", 'r') as f:
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

        if data[0] == "objective":
            self.objective = int(data[1])
            self.objective_name = self.params.objectives[self.objective]

        if data[0] == "bins" and len(data) > 1:
            self.bins = []
            for b in data[1:]:
                self.bins.append(int(b))

        if data[0] == "domain" and len(data) > 1:
            self.domain = []
            for i in range(1, len(data), 2):
                self.domain.append((float(data[i]), float(data[i+1])))
            print(self.domain)

        if data[0] == "experiment" and len(data) > 1: self.experiment = data[1]
        if data[0] == "generations": self.generations = int(data[1])
        if data[0] == "seed": self.seed = int(data[1])
        if data[0] == "save": self.save = True if data[1] == "True" else False


    def getGpData(self, container):

        path = self.params.input_path+"/gp/"+self.experiment+"/"+self.objective_name
        checkpoint_input_filename = path+"/"+str(self.seed)+"/checkpoint-"+self.objective_name+"-"+str(self.seed)+"-"+str(self.generations)+"-"+self.objective_name+".txt"
        container = self.utilities.updateContainerFromString(self.redundancy, container, checkpoint_input_filename)

        return container

    def getMtData(self, container, compatible_objectives):

        algorithm_type = "mtc" if compatible_objectives else "mti"
        description = self.utilities.getExperimentDescription(self.objective, algorithm_type)

        input_path = self.params.shared_path+"/gp/"+self.experiment+"/"+description
        checkpoint_input_filename = input_path+"/"+str(self.seed)+"/checkpoint-"+description+"-"+str(self.seed)+"-"+str(self.generations)+"-"+self.objective_name+".txt"
        container = self.utilities.updateContainerFromString(self.redundancy, container, checkpoint_input_filename)

        return container

    def getQdpyData(self, container):

        path = self.params.input_path+"/qdpy/"+self.experiment+"/"+self.objective_name
        checkpoint_input_filename = path+"/"+str(self.seed)+"/checkpoint-"+self.objective_name+"-"+str(self.seed)+"-"+str(self.generations)+"-"+self.objective_name+".txt"
        container = self.utilities.updateContainerFromString(self.redundancy, container, checkpoint_input_filename)

        return container

    def getCsvData(self, algorithm_name):

        container = (Grid(shape = self.bins,
                          max_items_per_bin = 1,
                          fitness_domain = [(0.,1.0),],
                          features_domain = self.domain,
                          storage_type=list))

        if algorithm_name == "gp": self.getGpData(container)
        if algorithm_name == "mtc": self.getMtData(container, True)
        if algorithm_name == "mti": self.getMtData(container, False)
        if algorithm_name == "qd": self.getQdpyData(container)
        print(self.utilities.getExtrema(container))

        return self.rotateGrid(container.quality_array[..., 0])


    def rotateGrid(self, population):

        for i in range(len(population)):
            for j in range(len(population[i])):
                output = ""
                for k in range(len(population[i][j])):
                    output += str(population[i,j,k])+" "
                # print(output+"\n")
        print()

        # population shape = movement, rotations (x), conditionality (y)
        # population shape = density, nest, food

        # rotated_population = np.zeros((population.shape[2], population.shape[1], population.shape[0]))
        rotated_population = np.zeros((population.shape[0], population.shape[1], population.shape[2]))

        for i in range(population.shape[0]):
            for j in range(population.shape[1]):
                for k in range(population.shape[2]):
                    # rotated_population[i,j,k] = population[k,j,i]
                    rotated_population[i,j,k] = population[i,j,k]

        # rotated_population shape = conditionality, rotations (x), movement (y)
        # rotated_population shape = food, nest, density

        return rotated_population

    def rotateGrid2D(self, population):

        for i in range(len(population)):
            output = ""
            for j in range(len(population[i])):
                output += str(population[i][j])+" "
            # print(output+"\n")
        # print()

        rotated_population = np.zeros((len(population[0]), len(population)))

        for i in range(len(rotated_population)):
            output = ""
            for j in range(len(rotated_population[i])):
                output += str(rotated_population[i][j])+" "
            # print(output+"\n")
        # print()

        for i in range(len(population)):
            for j in range(len(population[0])):
                # rotated_population[i,j,k] = population[k,j,i]
                rotated_population[j][i] = population[i][j]

        return rotated_population

    def drawColourBar(self, fig, ax, cax, figure_size):

        fig.subplots_adjust(right=0.9, wspace=0.40)
        colour_bar_axes = fig.add_axes([0.92, 0.3, 0.01, 0.4])
        cbar = fig.colorbar(cax, cax=colour_bar_axes, format="%.2f")
        cbar.ax.tick_params(labelsize=12)

    def writeZTitle(self, index):
        domain = self.domain[0]
        domain_max = domain[1] - domain[0]
        title = ((domain_max / self.bins[0]) * index) + domain[0]
        return str("%.2f" % title)

    def drawCollapsedDiagram(self, algorithms):

        all_verbose = []
        for algorithm in algorithms:
            all_verbose.append(self.getCsvData(algorithm))

        verbose = all_verbose[0]

        data = self.collapse(verbose)
        all_data = [data]

        fitness_min = -1.0
        fitness_max = 1.0
        colour_map="YlGnBu"
        colour_bar_label="Fitness"
        features_domain = self.domain
        fitness_domain = (fitness_min, fitness_max)
        ticks = 4
        bin_size_inches = 0.2

        bins = self.bins

        horizontal_bins = bins[::2]
        print(horizontal_bins)
        horizontal_bins = [3,10]
        vertical_bins = bins[1::2]
        horizontal_bins_total = reduce(mul, horizontal_bins, 1)
        vertical_bins_total = reduce(mul, vertical_bins, 1)
        vertical_bins_total *= len(all_data)

        figure_size = [2.1 + (bins[0] + bins[1] + bins[2]) * bin_size_inches,
                       1.0 + max(bins) * bin_size_inches]
        print(figure_size)

        fig, ax = plt.subplots(nrows=len(all_data), ncols=len(data), figsize=figure_size)

        for d in range(len(all_data)):
            for x in range(len(data)):
                ax = plt.subplot(len(all_data), len(data), x + 1)
                if x == 0:
                    ax.set_ylabel(algorithms[0].upper(), fontsize=15, rotation='horizontal')
                    ax.yaxis.set_label_coords(-0.3,0.4)
                    ticks = (bins[1],bins[2])
                    features_domain=self.domain[-2:]
                    title = "nest (x) vs food (y)"
                if x == 1:
                    ticks = (bins[0],bins[2])
                    features_domain=[self.domain[0],self.domain[2]]
                    title = "density (x) vs food (y)"
                if x == 2:
                    ticks = (bins[0],bins[1])
                    features_domain=[self.domain[1],self.domain[0]]
                    title = "nest (x) vs density (y)"
                cax = self.draw2DSubplot(ax,
                                         data[x],
                                         self.rotateGrid2D(data[x]),
                                         colour_map=colour_map,
                                         features_domain=features_domain,
                                         fitness_domain=fitness_domain[-2:],
                                         title=title, bins=(len(data[0]), len(data[0][0])), ticks=ticks)

        plt.tight_layout()
        self.drawColourBar(fig, ax, cax, figure_size)

        output_filename = "./heatmaps/objectives_cast_to_grid_arena_2/seed-"+str(self.seed)+".png"
        if self.save:
            print("\nWriting to "+output_filename+"\n")
            fig.savefig(output_filename)
        else:
            print("\nOutput file: "+output_filename+"\n")

        plt.show()

    def draw2DSubplot(self, ax, data, data_t, colour_map, features_domain, fitness_domain, title, bins=None, ticks = 4):

        vertical_min = fitness_domain[0]
        vertical_max = fitness_domain[1]

        cax = ax.imshow(data_t, interpolation="none", cmap=colour_map, vmin=vertical_min, vmax=vertical_max, aspect="equal")

        num_x_ticks = len(data) / 4
        num_y_ticks = len(data[0]) / 4

        ax.set_title(title,fontsize=14)

        ax.xaxis.set_tick_params(which='major', left=True, bottom=True, top=False, right=False)
        ax.yaxis.set_tick_params(which='major', left=True, bottom=True, top=False, right=False)

        xticks = list(np.arange(0, len(data) + 1, len(data) / num_x_ticks))
        yticks = list(np.arange(0, len(data[0]) + 1, len(data[0]) / num_y_ticks))
        ax.set_xticks(xticks)
        ax.set_yticks(yticks)

        delta_x = features_domain[0][1] - features_domain[0][0]
        delta_y = features_domain[1][1] - features_domain[1][0]

        ax.set_xticklabels([f'{round(float(x / float(len(data)) * delta_x + features_domain[0][0]), 2):1.2f}' for x in xticks], fontsize=12)
        ax.set_yticklabels([f'{round(float(y / float(len(data[0])) * delta_y + features_domain[1][0]), 2):1.2f}' for y in yticks], fontsize=12)

        if bins[1] == 1:
            yticks = []

        plt.xticks(xticks, rotation='vertical')
        plt.yticks(yticks)

        ax.invert_yaxis()

        ax.xaxis.set_tick_params(which='minor', direction="in", left=False, bottom=False, top=False, right=False)
        ax.yaxis.set_tick_params(which='minor', direction="in", left=False, bottom=False, top=False, right=False)

        ax.autoscale_view()

        return cax

    def collapse(self, data):

        xy = []
        for i in range(self.bins[1]):
            xy.append([])
            for j in range(self.bins[2]):
                xy[-1].append(False)

        for z in range(len(data)):
            for y in range(len(data[0])):
                for x in range(len(data[0][0])):
                    if not math.isnan(data[z][y][x]):
                        xy[y][x] = True

        xz = []
        for i in range(self.bins[0]):
            xz.append([])
            for j in range(self.bins[2]):
                xz[-1].append(False)

        for y in range(len(data[0])):
            for z in range(len(data)):
                for x in range(len(data[0][0])):
                    if not math.isnan(data[z][y][x]):
                        xz[z][x] = True

        yz = []
        for i in range(self.bins[1]):
            yz.append([])
            for j in range(self.bins[0]):
                yz[-1].append(False)

        for x in range(len(data[0][0])):
            for y in range(len(data[0])):
                for z in range(len(data)):
                    if not math.isnan(data[z][y][x]):
                        yz[y][z] = True

        return [xy, xz, yz]

    def selTournament(self):
        return []

if __name__ == "__main__":

    algorithms = ["qd"]

    heatmaps = Heatmaps()

    if not heatmaps.cancelled:
        heatmaps.drawCollapsedDiagram(algorithms)


