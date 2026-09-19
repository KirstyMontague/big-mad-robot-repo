import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib as mpl

from functools import reduce
from operator import mul

import numpy as np
import math
import re
import subprocess

import sys
sys.path.insert(0, '..')

# from containers import *
from grid import Grid

from deap import tools

from params import eaParams
from redundancy import Redundancy
from utilities import Utilities


class Chromosome():

    def __init__(self, params):

        self.params = params
        self.params.is_qdpy = True
        self.params.using_repertoire = False

        self.utilities = Utilities(self.params, None)

        if self.params.repertoire_size <= 512:
            self.redundancy = Redundancy(self.params)
        else:
            print("Repertoire too large: "+str(self.params.repertoire_size)+"\n(derived from params.repertoire_size)")
            return

        self.gp_toolbox = self.utilities.setupToolboxGP(None)

        if not self.utilities.checkContainerSize():
            return

        self.params.makePaths()

        repertoire_path = self.params.shared_path+"/ga/"+self.params.experiments[0]+"/foraging"
        repertoire_file = repertoire_path+"/foraging-"+str(self.params.src_bins[0])+"-bins.txt"

        self.repertoire = self.utilities.createContainer(self.params.src_bins,
                                                         self.params.src_domain,
                                                         self.params.max_items_per_bin)

        try:
            self.params.console("\nReading from "+repertoire_file)
            self.utilities.updateContainerFromString(self.redundancy, self.gp_toolbox,
                                                     self.repertoire, repertoire_file, 2000, 0, 0)

        except FileNotFoundError as e:
            self.params.cancelled = True
            print("\n"+str(e)+"\n")
            return

        self.params.console("")
        flat_indexes = []
        grid_indexes = []

        if self.params.usingNewGrid:
            flat_indexes.extend(range(len(self.repertoire.items())))
            grid_indexes = [key for key, value in self.repertoire.items()]
            self.params.console("repertoire size "+str(len(self.repertoire.values()))+"\n")
        else:
            container = self.repertoire.solutions.items()
            flat_indexes = [self.repertoire.items.index(inds[0]) for index, inds in container if len(inds) > 0]
            grid_indexes = [self.repertoire.index_grid(inds[0].features) for index, inds in container if len(inds) > 0]
            self.params.console("repertoire size "+str(len(self.repertoire))+"\n")

        self.utilities.toolbox = self.utilities.setupToolboxGA(self.repertoire, None, None, flat_indexes, grid_indexes)

        max_per_axis = [0,0,0]
        for index in grid_indexes:
            for i in range(len(index)):
                if index[i] > max_per_axis[i]:
                    max_per_axis[i] = index[i]
        print("max per axis "+str(max_per_axis)+"\n")

    def getChromomesFromCSV(self, filename):

        print("Loading from: "+filename+"\n")

        try:
            with open(filename, "r") as f:

                chromosomes = []

                for line in f:

                    data = []
                    sections = line.split("\"")
                    if len(sections) > 1:
                        chromosomes.append(sections[1])

        except FileNotFoundError as e:
            self.params.cancelled = True
            print(str(e)+"\n")
            return

        return chromosomes

    def getSwarms(self):

        if self.params.bias != -1:
            experiment = self.params.experiments[1]+"-bias-"+str(self.params.bias)
        else:
            experiment = self.params.experiments[1]

        csv_path = self.params.input_path+"/ga/"+experiment+"/foraging"
        csv_file = csv_path+"/bins-"+str(self.params.src_bins[0])+"/best"+str(self.params.generations)+".csv"

        ga_chromosomes = self.getChromomesFromCSV(csv_file)
        if ga_chromosomes is None:
            return []

        swarms = []

        for chromosome in ga_chromosomes:

            numbers = re.sub(r'\D', ' ', chromosome)
            bits = numbers.split(" ")

            tokens = []
            for token in bits:
                if token != "":
                    tokens.append(int(token))

            swarm = []
            for i in range(0, len(tokens), 3):
                swarm.append((tokens[i], tokens[i+1], tokens[i+2]))

            swarms.append(swarm)

        return swarms

    def getTrees(self, swarms, seed = 1):

        if len(swarms) == 0:
            return

        swarm = swarms[seed-1]
        print("Swarm: "+str(swarm)+"\n")

        chromosomes = ""
        for ind in swarm:
            ind = self.repertoire.container[tuple(ind)]
            chromosomes += str(ind)+"\n"

        return chromosomes

    def printTrees(self, swarms, seed = 1):

        trees = self.getTrees(swarms, seed)
        print(trees)

    def chromosomeContributions(self, swarms, x, y, z, seed = 1):

        if len(swarms) == 0:
            return

        print("\n\nLooking for "+str(tuple((x, y, z)))+"\n")

        seed -= 1
        for i in range(len(swarms)):

            if i < seed:
                continue

            swarm = swarms[i]
            positions = []
            for j in range(len(swarm)):
                if swarm[j] == tuple((x, y, z)):
                    positions.append(j)

            if len(positions) > 0:

                print("Seed "+str(i+1)+"\n")
                for position in positions:
                    print("result "+str(position))
                print()

                trees = self.getTrees(swarms, i+1)
                with open("../argos3/best.txt", "w") as f:
                    f.write(trees)

                subprocess.call(["/bin/bash", "./headless"])

                print()
                return

        print("Not found\n")

    def chromosomePositions(self, swarms, x, y, z):

        if len(swarms) == 0:
            return

        print(str(x)+"-"+str(y)+"-"+str(z))

        for i in range(len(swarms)):
            swarm = swarms[i]
            exists = False
            for j in range(len(swarm)):
                if swarm[j] == tuple((x, y, z)):
                    print(j)
                    exists = True
        print()

    def printTreeFromRepertoire(self, x, y, z):
        print("\n"+str(self.repertoire.container[x,y,z])+"\n")
        print(self.repertoire.container[x,y,z].fitness.values)
        print(self.repertoire.container[x,y,z].features)
        print()

    def printRepertoireScores(self):

        increments = [0.08, 0.16, 0.24, 0.32, 0.40, 0.48]

        # one food / (six iterations * nine robots) = 0.018518518518518517
        min_contribution = 1 / (6 * 9)

        # maximum fitness score for each bin # and how much food can be deposited
        increments[0] = 0.07407407407407407 # 4
        increments[1] = 0.14814814814814814 # 8
        increments[2] = 0.2222222222222222 # 12
        increments[3] = 0.3148148148148148 # 17
        increments[4] = 0.3888888888888889 # 21
        increments[5] = 0.46296296296296297 # 25

        src = self.repertoire.container
        count = 0
        for z in range(0, 6):
            for x in range(0, 6):
                for y in range(0, 6):
                    deviation = []
                    coords = [x,y,z]
                    for f in range(3):
                        if src[x, y, z].features[f] not in increments:
                            deviation.append(f)
                    if len(deviation) != 0:
                        count += 1
                        print(str(x)+"-"+str(y)+"-"+str(z)+"  "+str(deviation))

            print("\nTotal deviations: "+str(count)+"\n")


    def heterogenousRepertoireContributions(self, x, y, z):

        dst_repertoire = self.utilities.createContainer(self.params.nb_bins, self.params.features_domain, 1)

        src_bins = str(self.params.src_bins[0])
        dst_bins = str(self.params.nb_bins[0])
        repertoire_path = self.params.input_path+"/ga/"+self.params.experiments[1]+"/foraging"
        repertoire_file = repertoire_path+"/bins-"+src_bins+"/foraging-with-all-seeds-"+dst_bins+"-bins.txt"

        try:
            self.params.console("\nReading from "+repertoire_file)
            self.utilities.updateContainerFromString(None, self.utilities.toolbox,
                                                     dst_repertoire, repertoire_file, 2000, 0, 0)
        except FileNotFoundError as e:
            self.params.cancelled = True
            print("\n"+str(e)+"\n")
            return

        print("\nRepertoire size: "+str(len(dst_repertoire.values()))+"\n")

        for x in range(self.params.src_bins[0]):
            for y in range(self.params.src_bins[1]):
                for z in range(self.params.src_bins[2]):

                    output = str(x)+"-"+str(y)+"-"+str(z)+" "

                    total_pos = 0
                    count_pos = 0
                    for index, swarm in dst_repertoire.items():
                        if tuple((x,y,z)) in swarm:
                            total_pos += swarm.fitness.values[0]
                            count_pos += 1
                    avg_pos = total_pos / count_pos if count_pos > 0 else 0
                    output += str(avg_pos)+" "
                    output += str(count_pos)+" "

                    total_neg = 0
                    count_neg = 0
                    for index, swarm in dst_repertoire.items():
                        if tuple((x,y,z)) not in swarm:
                            total_neg += swarm.fitness.values[0]
                            count_neg += 1
                    avg_neg = total_neg / count_neg if count_neg > 0 else 0
                    output += str(avg_neg)+" "
                    output += str(count_neg)+" "

                    if count_pos > 0:
                        print(output)

    def evaluateSwarm(self, swarms, seed = 1, argos_seed = 0):

        if len(swarms) == 0:
            return

        swarm = swarms[seed-1]
        print("\nSeed "+str(seed)+"\n")

        self.utilities.saveConfigurationFile()

        print(self.utilities.evaluateSwarm(swarm, 1, argos_seed))

        self.params.deleteTempFiles()

    def heterogeneity(self):

        swarms = self.getSwarms()

        # 270 = maximum possible occurences for 9 individuals and 30 seeds
        domain = [[0,270],[0,270],[0,270]]
        container = self.utilities.createContainer(self.params.src_bins, domain, 1)

        for swarm in swarms:
            for ind in swarm:
                if tuple(ind) in container.container:
                    container.container[tuple(ind)] += 1
                else:
                    container.container[tuple(ind)] = 1

        print("\nrepertoire size "+str(len(container.items()))+"\n")

        max_total = 0
        results = np.full((self.params.src_bins[0], self.params.src_bins[1], self.params.src_bins[2]), np.nan)
        for index, total in container.items():
            results[index[0]][index[1]][index[2]] = total
            if total > max_total:
                max_total = total
        print("most prolific behaviour "+str(max_total))

        src = np.full((self.params.src_bins[0], self.params.src_bins[1], self.params.src_bins[2]), np.nan)
        for index, total in self.repertoire.items():
            try:
                src[index[0]][index[1]][index[2]] = 1
            except ValueError as e:
                print(index)
                return

        # from heterogeneous chromosomes
        all_data = [results]
        for data in all_data:
            fitness_min = np.nanmin(data)
            fitness_max = np.nanmax(data)

        # from source repertoire
        # all_data = [src]
        # fitness_min = 0.0
        # fitness_max = 1.8
        # self.flattenFitnessScores(src)

        bins = self.params.src_bins
        if bins[0]   <= 4:  bin_size_inches = 0.8
        elif bins[0] <= 8:  bin_size_inches = 0.4
        elif bins[0] <= 16: bin_size_inches = 0.2
        elif bins[0] <= 24: bin_size_inches = 0.133
        elif bins[0] <= 32: bin_size_inches = 0.1
        else: bin_size_inches = 0.04

        ticks = 4

        cmap = plt.get_cmap('YlGnBu')
        colour_map = self.truncate_colours(cmap, 0.35, 0.85)

        features_domain = self.params.src_domain
        fitness_domain = (fitness_min, fitness_max)
        self.small_repertoire = False

        for i in range(len(all_data)):
            all_data[i] = all_data[i].reshape((all_data[i].shape[0], 1) + all_data[i].shape[1:])
        features_domain = (features_domain[0], (0., 0.)) + tuple(features_domain[1:])
        bins = all_data[0].shape

        sections = []
        sections.append({"start" : 0, "end" : 2, "interval" : 1})

        count = 0
        for section in sections:

            count += 1
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

            if self.params.src_bins[0] == 4:
                figure_size = [1.5 + horizontal_bins_total * bin_size_inches, 0.5 + vertical_bins_total * bin_size_inches]
            else:
                figure_size = [1.5 + horizontal_bins_total * bin_size_inches, 0.8 + vertical_bins_total * bin_size_inches]

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
            self.drawColourBar(fig, ax, cax, figure_size)

            filename = "./heatmaps/temp.png"
            print(filename)
            # plt.savefig(filename)

            plt.show()

    def drawSubplot(self, ax, data_t, colour_map, features_domain, fitness_domain, z_index=0, bins=None, ticks = 4, show_y_tick_labels = False):

        vertical_min = fitness_domain[0]
        if np.isnan(vertical_min) or np.isinf(vertical_min):
            vertical_min = np.nanmin(data)

        vertical_max = fitness_domain[1]
        if np.isnan(vertical_max) or np.isinf(vertical_max):
            vertical_max = np.nanmax(data)

        cax = ax.imshow(data_t, interpolation="none", cmap=colour_map, vmin=vertical_min, vmax=vertical_max, aspect="equal")

        ax.set_title(self.writeZTitle(z_index, features_domain, bins),fontsize=20)

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

        ax.set_xticklabels([f'{round(float(x / float(len(data_t))    * delta_x + features_domain[0][0]), 2):1.2f}' for x in xticks], fontsize=20)
        ax.set_yticklabels([f'{round(float(y / float(len(data_t[0])) * delta_y + features_domain[1][0]), 2):1.2f}' for y in yticks], fontsize=20)

        if bins[1] == 1:
            yticks = []

        plt.xticks(xticks, rotation='vertical')
        plt.yticks(yticks)

        ax.invert_yaxis()
        ax.autoscale_view()

        return cax

    def writeZTitle(self, index, domain, bins):
        domain = self.params.src_domain[0]
        domain_max = domain[1] - domain[0]
        start = ((domain_max / bins[0]) * index) + domain[0]
        end = ((domain_max / bins[0]) * (index + 1)) + domain[0]
        title = str("%1.2f" % start)+"  -  "+str("%1.2f" % end)
        return title

    def drawColourBar(self, fig, ax, cax, figure_size):

        if self.params.src_bins[0] < 8:
            fig.subplots_adjust(right=0.80, wspace=0.20)
            colour_bar_axes = fig.add_axes([0.86, 0.1, 0.06, 0.8])

        elif self.params.src_bins[0] < 16:
            fig.subplots_adjust(right=0.88, wspace=0.20)
            colour_bar_axes = fig.add_axes([0.92, 0.1, 0.03, 0.8])

        else:
            fig.subplots_adjust(left=0.05, right=0.90, wspace=0.20)
            colour_bar_axes = fig.add_axes([0.94, 0.1, 0.03, 0.8])

        cbar = fig.colorbar(cax, cax=colour_bar_axes, format="%.0f")
        cbar.ax.tick_params(labelsize=18)

    def truncate_colours(self, cmap, minval=0.0, maxval=1.0, n=100):
        new_cmap = colors.LinearSegmentedColormap.from_list(
            'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
            cmap(np.linspace(minval, maxval, n)))
        return new_cmap

    def flattenFitnessScores(self, data):
        for x in range(len(data)):
            for y in range(len(data[0])):
                for z in range(len(data[0][0])):
                    if not math.isnan(data[x][y][z]):
                        data[x][y][z] = 1.0

def main():

    params = eaParams()
    params.deapSeed = 1
    params.configure()
    chromosome = Chromosome(params)

    if not params.cancelled:
        swarms = chromosome.getSwarms()

    if not params.cancelled:

        # x = 0
        # for y in range(4):
            # for z in range(4):
                # chromosome.chromosomePositions(swarms, x,y,z)

        chromosome.printTrees(swarms, 1)
        # chromosome.printTreeFromRepertoire(0,1,0)
        # chromosome.printRepertoireScores()

        # chromosome.chromosomeContributions(swarms,1,0,3, 1 )

        # chromosome.heterogeneity()

        # chromosome.heterogenousRepertoireContributions(0,0,0)

        # chromosome.evaluateSwarm(swarms, 1, 0)

if __name__ == "__main__":
    main()
