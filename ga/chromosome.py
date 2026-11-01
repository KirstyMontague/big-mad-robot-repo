import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib as mpl

from functools import reduce
from operator import mul

import numpy as np
import math
import re
import statistics
import subprocess

import sys
sys.path.insert(0, '..')

# from containers import *
from grid import Grid

from deap import creator
from deap import gp
from deap import tools

from params import eaParams
from redundancy import Redundancy
from utilities import Utilities


class Chromosome():

    def __init__(self, params):

        self.params = params
        self.params.is_qdpy = True
        self.params.using_repertoire = False

        self.queries = []
        self.seed = 1
        self.start = 1
        self.stop = 2
        self.x = 0
        self.y = 0
        self.z = 0
        self.threads = 8
        self.save = False

        self.configure()

        self.utilities = Utilities(self.params, None)

        self.gp_toolbox = self.utilities.setupToolboxGP(None, True)

        if self.params.project == "straight_to_foraging":
            return

        if self.params.repertoire_size <= 512:
            self.redundancy = Redundancy(self.params)
        else:
            print("Repertoire too large: "+str(self.params.repertoire_size)+"\n(derived from params.repertoire_size)")
            return

        if not self.utilities.checkContainerSize():
            return

        self.params.makePaths()

        repertoire_path = self.params.shared_path+"/ga/"+self.params.experiments[1]+"/foraging"
        repertoire_file = repertoire_path+"/foraging-"+str(self.params.src_bins[0])+"-bins.txt"

        self.repertoire = self.utilities.createContainer(self.params.src_bins,
                                                         self.params.src_domain,
                                                         self.params.max_items_per_bin)

        try:
            self.params.console("\nReading from "+repertoire_file)
            self.utilities.updateContainerFromString(self.redundancy, self.gp_toolbox,
                                                     self.repertoire, repertoire_file,
                                                     2000, 0, 0)

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

        self.utilities.toolbox = self.utilities.setupToolboxGA(self.repertoire, None, None, flat_indexes, grid_indexes, True)

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

        experiment = self.params.experiments[2]

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

    def getTrees(self, swarms, seed):

        if len(swarms) == 0:
            return

        swarm = swarms[seed-1]
        print("Swarm: "+str(swarm)+"\n")

        chromosomes = ""
        for ind in swarm:
            ind = self.repertoire.container[tuple(ind)]
            chromosomes += str(ind)+"\n"

        return chromosomes

    def printTrees(self):

        swarms = self.getSwarms()
        trees = self.getTrees(swarms, self.seed)
        print(trees)

    def getBaselineTrees(self):

        filename = self.params.input_path+"/qdpy/"+self.params.experiments[0]+"/foraging/baseline/best2000.csv"

        print("Loading from: "+filename+"\n")

        try:
            with open(filename, "r") as f:
                chromosomes = []
                for line in f:
                    sections = line.split("\"")
                    if len(sections) > 1:
                        chromosomes.append(sections[1])

        except FileNotFoundError as e:
            self.params.cancelled = True
            print(str(e)+"\n")
            return

        return chromosomes

    def allChromosomeContributions(self, verbose = True):

        swarms = self.getSwarms()
        if len(swarms) == 0:
            return

        cancelled = False
        for x in range(self.params.src_bins[0]):
            for y in range(self.params.src_bins[1]):
                for z in range(self.params.src_bins[2]):
                    self.x = x
                    self.y = y
                    self.z = z
                    cancelled = self.chromosomeContributions(swarms, verbose)
                    if cancelled: break
                if cancelled: break
            if cancelled: break

    def chromosomeContributions(self, swarms, verbose = True):

        location = tuple((self.x, self.y, self.z))

        self.utilities.saveConfigurationFile()
        with open(self.params.local_path+"/seed1.txt", "w") as f:
            f.write("1\n0.2")

        num_robots = self.params.sqrt_robots * self.params.sqrt_robots
        num_scores = len(self.params.indexes) + self.params.characteristics

        aggregated = []
        for i in range(num_scores):
            aggregated.append([])

        if verbose:
            print("\nLooking for "+str(location)+"\n")

        seed = self.seed - 1
        for i in range(len(swarms)):

            if i < seed:
                continue

            swarm = swarms[i]
            positions = []
            for j in range(len(swarm)):
                if swarm[j] == location:
                    positions.append(j)

            if len(positions) > 0:

                if verbose:
                    print("Seed "+str(i+1)+"\n")
                    for position in positions:
                        print("result "+str(position))
                    print()

                trees = self.getTrees(swarms, i+1)
                with open(self.params.local_path+"/chromosome1.txt", "w") as f:
                    f.write(trees)

                subprocess.call(["/bin/bash", "./headless", "1", self.params.local_path])

                scores = {}
                for j in range(num_scores):
                    scores[j] = []
                    for k in range(num_robots):
                        scores[j].append([])

                with open(self.params.local_path+"/result1.txt", "r") as f:
                    for line in f:

                        first = line[0:line.find(" ")]
                        if first == "error":
                            print("error")
                            return True

                        lines = line.split()
                        robotId = int(float(lines[1]))
                        score_index = 0
                        if robotId in positions:
                            for k in range(self.params.iterations):
                                scores[score_index][robotId].append(float(lines[k + 2]))
                            score_index += 1
                            for j in range(3):
                                for k in range(self.params.iterations):
                                    index = (j * self.params.iterations) + self.params.iterations + k + 2
                                    scores[score_index][robotId].append(float(lines[index]))
                                score_index += 1

                if verbose:
                    for robot_id in range(num_robots):
                        if robot_id in positions:
                            print("Robot "+str(robot_id))
                            for feature in scores.values():
                                print(feature[robot_id])
                            print()

                for feature_index in range(len(scores.values())):
                    feature = scores[feature_index]
                    for robot_id in range(len(feature)):
                        if robot_id in positions:
                            aggregated[feature_index].append(statistics.median(feature[robot_id]))

                if verbose:
                    for position_id in range(len(positions)):
                        robot_scores = []
                        for feature in aggregated:
                            robot_scores.append(feature[position_id])
                        print("Robot "+str(positions[position_id])+" "+str(robot_scores))
                    print()

                    confirm = input("Continue? (Y/n)\n")
                    if confirm == "n":
                        return True

        if len(aggregated[0]) == 0:
            if verbose:
                print("Not found")
            return False

        medians = []
        means = []
        for feature in aggregated:
            medians.append(statistics.median(feature))
            means.append(statistics.mean(feature))

        output = str(location[0])+","+str(location[1])+","+str(location[2])+","
        output += str(medians[0])+","
        output += str(means[0])+"\n"
        print(output)

        return False

    def chromosomePositions(self):

        swarms = self.getSwarms()

        csv = ""

        for x in range(self.repertoire.nb_bins[0]):
            for y in range(self.repertoire.nb_bins[1]):
                for z in range(self.repertoire.nb_bins[2]):
                    csv += self.chromosomePosition(swarms, x,y,z)

        print(csv)

    def chromosomePosition(self, swarms, x, y, z):

        if len(swarms) == 0:
            return

        index = str(x)+"-"+str(y)+"-"+str(z)

        occurrences = 0
        positions = []
        for i in range(len(swarms)):
            swarm = swarms[i]
            for j in range(len(swarm)):
                if swarm[j] == tuple((x, y, z)):
                    occurrences += 1
                    positions.append(j)

        if occurrences > 0:
            unique, qty = np.unique(positions, return_counts=True)
            occurrences = str(len(positions))
            num_positions = str(len(set(positions)))
            max_one_location = str(np.max(qty))
            return index+","+occurrences+","+num_positions+","+max_one_location+"\n"

        return ""

    def printTreeFromRepertoire(self):
        index = tuple((self.x, self.y, self.z))
        print("\n"+str(self.repertoire.container[index])+"\n")
        print(self.repertoire.container[index].fitness.values)
        print(self.repertoire.container[index].features)
        print()

    def printRepertoireScores6Bins(self):

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

    def printRepertoireScores(self):

        for index, ind in self.repertoire.items():
            output = str(index)+" \t"
            output += str("%.6f" % ind.fitness.values)+" \t"
            for feature in ind.features:
                output += str("%.6f" % feature)+" "
            print(output)

    def heterogenousRepertoireContributions(self):

        dst_repertoire = self.utilities.createContainer(self.params.nb_bins, self.params.features_domain, 1)

        src_bins = str(self.params.src_bins[0])
        dst_bins = str(self.params.nb_bins[0])
        repertoire_path = self.params.input_path+"/ga/"+self.params.experiments[2]+"/foraging"
        repertoire_file = repertoire_path+"/bins-"+src_bins+"/foraging-with-all-seeds-"+dst_bins+"-bins.txt"

        try:
            self.params.console("\nReading from "+repertoire_file)
            self.utilities.updateContainerFromString(None, self.utilities.toolbox,
                                                     dst_repertoire, repertoire_file,
                                                     2000, 0, 0)
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

    def evaluateSwarm(self):

        swarms = self.getSwarms()
        if len(swarms) == 0:
            return

        for seed in range(self.start, self.stop + 1):
            swarm = swarms[seed-1]

            num_robots = self.params.sqrt_robots * self.params.sqrt_robots
            swarm = swarm[0:num_robots]

            results = []
            for i in range(self.threads):
                result = creator.IndividualGA(swarm)
                results.append(result)

            self.utilities.saveConfigurationFile()

            self.utilities.evaluate(self.assignPopulationFitness, results)

            output = "\nSeed "+str(seed)+"\n"
            for result in results:
                output += ",%.6f" % result.fitness.values[0]+",,"
                for feature in result.features:
                    output += "%.6f" % feature+","
                output += "\n"
            print(output)
            print()

        self.params.deleteTempFiles()

    def evaluateTree(self):

        index = tuple([self.x,self.y,self.z])
        if index not in self.repertoire.container:
            return

        primitivetree = gp.PrimitiveTree([])

        trees = []
        for i in range(self.threads):
            tree = str(self.repertoire.container[index])
            tree = primitivetree.from_string(tree, self.utilities.pset)
            individual = creator.IndividualGP(tree)
            trees.append(individual)

        output = "\n\n"+str(tree)+"\n\n"
        output += str(self.x)+"-"+str(self.y)+"-"+str(self.z)
        ind = self.repertoire.container[index]
        print(output)

        self.utilities.saveConfigurationFile()
        self.utilities.toolbox = self.gp_toolbox

        self.params.fitness_function = "median"
        self.utilities.evaluate(self.assignPopulationFitness, trees)

        print()
        for tree in trees:
            output = "%.6f" % tree.fitness.values[0]+",,"
            for feature in tree.features:
                output += "%.6f" % feature+","
            print(output)
        print()

        self.params.fitness_function = "mean"
        self.utilities.evaluate(self.assignPopulationFitness, trees)

        print()
        for tree in trees:
            output = "%.6f" % tree.fitness.values[0]+",,"
            for feature in tree.features:
                output += "%.6f" % feature+","
            print(output)
        print()

        self.params.deleteTempFiles()

    def evaluateTrees(self):

        primitivetree = gp.PrimitiveTree([])

        for index, ind in self.repertoire.items():

            trees = []
            for i in range(self.threads):
                tree = str(ind)
                tree = primitivetree.from_string(tree, self.utilities.pset)
                individual = creator.IndividualGP(tree)
                trees.append(individual)

            self.utilities.saveConfigurationFile()
            self.utilities.toolbox = self.gp_toolbox

            self.utilities.evaluate(self.assignPopulationFitness, trees)

            output = str(index[0])+"-"+str(index[1])+"-"+str(index[2])
            for tree in trees:
                output += ",%.6f" % tree.fitness.values[0]+",,"
                for feature in tree.features:
                    output += "%.6f" % feature+","
                output += "\n"
            print()
            print(output)

        self.params.deleteTempFiles()

    def evaluateBaselineTrees(self):

        trees = self.getBaselineTrees()

        primitivetree = gp.PrimitiveTree([])

        for seed in range(self.start, self.stop + 1):

            tree = str(trees[seed-1])
            tree = primitivetree.from_string(tree, self.utilities.pset)

            duplicates = []
            for j in range(self.threads):
                individual = creator.IndividualGP(tree)
                duplicates.append(individual)

            self.utilities.saveConfigurationFile()
            self.utilities.toolbox = self.gp_toolbox

            self.utilities.evaluate(self.assignPopulationFitness, duplicates)

            output = "\nSeed "+str(seed)+"\n"
            for tree in duplicates:
                output += ",%.6f" % tree.fitness.values[0]+",,"
                for feature in tree.features:
                    output += "%.6f" % feature+","
                output += "\n"
            print(output)
            print()

        self.params.deleteTempFiles()

    def getMeanFitnessFromTraining(self):

        repertoire = "median"
        results = "median"
        query = "mean"
        bins = str(9)

        filename = "./"+self.params.project+"/"
        if self.params.project == "heterogeneous_genetic_algorithm":
            filename += repertoire+"-then-"+results+"-argos-seeds-"+bins+"-bins-"+query+"-fitness.txt"
        else:
            filename += repertoire+"-argos-seeds-"+bins+"-bins-"+query+"-fitness.txt"

        print("Loading from: "+filename+"\n")

        try:
            with open(filename, "r") as f:

                native = []
                for line in f:
                    if len(line) > 2:
                        if (line[1] == "," or line[2] == "," or line[5] == ","):
                            sections = line.split(",")
                            native.append(float(sections[1]))

        except FileNotFoundError as e:
            self.params.cancelled = True
            print(str(e)+"\n")
            return

        for n in native:
            print(n)
        print()

    def writeUnseenSeedScores(self):

        repertoire = "mean"
        results = "median"
        query = "mean"
        bins = str(8)

        filename = "./"+self.params.project+"/"
        if self.params.project == "heterogeneous_genetic_algorithm":
            filename += repertoire+"-then-"+results+"-argos-seeds-"+bins+"-bins-"+query+"-fitness.txt"
        else:
            filename += repertoire+"-argos-seeds-"+bins+"-bins-"+query+"-fitness.txt"

        print("Loading from: "+filename+"\n")

        try:
            with open(filename, "r") as f:

                native = []
                unseen = []

                for line in f:

                    if len(line) > 6:
                        if "," in [line[1], line[2], line[5]]:
                            sections = line.split(",")
                            native.append(float(sections[1]))
                            unseen.append([])

                    if line[0] == ",":
                        sections = line.split(",")
                        value = float(sections[1]) / native[-1]
                        unseen[-1].append(value)

        except FileNotFoundError as e:
            self.params.cancelled = True
            print(str(e)+"\n")
            return

        avg_unseen = []
        for u in unseen:
            print(u)
            avg_unseen.append(statistics.mean(u))

        algorithm = "ga" if self.params.project == "heterogeneous_genetic_algorithm" else "qdpy"
        experiment_index = 2 if self.params.project == "heterogeneous_genetic_algorithm" else 0
        subdirectory = "bins-"+str(bins) if self.params.project == "heterogeneous_genetic_algorithm" else "baseline"

        csv_path = self.params.input_path+"/"+algorithm+"/"+self.params.experiments[experiment_index]+"/foraging"
        csv_file = csv_path+"/"+subdirectory+"/total-unseen-"+query+"s"+str(self.params.generations)+".csv"

        csv_headers = "Objective,,1000\n"
        csv_prefix = "foraging,"

        # with open(csv_file, "w") as f:
            # f.write(csv_headers)
            # for deap_seed in unseen:
                # for argos_seed in deap_seed:
                    # f.write(csv_prefix+","+str(argos_seed)+"\n")

        # csv = csv_headers
        # for deap_seed in unseen:
            # for argos_seed in deap_seed:
                # csv += csv_prefix+","+str(argos_seed)+"\n"
        # print(csv)

        print("\n"+csv_file+"\n")

    def writeNewUnseenSeedScores(self):

        bins = str(12)
        arena_index = 4

        arenas = ["20-80", "30-75", "40-70", "50-65", "60-60"]
        arena = arenas[arena_index]

        experiment_index = 2 if self.params.project == "heterogeneous_genetic_algorithm" else 0
        experiment = self.params.experiments[experiment_index]

        filename = "./"+self.params.project+"/"+experiment+"/"+experiment+"-"+arena
        if self.params.project == "heterogeneous_genetic_algorithm":
            filename += "-bins-"+bins
        filename += ".txt"

        print("Loading from: "+filename+"\n")

        try:
            with open(filename, "r") as f:

                unseen = []

                for line in f:

                    if len(line) > 6:
                        if line[0:4] == "Seed" or "," in line[1:3]:
                            unseen.append([])

                    if "," in line[0:3]:
                        sections = line.split(",")
                        value = float(sections[1])
                        unseen[-1].append(value)

        except FileNotFoundError as e:
            self.params.cancelled = True
            print(str(e)+"\n")
            return

        avg_unseen = []
        for u in unseen:
            print(u[-6:])
            avg_unseen.append(statistics.mean(u))

        algorithm = "ga" if self.params.project == "heterogeneous_genetic_algorithm" else "qdpy"
        experiment_index = 2 if self.params.project == "heterogeneous_genetic_algorithm" else 0
        subdirectory = "bins-"+str(bins) if self.params.project == "heterogeneous_genetic_algorithm" else "baseline"

        csv_path = self.params.input_path+"/"+algorithm+"/"+self.params.experiments[experiment_index]+"/foraging"
        csv_file = csv_path+"/"+subdirectory+"/total-"+arena+"-medians"+str(self.params.generations)+".csv"

        csv_headers = "Objective,,"+str(self.params.generations)+"\n"
        csv_prefix = "foraging,"

        # with open(csv_file, "w") as f:
            # f.write(csv_headers)
            # for i in range(len(unseen)):
                # for j in range(len(unseen[i])):
                    # f.write(csv_prefix+","+str(unseen[i][j])+"\n")

        # csv = csv_headers
        # for deap_seed in unseen:
            # for argos_seed in deap_seed:
                # csv += csv_prefix+","+str(argos_seed)+"\n"
        # print(csv)

        print("\nCSV file: "+csv_file+"\n")

    def readEvaluationOutput(self):

        repertoire = "median"
        results = "median"
        query = "median"
        bins = str(9)

        filename = "./"+self.params.project+"/"
        if self.params.project == "heterogeneous_genetic_algorithm":
            filename += repertoire+"-then-"+results+"-argos-seeds-"+bins+"-bins-"+query+"-fitness.txt"
        else:
            filename += repertoire+"-argos-seeds-"+bins+"-bins-"+query+"-fitness.txt"

        print("Loading from: "+filename+"\n")

        try:
            with open(filename, "r") as f:

                native = []
                unseen = []

                for line in f:

                    if len(line) > 6:
                        if "," in [line[1], line[2], line[5]]:
                            sections = line.split(",")
                            native.append(float(sections[1]))
                            unseen.append([])

                    if line[0] == ",":
                        sections = line.split(",")
                        unseen[-1].append(float(sections[1]))

        except FileNotFoundError as e:
            self.params.cancelled = True
            print(str(e)+"\n")
            return

        avg_unseen = []
        for u in unseen:
            print(u)
            avg_unseen.append(statistics.mean(u))

        print(native)
        print("\n"+str(statistics.mean(native))+","+str(statistics.mean(avg_unseen))+"\n")
        print()

    def readEvaluationOutputHeterogeneous(self):

        repertoire = "mean"
        results = "mean"
        query = "mean"
        bins = str(4)

        filename = "./"+self.params.project+"/"
        if self.params.project == "heterogeneous_genetic_algorithm":
            filename += repertoire+"-then-"+results+"-argos-seeds-"+bins+"-bins-"+query+"-fitness.txt"
        else:
            filename += repertoire+"-argos-seeds-"+bins+"-bins-"+query+"-fitness.txt"

        print("Loading from: "+filename+"\n")

        try:
            with open(filename, "r") as f:

                native = []
                unseen = []

                for line in f:

                    if len(line) > 2:
                        if (line[1] == "," or line[2] == "," or line[5] == ","):
                            sections = line.split(",")
                            native.append(float(sections[1]))
                            unseen.append([])

                    if line[0] == ",":
                        sections = line.split(",")
                        unseen[-1].append(native[-1] - float(sections[1]))

        except FileNotFoundError as e:
            self.params.cancelled = True
            print(str(e)+"\n")
            return

        avg_unseen = []
        for u in unseen:
            avg_unseen.append(statistics.mean(u))

        print(native)
        print("\n"+str(statistics.mean(native))+","+str(statistics.mean(avg_unseen))+"\n")
        print()

    def writeContributionsToCSV(self):

        filename = self.params.input_path+"/"+self.params.algorithm+"/"
        filename += self.params.experiments[2]+"/foraging/"
        filename += "bins-"+str(self.params.src_bins[0])+"/contributions"

        output = ""

        with open(filename+".txt", "r") as f:
            for line in f:
                if "," in line[0:3]:
                    columns = line.split(",")
                    index = tuple([int(columns[0]), int(columns[1]), int(columns[2])])
                    ind = self.repertoire.container[index]
                    fitness_in_repertoire = ind.fitness.values[0]
                    output += columns[0]+","+columns[1]+","+columns[2]+","+str(fitness_in_repertoire)+","+columns[3]+","+columns[4]+""

        print(output)

        if self.save:
            print("Saving to "+filename+"-abridged.csv")
            with open(filename+"-abridged.csv", "w") as f:
                f.write(output)
        else:
            print("Output file: "+filename+"-abridged.csv")

    def assignPopulationFitness(self, population, fitnesses):
        for ind, fit in zip(population, fitnesses):
            ind.fitness.values = fit[0]
            ind.features = fit[1]

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
        output_type = "bins"
        all_data = [results]
        for data in all_data:
            fitness_min = np.nanmin(data)
            fitness_max = np.nanmax(data)

        # from source repertoire
        # output_type = "src"
        # all_data = [src]
        # fitness_min = 0.0
        # fitness_max = 1.8
        # self.flattenFitnessScores(src)

        bins = self.params.src_bins
        if bins[0]   <= 5:  bin_size_inches = 0.8
        elif bins[0] <= 9:  bin_size_inches = 0.4
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

            filename = "../charts/heatmaps/temp-"
            filename += output_type+"-"+str(self.params.src_bins[0])
            if len(sections) > 1: filename += "-"+str(count)
            if self.params.bias != -1: filename += "-bias-"+self.params.bias
            filename += ".png"
            print(filename)

            if self.save:
                plt.savefig(filename)

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

    def configure(self):

        """
        self.params.experiments
        [0] homogeneous results location
        [1] heterogeneous repetoire location
        [2] heterogeneous results location
        """

        with open(self.params.shared_path+"/chromosome.txt", "r") as f:
            for line in f:
                line = line.strip('\t\n\r')
                data = line.split()

                if len(data) > 0 and data[0] == "queries":
                    self.queries = []
                    for i in range(1, len(data)):
                        self.queries.append(data[i])

                if len(data) > 0 and data[0] == "seed":
                    self.seed = int(data[1])

                if len(data) > 0 and data[0] == "start":
                    self.start = int(data[1])
                if len(data) > 0 and data[0] == "stop":
                    self.stop = int(data[1])

                if len(data) > 0 and data[0] == "x":
                    self.x = int(data[1])
                if len(data) > 0 and data[0] == "y":
                    self.y = int(data[1])
                if len(data) > 0 and data[0] == "z":
                    self.z = int(data[1])

                if len(data) > 0 and data[0] == "threads":
                    self.threads = int(data[1])

                if len(data) > 0 and data[0] == "save":
                    self.save = True if data[1] == "True" else False

