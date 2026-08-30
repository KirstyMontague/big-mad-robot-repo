
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

if __name__ == "__main__":

    statistics = Statistics()

    statistics.loadContainers()

    if not statistics.cancelled:

        if statistics.output == "qd_score_csv":
            statistics.generateAdjustedQdScoreCSV()

        if statistics.output == "extrema_csv":
            statistics.generateExtremaCSV()

        if statistics.output == "combined":
            print()
            statistics.getBest()
            statistics.getCoverage()
            statistics.getQdScore()
            statistics.getAvgQuality()
            statistics.getExtrema()
            statistics.getAvgPerAxis()
            statistics.getQdScorePerAxis()


