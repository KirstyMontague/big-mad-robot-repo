
import sys
sys.path.insert(0, '..')

import time

from params import eaParams
from redundancy import Redundancy
from repertoire import Repertoire
from utilities import Utilities

"""

Work in progress for analysing repertoires and generating CSVs retrospectively

postpro input type is for BT repertoires in the GA folder
(ie, source repertoires for heterogeneous swarms)

population output type identifies points of interest in the repertoire and prints
the index and features of the individuals at these locations

"""

class Statistics():

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

        self.input = self.repertoire.input
        self.output = self.repertoire.output
        self.mode = self.repertoire.mode
        self.save = self.repertoire.save
        self.pause = self.repertoire.pause

        self.seeds = self.repertoire.seedsList()
        self.algorithm = self.repertoire.algorithms[0]
        self.experiment = self.repertoire.experiments[0]

        self.params.algorithm = self.algorithm
        self.params.indexes = self.utilities.getExperimentIndexes(self.objective, self.algorithm)
        self.params.description = self.utilities.getExperimentDescription(self.objective, self.algorithm)
        self.params.nb_bins = self.bins

        if self.input == "combined" and "csv" in self.output:
            print("\nCan only write CSVs from separate seeds\n")
            self.cancelled = True
            return

    def loadContainers(self):

        if self.cancelled:
            return

        try:

            description = self.utilities.getExperimentDescription(self.objective, self.algorithm)

            self.features = []

            for i in self.params.indexes:

                containers = []

                if self.input == "separate":
                    for seed in self.seeds:
                        containers.append(self.repertoire.getData([seed], self.algorithm, self.experiment, i))

                elif self.input in ["combined" , "postpro"]:
                    containers.append(self.repertoire.getData(0, self.algorithm, self.experiment, i))

                else:
                    print("\nInput type not supported\n")
                    self.cancelled = True

                print()

                if self.pause > 0.0:
                    print("pausing for "+str(self.pause)+"s\n")
                    time.sleep(self.pause)

                self.features.append(containers)

        except FileNotFoundError as e:
            print("\n"+str(e)+"\n")
            self.cancelled = True

    def generateExtremaCSV(self):

        if self.cancelled:
            return

        algorithm_type = self.repertoire.getAlgorithmDir(self.algorithm)
        description = self.utilities.getExperimentDescription(self.objective, self.algorithm)
        output_dir = self.repertoire.getOutputDir(algorithm_type, self.experiment, description)

        headings = "Objective,Time,Seed,Robots,Pop,Tourn,Iterations,Params,,0,1000,,Chromosome,,Nodes"

        for i in range(len(self.params.indexes)):

            containers = self.features[i]
            objective_name = self.params.objectives[self.params.indexes[i]]

            csv = []

            for axis in range(len(self.bins)):
                if self.mode == "write":
                    csv.append(headings+"\n")
                else:
                    csv.append("")

            for i in range(len(containers)):
                extrema = self.utilities.getExtremaFromContainer(containers[i])
                seed = self.seeds[i]
                for axis in range(len(self.bins)):
                    ind = extrema[axis]
                    csv[axis] += self.params.description+",0,"+str(seed)+",3,25,3,6,0.2,,0,"+str(ind.features[axis])+",,,,\n"

            for axis in range(len(self.bins)):

                if len(self.params.indexes) > 1:
                    output_file = output_dir+"/extrema-"+objective_name+"-1000-"+str(axis+1)+".csv"
                else:
                    output_file = output_dir+"/extrema1000-"+str(axis+1)+".csv"
                print("output file "+output_file)
                print()

                print(csv[axis].replace(",", "\t"))
                print()

                if self.save:
                    mode = "w" if self.mode == "write" else "a"
                    with open(output_file, mode) as f:
                        f.write(csv[axis])

    def generateAdjustedQdScoreCSV(self):

        if self.cancelled:
            return

        algorithm_type = self.repertoire.getAlgorithmDir(self.algorithm)
        description = self.utilities.getExperimentDescription(self.objective, self.algorithm)
        output_dir = self.repertoire.getOutputDir(algorithm_type, self.experiment, description)

        headings = "Objective,Time,Seed,Robots,Pop,Tourn,Iterations,Params,,0,1000,,Chromosome,,Nodes"

        csv = ""
        if self.mode == "write":
            csv = headings+"\n"

        for seed in range(len(self.seeds)):

            csv += self.utilities.getExperimentDescription(self.objective, self.algorithm)+",0,"+str(seed)+",3,25,3,6,0.2,,"

            for feature in range(len(self.params.indexes)):
                csv += "0.0 "
            csv = csv[:-1]+","

            for feature in range(len(self.params.indexes)):
                container = self.features[feature][seed]
                csv += str(self.utilities.getAdjustedQDScore(container))+" "

            csv = csv[:-1]+",,,,\n"

        output_file = output_dir+"/adjusted-qd-scores1000.csv"
        print("CSV file "+output_file)
        print()

        print(csv.replace(",", "\t"))
        print()

        if self.save:
            mode = "w" if self.mode == "write" else "a"
            with open(output_file, mode) as f:
                f.write(csv)

    def getBest(self):

        output = ""

        for i in range(len(self.features)):

            if self.algorithm == "ga":

                if self.params.bias > -1:
                    output += "Best with bias:\n"
                    best = self.utilities.getBestSwarmFromContainer(self.features[i][0], self.params.bias)
                    raw_fitness = self.utilities.getAdjustedSwarmFitness(best, -1)
                    adj_fitness = self.utilities.getAdjustedSwarmFitness(best, self.params.bias)
                    output += str("%1.6f" % adj_fitness)+" ("+str("%1.6f" % raw_fitness)+")   "
                    output += str(best.features)+"\n\n"

                output += "Best ever:\n"
                best = self.utilities.getBestSwarmFromContainer(self.features[i][0], -1)
                fitness = best.features[0] + best.features[1] + best.features[2]
                output += str("%1.6f" % fitness)+"    "
                output += str(best.features)

            else:

                best = self.utilities.getBestFromContainer(self.features[i][0])
                output += "Best fitness:\n"
                output += str(best.fitness.values)

        print(output)
        print()

    def getCoverage(self):
        output = "Coverage: "
        for i in range(len(self.features)):
            coverage = self.utilities.getCoverage(self.features[i][0])
            coverage *= self.bins[0] * self.bins[1] * self.bins[2]
            output += str("%1.6f" % coverage)+"    "
        print(output)
        print()

    def getQdScore(self):
        qd_score = "QD Score: "
        adj_score = "Adjusted: "
        for i in range(len(self.features)):
            if self.algorithm == "ga":
                qd = self.utilities.getQDScoreWithBias(self.features[i][0], self.bins)
                qd_score += str("%1.6f" % qd)+"    "
            else:
                qd = self.utilities.getQDScore(self.features[i][0], self.bins)
                adj = self.utilities.getAdjustedQDScore(self.features[i][0], self.bins)
                qd_score += str("%1.6f" % qd)+"    "
                adj_score += str("%1.6f" % adj)+"    "
        print(qd_score)
        if self.algorithm != "ga":
            print(adj_score)
        print()

    def getAvgQuality(self):
        avg_quality = "Avg quality: "
        total_bins = self.bins[0] * self.bins[1] * self.bins[2]
        for i in range(len(self.features)):
            coverage = self.utilities.getCoverage(self.features[i][0]) * total_bins
            if self.algorithm == "ga":
                quality = self.utilities.getQDScoreWithBias(self.features[i][0], self.bins)
            else:
                quality = self.utilities.getQDScore(self.features[i][0], self.bins)
            quality = quality * total_bins
            quality = quality / coverage
            avg_quality += str("%1.6f" % quality)+"    "
        print(avg_quality)
        print()

    def getExtrema(self):
        output = "Extrema per axis: "
        for i in range(len(self.features)):
            extrema = self.utilities.getExtremaFromContainer(self.features[i][0])
            for axis in range(len(extrema)):
                output += str("%.6f" % extrema[axis].features[axis])+" "
        print(output)
        print()

    def getAvgPerAxis(self):
        for i in range(len(self.features)):
            output = "Average per axis: "
            avg = [0,0,0]
            for index, ind in self.features[i][0].items():
                for axis in range(len(self.bins)):
                    avg[axis] += ind.features[axis]
            for axis in range(len(avg)):
                avg[axis] /= len(self.features[i][0].items())
                output += str("%.6f" % avg[axis])+" "
            print(output)
            print()

    def getQdScorePerAxis(self):
        for i in range(len(self.features)):
            output = "QD per axis: "
            avg = [0,0,0]
            for index, ind in self.features[i][0].items():
                for axis in range(len(self.bins)):
                    avg[axis] += ind.features[axis]
            for axis in range(len(avg)):
                avg[axis] /= self.bins[0]*self.bins[1]*self.bins[2]
                output += str("%.6f" % avg[axis])+" "
            print(output)
            print()

    def printIndividual(self, x, y, z):
        for i in range(len(self.features)):
            container = self.features[i][0]

            print(str(x)+", "+str(y)+", "+str(z))
            print(container.container[x,y,z].features)
            print()

    def printPopulation(self):

        extrema = [-1,-1,-1]
        for axis in range(len(self.bins)):
            for index, ind in self.features[0][0].items():
                if index[axis] >= extrema[axis]:
                    extrema[axis] = index[axis]

        x = extrema[0]
        y = extrema[1]
        z = extrema[2]


        print("== max x, min y/z =================================================================\n")

        max_x = -1
        min_y = self.bins[1]
        min_zy = self.bins[1]
        min_z = self.bins[2]
        min_yz = self.bins[2]

        for index, ind in self.features[0][0].items():
            if index[0] == x:
                if index[1] <= min_y: min_y = index[1]
                if index[2] <= min_z: min_z = index[2]

        for index, ind in self.features[0][0].items():
            if index[0] == x:
                if index[1] == min_y and index[2] <= min_yz:
                    min_yz = index[2]
                if index[2] == min_z and index[1] <= min_zy:
                    min_zy = index[1]

        self.printIndividual(x, min_y, min_yz)
        self.printIndividual(x, min_zy, min_z)


        print("== max y, min x/z =================================================================\n")

        max_y = -1
        min_x = self.bins[0]
        min_zx = self.bins[0]
        min_z = self.bins[2]
        min_xz = self.bins[2]

        for index, ind in self.features[0][0].items():
            if index[1] == y:
                if index[0] <= min_x: min_x = index[0]
                if index[2] <= min_z: min_z = index[2]

        for index, ind in self.features[0][0].items():
            if index[1] == y:
                if index[0] == min_x and index[2] <= min_xz:
                    min_xz = index[2]
                if index[2] == min_z and index[0] <= min_zx:
                    min_zx = index[0]

        self.printIndividual(min_x, y, min_xz)
        self.printIndividual(min_zx, y, min_z)

        print("== max z, min x/y =================================================================\n")

        max_z = -1
        min_x = self.bins[0]
        min_yx = self.bins[0]
        min_y = self.bins[1]
        min_xy = self.bins[1]

        for index, ind in self.features[0][0].items():
            if index[2] == z:
                if index[0] <= min_x: min_x = index[0]
                if index[1] <= min_y: min_y = index[1]

        for index, ind in self.features[0][0].items():
            if index[2] == z:
                if index[0] == min_x and index[1] <= min_xy:
                    min_xy = index[1]
                if index[1] == min_y and index[0] <= min_yx:
                    min_yx = index[0]

        self.printIndividual(min_x, min_xy, z)
        self.printIndividual(min_yx, min_y, z)

        print("== max x/y, min z =================================================================\n")

        max_x = -1
        max_y = -1
        min_z1 = self.bins[2]
        min_z2 = self.bins[2]
        for index, ind in self.features[0][0].items():
            if index[0] == x and index[1] >= max_y: max_y = index[1]
            if index[1] == y and index[0] >= max_x: max_x = index[0]

        for index, ind in self.features[0][0].items():
            if index[0] == x and index[1] == max_y and index[2] <= min_z1:
                min_z1 = index[2]

        for index, ind in self.features[0][0].items():
            if index[0] == max_x and index[1] == y and index[2] <= min_z2:
                min_z2 = index[2]

        self.printIndividual(x, max_y, min_z1)
        self.printIndividual(max_x, y, min_z2)

        print("== max x/z, min y =================================================================\n")

        max_x = -1
        max_z = -1
        min_y1 = self.bins[1]
        min_y2 = self.bins[1]
        for index, ind in self.features[0][0].items():
            if index[0] == x and index[2] >= max_z: max_z = index[2]
            if index[2] == z and index[0] >= max_x: max_x = index[0]

        for index, ind in self.features[0][0].items():
            if index[0] == x and index[2] == max_z and index[1] <= min_y1:
                min_y1 = index[1]

        for index, ind in self.features[0][0].items():
            if index[0] == max_x and index[2] == z and index[1] <= min_y2:
                min_y2 = index[1]

        self.printIndividual(x, min_y1, max_z)
        self.printIndividual(max_x, min_y2, z)

        print("== max y/z, min x =================================================================\n")

        max_y = -1
        max_z = -1
        min_x1 = self.bins[0]
        min_x2 = self.bins[0]
        for index, ind in self.features[0][0].items():
            if index[1] == y and index[2] >= max_z: max_z = index[2]
            if index[2] == z and index[1] >= max_y: max_y = index[1]

        for index, ind in self.features[0][0].items():
            if index[1] == y and index[2] == max_z and index[0] <= min_x1:
                min_x1 = index[0]

        for index, ind in self.features[0][0].items():
            if index[1] == max_y and index[2] == z and index[0] <= min_x2:
                min_x2 = index[0]

        self.printIndividual(min_x1, y, max_z)
        self.printIndividual(min_x2, max_y, z)

        print("== max x/y/z =================================================================\n")

        max_y = -1
        max_z = -1
        max_yz = -1
        max_zy = -1
        for index, ind in self.features[0][0].items():
            if index[0] == x and index[1] >= max_y: max_y = index[1]
            if index[0] == x and index[2] >= max_z: max_z = index[2]

        for index, ind in self.features[0][0].items():
            if index[0] == x and index[1] == max_y and index[2] >= max_yz:
                max_yz = index[2]

        for index, ind in self.features[0][0].items():
            if index[0] == x and index[2] == max_z and index[1] >= max_zy:
                max_zy = index[1]

        self.printIndividual(x, max_y, max_yz)
        self.printIndividual(x, max_zy, max_z)

        print("== max y/x/z =================================================================\n")

        max_x = -1
        max_z = -1
        max_xz = -1
        max_zx = -1
        for index, ind in self.features[0][0].items():
            if index[1] == y and index[0] >= max_x: max_x = index[0]
            if index[1] == y and index[2] >= max_z: max_z = index[2]

        for index, ind in self.features[0][0].items():
            if index[1] == y and index[0] == max_x and index[2] >= max_xz:
                max_xz = index[2]

        for index, ind in self.features[0][0].items():
            if index[1] == y and index[2] == max_z and index[0] >= max_zx:
                max_zx = index[0]

        self.printIndividual(max_x, y, max_xz)
        self.printIndividual(max_zx, y, max_z)

        print("== max z/x/y =================================================================\n")

        max_x = -1
        max_y = -1
        max_xy = -1
        max_yx = -1
        for index, ind in self.features[0][0].items():
            if index[2] == z and index[0] >= max_x: max_x = index[0]
            if index[2] == z and index[1] >= max_y: max_y = index[1]

        for index, ind in self.features[0][0].items():
            if index[2] == z and index[0] == max_x and index[1] >= max_xy:
                max_xy = index[1]

        for index, ind in self.features[0][0].items():
            if index[2] == z and index[1] == max_y and index[0] >= max_yx:
                max_yx = index[0]

        self.printIndividual(max_x, max_xy, z)
        self.printIndividual(max_yx, max_y, z)

if __name__ == "__main__":

    statistics = Statistics()

    statistics.loadContainers()

    if not statistics.cancelled:

        if statistics.output == "qd_score_csv":
            statistics.generateAdjustedQdScoreCSV()

        if statistics.output == "extrema_csv":
            statistics.generateExtremaCSV()

        if statistics.output == "population":
            statistics.printPopulation()

        if statistics.output == "combined":
            print()
            statistics.getBest()
            statistics.getCoverage()
            statistics.getQdScore()
            statistics.getAvgQuality()
            statistics.getExtrema()
            statistics.getAvgPerAxis()
            statistics.getQdScorePerAxis()

    print()