def main():

    params = eaParams()
    params.deapSeed = 1
    params.configure()

    if not params.cancelled:
        chromosome = Chromosome(params)

    if not params.cancelled:

        if "positions" in chromosome.queries:
            chromosome.chromosomePositions()

        if "trees" in chromosome.queries:
            chromosome.printTrees()

        if "scores" in chromosome.queries:
            chromosome.printRepertoireScores()

        if "tree" in chromosome.queries:
            chromosome.printTreeFromRepertoire()

        if "contributions" in chromosome.queries:
            chromosome.allChromosomeContributions()

        if "heterogeneity" in chromosome.queries:
            chromosome.heterogeneity()

        if "heterogeneous_contributions" in chromosome.queries:
            chromosome.heterogenousRepertoireContributions()

        if "evaluate" in chromosome.queries:
            if params.project == "heterogeneous_genetic_algorithm":
                chromosome.evaluateSwarm()
            if params.project == "straight_to_foraging":
                chromosome.evaluateBaselineTrees()

        if "read_evaluation" in chromosome.queries:
            chromosome.readEvaluationOutput()

        if "read_contributions" in chromosome.queries:
            chromosome.writeContributionsToCSV()

        if "get_mean_fitness" in chromosome.queries:
            chromosome.getMeanFitnessFromTraining()

        if "save_unseen" in chromosome.queries:
            chromosome.writeNewUnseenSeedScores()

        print("\nTerminating\n")

if __name__ == "__main__":
    main()
