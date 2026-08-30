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
from redundancy import Redundancy
from repertoire import Repertoire
from utilities import Utilities

from functools import reduce
from operator import mul
from qdpy.utils import is_iterable

import matplotlib
import matplotlib as mpl


class Heatmaps():

    def __init__(self):

        self.params = eaParams()
        self.params.is_qdpy = True

        self.repertoire = Repertoire(self.params)
        self.repertoire.configure()
        self.cancelled = self.repertoire.cancelled
        print()

        self.algorithms = self.repertoire.algorithms
        self.experiments = self.repertoire.experiments

        if len(self.algorithms) != len(self.experiments):
            print("\nAlgorithms and experiments don't match\n")
            print(str(len(self.algorithms))+" algorithms,  "+str(len(self.experiments))+" experiments\n")
            self.cancelled = True
            return

        self.utilities = Utilities(self.params, None)

        if self.params.project == "heterogeneous_genetic_algorithm":
            self.utilities.toolbox = self.utilities.setupToolboxGA(None, None, None, None, None)
            self.redundancy = None
        else:
            self.utilities.toolbox = self.utilities.setupToolboxGP(None)
            self.redundancy = Redundancy(self.params)

        self.repertoire.setUp(self.utilities, self.redundancy)

        self.objective = self.repertoire.objective
        self.bins = self.repertoire.dst_bins
        self.domain = self.repertoire.domain
        self.small_repertoire = self.repertoire.isSmallRepertoire()

        self.save = self.repertoire.save
        self.show = self.repertoire.show

        self.seeds = self.repertoire.seedsList()
        self.algorithm = self.repertoire.algorithms[0]
        self.experiment = self.repertoire.experiments[0]

        self.params.algorithm = self.algorithm
        self.params.indexes = self.utilities.getExperimentIndexes(self.objective, self.algorithm)
        self.params.description = self.utilities.getExperimentDescription(self.objective, self.algorithm)

    def flattenFitnessScores(self, data):
        for x in range(len(data)):
            for y in range(len(data[0])):
                for z in range(len(data[0][0])):
                    for w in range(len(data[0][0][0])):
                        if not math.isnan(data[x][y][z][w]):
                            data[x][y][z][w] = 1.0

    def rotateDomain(self):
        if self.small_repertoire:
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

        if self.small_repertoire:
            rotated_population = np.zeros((population.shape[2], population.shape[1], population.shape[0]))
        else:
            rotated_population = np.zeros((population.shape[0], population.shape[1], population.shape[2]))

        for i in range(population.shape[0]):
            for j in range(population.shape[1]):
                for k in range(population.shape[2]):
                    if self.small_repertoire:
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
        title = str("%1.2f" % start)+"  -  "+str("%1.2f" % end)
        return title

    def drawHeatmap(self):

        start_time = round(time.time() * 1000)

        all_data = []
        try:
            for i in range(len(self.algorithms)):
                container = self.repertoire.getData(self.seeds, self.algorithms[i], self.experiments[i], self.objective)
                quality_array = self.repertoire.getQualityArray(container)
                all_data.append(self.rotateGrid(quality_array))
                print("Population size: "+str(len(container.values())))
                print(self.utilities.printExtrema(container))
        except FileNotFoundError as e:
            print("\n"+str(e)+"\n")
            return

        end_time = round(time.time() * 1000)
        duration = end_time - start_time
        print("\nLoading time: " +self.utilities.formatDuration(duration)+"\n")
        start_time = round(time.time() * 1000)

        if self.small_repertoire:

            fitness_min = -0.5
            fitness_max = 1.0
            for data in all_data:
                fitness_min = np.max([fitness_min, np.nanmin(data)])
                fitness_max = np.min([fitness_max, np.nanmax(data)])
            fitness_min -= 0.01
            bin_size_inches = 0.2
            ticks = 4
            self.rotateDomain()

        else:

            fitness_min = 0.0
            fitness_max = 1.8

            if self.bins[0]   <= 4:  bin_size_inches = 0.4
            elif self.bins[0] <= 8:  bin_size_inches = 0.2
            elif self.bins[0] <= 16: bin_size_inches = 0.1
            elif self.bins[0] <= 24: bin_size_inches = 0.133
            elif self.bins[0] <= 32: bin_size_inches = 0.1
            else: bin_size_inches = 0.04

            if self.bins[0]   <= 4:  ticks = 5
            elif self.bins[0] <= 8:  ticks = 8
            elif self.bins[0] <= 16: ticks = 8
            elif self.bins[0] <= 24: ticks = 4
            elif self.bins[0] <= 32: ticks = 4
            else: ticks = 5

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

        sections = []
        sections.append({"start" : 0, "end" : 2, "interval" : 1})

        for section in sections:

            section_start = section["start"]
            section_end = section["end"]
            section_interval = section["interval"]
            section_size = (section_end - section_start) / section_interval

            if section_start >= section_end:
                print("Section start must be less than section end")
                return

            bins = (int(section_size), 1, bins[2], bins[3])
            horizontal_bins = bins[::2]
            vertical_bins = bins[1::2]
            horizontal_bins_total = reduce(mul, horizontal_bins, 1)
            vertical_bins_total = reduce(mul, vertical_bins, 1)
            vertical_bins_total *= len(all_data)

            figure_size = [3.1 + horizontal_bins_total * bin_size_inches, 1.5 + vertical_bins_total * bin_size_inches]

            fig, ax = plt.subplots(nrows=len(all_data), ncols=bins[0], figsize=figure_size)

            for x in range(bins[0]):
                interval = x * section_interval
                for y in range(len(all_data)):
                    data = all_data[y]
                    ax = plt.subplot(len(all_data), bins[0], y * bins[0] + x + 1)
                    z_index = section_start + interval
                    show_y_tick_labels = False
                    if x == 0 and self.small_repertoire:
                        ax.set_ylabel(self.algorithms[y].upper(), fontsize=15, rotation='horizontal')
                    if x == 0 or self.small_repertoire:
                        ax.yaxis.set_label_coords(-0.7,0.4)
                        show_y_tick_labels = True
                    cax = self.drawSubplot(ax,
                                           data_t = data[section_start + interval, 0, 0:bins[2], 0:bins[3]].T,
                                           colour_map=colour_map,
                                           features_domain=features_domain[-2:],
                                           fitness_domain=fitness_domain[-2:],
                                           z_index=z_index, bins=(bins[2], bins[3]),
                                           ticks=ticks, show_y_tick_labels=show_y_tick_labels)

            plt.tight_layout()
            if self.bins[0] <= 8:
                self.drawColourBar(fig, ax, cax, figure_size)

            output_filename = "./heatmaps/enucc/"+self.params.project+"/cross-sections/"
            output_filename += "bins-"+str(self.bins[0])+"-"
            output_filename += self.experiments[0]+"/"
            output_filename += "sections-"+str(section_start)+"-"+str(section_end)+".png"

            if self.save:
                print("\nWriting image to "+output_filename+"\n")
                fig.savefig(output_filename)
            else:
                print("\nImage file: "+output_filename+"\n")

            end_time = round(time.time() * 1000)
            duration = end_time - start_time
            print("\nProcessing time: " +self.utilities.formatDuration(duration)+"\n")

            if self.show:
                plt.show()

    def drawSubplot(self, ax, data_t, colour_map, features_domain, fitness_domain, z_index=0, bins=None, ticks = 4, show_y_tick_labels = False):

        vertical_min = fitness_domain[0]
        if np.isnan(vertical_min) or np.isinf(vertical_min):
            vertical_min = np.nanmin(data)

        vertical_max = fitness_domain[1]
        if np.isnan(vertical_max) or np.isinf(vertical_max):
            vertical_max = np.nanmax(data)

        cax = ax.imshow(data_t, interpolation="none", cmap=colour_map, vmin=vertical_min, vmax=vertical_max, aspect="equal")

        ax.set_title(self.writeZTitle(z_index),fontsize=20)

        ax.xaxis.set_tick_params(which='major', left=True, bottom=True, top=False, right=False)
        ax.yaxis.set_tick_params(which='major', left=True, bottom=True, top=False, right=False)

        ax.xaxis.set_tick_params(which='minor', direction="in", left=False, bottom=False, top=False, right=False)
        ax.yaxis.set_tick_params(which='minor', direction="in", left=False, bottom=False, top=False, right=False)

        xticks = list(np.arange(0, len(data_t) + 1, len(data_t) / ticks))

        if not show_y_tick_labels or bins[1] == 1:
            yticks = []
        else:
            yticks = list(np.arange(0, len(data_t[0]) + 1, len(data_t[0]) / ticks))

        ax.set_xticks(xticks)
        ax.set_yticks(yticks)

        delta_x = features_domain[0][1] - features_domain[0][0]
        delta_y = features_domain[1][1] - features_domain[1][0]

        if self.small_repertoire:
            ax.set_xticklabels([f'{round(float(x / float(len(data_t))    * delta_x + features_domain[0][0]), 2):1.0f}' for x in xticks], fontsize=10)
            ax.set_yticklabels([f'{round(float(y / float(len(data_t[0])) * delta_y + features_domain[1][0]), 2):1.0f}' for y in yticks], fontsize=10)
        else:
            ax.set_xticklabels([f'{round(float(x / float(len(data_t))    * delta_x + features_domain[0][0]), 2):1.2f}' for x in xticks], fontsize=20)
            ax.set_yticklabels([f'{round(float(y / float(len(data_t[0])) * delta_y + features_domain[1][0]), 2):1.2f}' for y in yticks], fontsize=20)

        if bins[1] == 1:
            yticks = []

        plt.xticks(xticks, rotation='vertical')
        plt.yticks(yticks)

        ax.invert_yaxis()

        ax.autoscale_view()

        return cax

if __name__ == "__main__":

    heatmaps = Heatmaps()

    if not heatmaps.cancelled:
        heatmaps.drawHeatmap()


