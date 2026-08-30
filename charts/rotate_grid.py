import math
import matplotlib.pyplot as plt
import numpy as np
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
        self.params.algorithm = self.repertoire.algorithms[0]
        self.experiment = self.repertoire.experiments[0]

        self.params.indexes = [self.objective]
        self.params.description = self.params.objectives[self.objective]

    def convertToNumpy2D(self, population, rotate = False):

        converted_population = np.zeros((len(population[0]), len(population)))

        for i in range(len(population)):
            for j in range(len(population[0])):
                if rotate:
                    converted_population[j][i] = population[i][j]
                else:
                    converted_population[i][j] = population[i][j]

        return converted_population

    def drawCollapsedDiagram(self):

        start_time = round(time.time() * 1000)

        all_verbose = []
        try:
            container = self.repertoire.getData(self.seeds, self.params.algorithm, self.experiment, self.objective)
            all_verbose.append(self.repertoire.getQualityArray(container))
            print(self.utilities.printExtrema(container))
        except FileNotFoundError as e:
            print("\n"+str(e)+"\n")
            return

        end_time = round(time.time() * 1000)
        duration = end_time - start_time
        print("\nLoading time: " +self.utilities.formatDuration(duration)+"\n")

        bins = self.bins

        if self.small_repertoire:
            bin_size_inches = 0.35
            x_string = "Conditionality"
            y_string = "Rotations"
            z_string = "Movement"
        else:
            x_string = "Purple"
            y_string = "Blue"
            z_string = "Green"
            if bins[0] == 100:  bin_size_inches = 0.03
            elif bins[0] == 50: bin_size_inches = 0.06
            elif bins[0] == 32: bin_size_inches = 0.08
            elif bins[0] >= 13: bin_size_inches = 0.20
            elif bins[0] >= 7:  bin_size_inches = 0.37
            elif bins[0] >= 4:  bin_size_inches = 0.64
            elif bins[0] >= 2:  bin_size_inches = 1.28
            else: bin_size_inches = 0.04

        verbose = all_verbose[0]

        data = self.collapse(verbose)
        all_data = [data]

        fitness_min = 0.0
        fitness_max = 1.8
        colour_map="YlGnBu"
        colour_bar_label="Fitness"
        features_domain = self.domain
        fitness_domain = (fitness_min, fitness_max)

        horizontal_bins = bins[::2]
        horizontal_bins = [3,10]
        vertical_bins = bins[1::2]
        horizontal_bins_total = reduce(mul, horizontal_bins, 1)
        vertical_bins_total = reduce(mul, vertical_bins, 1)
        vertical_bins_total *= len(all_data)

        figure_size = [2.1 + (bins[0] + bins[1] + bins[2]) * bin_size_inches,
                       1.5 + max(bins) * bin_size_inches]

        plt.rcParams['axes.titley'] = 1.02
        fig, ax = plt.subplots(nrows=len(all_data), ncols=len(data), figsize=figure_size)

        for d in range(len(all_data)):
            for x in range(len(data)):

                # without rotating in 2D and old collapse format
                # if x == 0: title = "conditionality (x) vs rotations (y)"
                # if x == 1: title = "conditionality (x) vs movement (y)"
                # if x == 2: title = "movement (x) vs rotations (y)"

                # with 2D rotation and old collapse format
                # if x == 0: title = "rotations (x) vs conditionality (y)"
                # if x == 1: title = "movement (x) vs conditionality (y)"
                # if x == 2: title = "rotations (x) vs movement (y)"

                # new collapse format
                if x == 0: title = "rotations (x) vs movement (y)"
                if x == 1: title = "rotations (x) vs conditionality (y)"
                if x == 2: title = "conditionality (x) vs movement (y)"

                ax = plt.subplot(len(all_data), len(data), x + 1)
                show_y_tick_labels = False
                if x == 0 or self.small_repertoire:
                    show_y_tick_labels = True
                if x == 0:
                    ticks = (bins[0],bins[1])
                    features_domain=[self.domain[0],self.domain[1]]
                    # title = x_string+" (x) vs "+y_string+" (y)" # without 2D rotation
                    # title = y_string+" (x) vs "+x_string+" (y)" # with 2D rotation
                    title = y_string+" (x) vs "+z_string+" (y)"
                if x == 1:
                    ticks = (bins[1],bins[2])
                    features_domain=[self.domain[1],self.domain[2]]
                    # title = x_string+" (x) vs "+z_string+" (y)" # without 2D rotation
                    # title = z_string+" (x) vs "+x_string+" (y)" # with 2D rotation
                    title = y_string+" (x) vs "+x_string+" (y)"
                if x == 2:
                    ticks = (bins[2],bins[0])
                    features_domain=[self.domain[2],self.domain[0]]
                    # title = y_string+" (x) vs "+z_string+" (y)" # without 2D rotation
                    # title = z_string+" (x) vs "+y_string+" (y)" # with 2D rotation
                    title = z_string+" (x) vs "+x_string+" (y)"
                cax = self.draw2DSubplot(ax,
                                         data[x],
                                         self.convertToNumpy2D(data[x]),
                                         colour_map=colour_map,
                                         features_domain=features_domain,
                                         fitness_domain=fitness_domain[-2:],
                                         title=title, show_y_tick_labels=show_y_tick_labels,
                                         bins=ticks)

        plt.tight_layout()

        image_filename = "./heatmaps/temp.png"
        if self.save:
            print("\nWriting to "+image_filename+"\n")
            fig.savefig(image_filename)
        else:
            print("\nOutput file: "+image_filename+"\n")

        if self.show:
            plt.show()

    def draw2DSubplot(self, ax, data, data_t, colour_map, features_domain, fitness_domain, title, show_y_tick_labels, bins=None):

        vertical_min = fitness_domain[0]
        vertical_max = fitness_domain[1]
        dst_bins = bins[0]

        cax = ax.imshow(data_t, interpolation="none", cmap=colour_map, vmin=vertical_min, vmax=vertical_max, aspect="equal")

        if self.small_repertoire:
            num_x_ticks = 4
            num_y_ticks = 4
        elif dst_bins in [8, 16]:
            num_x_ticks = math.floor(dst_bins / 2)
            num_y_ticks = math.floor(dst_bins / 2)
        elif dst_bins == 32:
            num_x_ticks = math.floor(dst_bins / 4)
            num_y_ticks = math.floor(dst_bins / 4)
        else:
            num_x_ticks = 8
            num_y_ticks = 8

        ax.xaxis.set_tick_params(which='major', left=True, bottom=True, top=False, right=False)
        ax.yaxis.set_tick_params(which='major', left=True, bottom=True, top=False, right=False)

        xticks = list(np.arange(0, len(data) + 1, len(data) / num_x_ticks))

        if not show_y_tick_labels or bins[1] == 1:
            yticks = []
        else:
            yticks = list(np.arange(0, len(data[0]) + 1, len(data[0]) / num_y_ticks))

        # uncomment to hide tick labels
        # xticks = []
        # yticks = []

        ax.set_xticks(xticks)
        ax.set_yticks(yticks)

        # comment to hide chart titles
        ax.set_title(title,fontsize=18)

        if features_domain[0][1] < 2.0:
            features_domain[0] = (features_domain[0][0], 1.12)
            features_domain[1] = (features_domain[1][0], 1.12)
        else:
            features_domain[0] = (features_domain[0][0], 2.24)
            features_domain[1] = (features_domain[1][0], 2.24)

        delta_x = features_domain[0][1] - features_domain[0][0]
        delta_y = features_domain[1][1] - features_domain[1][0]

        if self.small_repertoire:
            ax.set_xticklabels([f'{round(float(x / float(len(data))    * delta_x + features_domain[0][0]), 2):1.0f}' for x in xticks], fontsize=10)
            ax.set_yticklabels([f'{round(float(y / float(len(data[0])) * delta_y + features_domain[1][0]), 2):1.0f}' for y in yticks], fontsize=10)
        else:
            ax.set_xticklabels([f'{round(float(x / float(len(data))    * delta_x + features_domain[0][0]), 2):1.1f}' for x in xticks], fontsize=14)
            ax.set_yticklabels([f'{round(float(y / float(len(data[0])) * delta_y + features_domain[1][0]), 2):1.1f}' for y in yticks], fontsize=14)

        plt.xticks(xticks, rotation='vertical')
        plt.yticks(yticks)

        ax.xaxis.set_tick_params(which='minor', direction="in", left=False, bottom=False, top=False, right=False)
        ax.yaxis.set_tick_params(which='minor', direction="in", left=False, bottom=False, top=False, right=False)

        ax.invert_yaxis()
        ax.autoscale_view()

        return cax

    def collapse(self, data):

        # x = conditionality
        # y = rotations
        # z = movement

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

        yx = []
        for i in range(self.bins[1]):
            yx.append([])
            for j in range(self.bins[2]):
                yx[-1].append(None)

        for z in range(len(data)):
            for x in range(len(data[0][0])):
                for y in range(len(data[0])):
                    if not math.isnan(data[z][y][x]):
                        yx[x][y] = 1.0

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

        zx = []
        for i in range(self.bins[0]):
            zx.append([])
            for j in range(self.bins[2]):
                zx[-1].append(None)

        for y in range(len(data[0])):
            for x in range(len(data[0][0])):
                for z in range(len(data)):
                    if not math.isnan(data[z][y][x]):
                        zx[x][z] = 1.0

        yz = []
        for i in range(self.bins[1]):
            yz.append([])
            for j in range(self.bins[0]):
                yz[-1].append(None)

        for x in range(len(data[0][0])):
            for y in range(len(data[0])):
                for z in range(len(data)):
                    if not math.isnan(data[z][y][x]):
                        yz[z][y] = 1.0

        # return [xy, xz, yz]
        # returns rotations vs movement          yz
        #         rotations vs conditionality    yx
        #         conditionality vs movement     xz

        return [yz, yx, zx]

if __name__ == "__main__":

    heatmaps = Heatmaps()

    if not heatmaps.cancelled:
        heatmaps.drawCollapsedDiagram()


