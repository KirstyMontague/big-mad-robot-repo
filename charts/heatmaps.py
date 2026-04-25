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
        self.params.is_qdpy = True
        self.objective = self.params.indexes[0]
        self.generations = self.params.generations
        self.seed = 0
        self.bins = [8,8,8]
        self.domain = [(-0.15, 0.15), (-0.5, 0.5), (-0.5, 0.5)]
        self.save = self.params.saveOutput

        self.cancelled = False
        self.configure()

        self.utilities = Utilities(self.params, None)
        self.utilities.toolbox = self.utilities.setupToolboxGP(self.selTournament)

        self.redundancy = Redundancy(self.params)

    def configure(self):
        permitted = ["project", "objective", "experiment", "generations", "seed", "bins", "domain", "save"]
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

        if data[0] == "project": self.params.project = data[1]
        if data[0] == "experiment" and len(data) > 1: self.experiment = data[1]
        if data[0] == "generations": self.generations = int(data[1])
        if data[0] == "seed": self.seed = int(data[1])
        if data[0] == "save": self.save = True if data[1] == "True" else False


    def getGpData(self, container):

        path = self.params.input_path+"/gp/"+self.experiment+"/"+self.objective_name
        checkpoint_input_filename = path+"/"+str(self.seed)+"/checkpoint-"+self.objective_name+"-"+str(self.seed)+"-"+str(self.generations)+"-"+self.objective_name+".txt"
        container = self.utilities.updateContainerFromString(self.redundancy, self.utilities.toolbox, container, checkpoint_input_filename)

        return container

    def getMtData(self, container, compatible_objectives):

        algorithm_type = "mtc" if compatible_objectives else "mti"
        description = self.utilities.getExperimentDescription(self.objective, algorithm_type)

        input_path = self.params.shared_path+"/gp/"+self.experiment+"/"+description
        checkpoint_input_filename = input_path+"/"+str(self.seed)+"/checkpoint-"+description+"-"+str(self.seed)+"-"+str(self.generations)+"-"+self.objective_name+".txt"
        container = self.utilities.updateContainerFromString(self.redundancy, self.utilities.toolbox, container, checkpoint_input_filename)

        return container

    def getQdpyData(self, container):

        path = self.params.input_path+"/qdpy/"+self.experiment+"/"+self.objective_name
        checkpoint_input_filename = path+"/"+str(self.seed)+"/checkpoint-"+self.objective_name+"-"+str(self.seed)+"-"+str(self.generations)+"-"+self.objective_name+".txt"
        container = self.utilities.updateContainerFromString(self.redundancy, self.utilities.toolbox, container, checkpoint_input_filename)

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
        title = str("%.2f" % start)+"  -  "+str("%.2f" % end)
        return title

    def drawHeatmap(self, algorithms):

        all_data = []
        for algorithm in algorithms:
            all_data.append(self.getCsvData(algorithm))

        fitness_min = -0.5
        fitness_max = 1.0
        # for data in all_data:
            # fitness_min = np.min([fitness_min, np.nanmin(data)])
            # fitness_max = np.max([fitness_max, np.nanmax(data)])

        colour_map="YlGnBu"
        colour_bar_label="Fitness"
        features_domain = self.domain
        fitness_domain = (fitness_min, fitness_max)
        ticks = 4
        bin_size_inches = 0.2

        if len(all_data[0].shape) % 2 == 1:
            for i in range(len(all_data)):
                all_data[i] = all_data[i].reshape((all_data[i].shape[0], 1) + all_data[i].shape[1:])
            features_domain = (features_domain[0], (0., 0.)) + tuple(features_domain[1:])
        bins = all_data[0].shape

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
                if x == 0:
                    ax.set_ylabel(algorithms[y].upper(), fontsize=15, rotation='horizontal')
                    ax.yaxis.set_label_coords(-0.5,0.4)
                cax = self.drawSubplot(ax,
                                       data[x, 0, 0:bins[2], 0:bins[3]],
                                       data_t = data[x, 0, 0:bins[2], 0:bins[3]].T,
                                       colour_map=colour_map,
                                       features_domain=features_domain[-2:],
                                       fitness_domain=fitness_domain[-2:],
                                       z_index=x, bins=(bins[2], bins[3]), ticks=ticks)


        plt.tight_layout()
        self.drawColourBar(fig, ax, cax, figure_size)

        output_filename = "./heatmaps/"+self.objective_name+".png"
        output_filename = "./heatmaps/temp.png"
        if self.save:
            print("\nWriting to "+output_filename+"\n")
            fig.savefig(output_filename)
        else:
            print("\nOutput file: "+output_filename+"\n")

        plt.show()

    def drawSubplot(self, ax, data, data_t, colour_map, features_domain, fitness_domain, z_index=0, bins=None, ticks = 4):

        vertical_min = fitness_domain[0]
        if np.isnan(vertical_min) or np.isinf(vertical_min):
            vertical_min = np.nanmin(data)

        vertical_max = fitness_domain[1]
        if np.isnan(vertical_max) or np.isinf(vertical_max):
            vertical_max = np.nanmax(data)

        cax = ax.imshow(data_t, interpolation="none", cmap=colour_map, vmin=vertical_min, vmax=vertical_max, aspect="equal")

        num_x_ticks = 5
        num_y_ticks = 5

        ax.set_title(self.writeZTitle(z_index),fontsize=10)

        ax.xaxis.set_tick_params(which='major', left=True, bottom=True, top=False, right=False)
        ax.yaxis.set_tick_params(which='major', left=True, bottom=True, top=False, right=False)

        ax.xaxis.set_tick_params(which='minor', direction="in", left=False, bottom=False, top=False, right=False)
        ax.yaxis.set_tick_params(which='minor', direction="in", left=False, bottom=False, top=False, right=False)

        # xticks = list(np.arange(0, data.shape[0] + 1, data.shape[0] / num_x_ticks))
        # yticks = list(np.arange(0, data.shape[1] + 1, data.shape[1] / num_y_ticks))
        xticks = list(np.arange(0, len(data)    + 1, len(data)    / num_x_ticks))
        yticks = list(np.arange(0, len(data[0]) + 1, len(data[0]) / num_y_ticks))

        ax.set_xticks(xticks)
        ax.set_yticks(yticks)

        delta_x = features_domain[0][1] - features_domain[0][0]
        delta_y = features_domain[1][1] - features_domain[1][0]

        # ax.set_xticklabels([f'{round(float(x / float(data.shape[0]) * delta_x + features_domain[0][0]), 2):1.2f}' for x in xticks], fontsize=10)
        # ax.set_yticklabels([f'{round(float(y / float(data.shape[1]) * delta_y + features_domain[1][0]), 2):1.2f}' for y in yticks], fontsize=10)
        ax.set_xticklabels([f'{round(float(x / float(len(data))    * delta_x + features_domain[0][0]), 2):1.2f}' for x in xticks], fontsize=10)
        ax.set_yticklabels([f'{round(float(y / float(len(data[0])) * delta_y + features_domain[1][0]), 2):1.2f}' for y in yticks], fontsize=10)


        if bins[1] == 1:
            yticks = []

        plt.xticks(xticks, rotation='vertical')
        plt.yticks(yticks)

        ax.invert_yaxis()

        ax.autoscale_view()

        return cax

    def selTournament(self):
        return []

if __name__ == "__main__":

    # algorithms = ["gp", "mtc", "mti", "qd"]
    algorithms = ["qd"]

    heatmaps = Heatmaps()

    if not heatmaps.cancelled:
        heatmaps.drawHeatmap(algorithms)


