
import sys
sys.path.insert(0, '..')

import numpy
import os
from pathlib import Path
import time

# from containers import *
from grid import Grid

from params import eaParams
from utilities import Utilities
from redundancy import Redundancy

"""

Work in progress for getting the best individual along
each axis and overall from one or more repertoires

"""

class Extrema():

    def __init__(self):

        self.params = eaParams()
        self.params.is_qdpy = True
        self.params.using_repertoire = False

        self.bins = self.params.nb_bins
        self.domain = self.params.features_domain
        self.seed = 0
        self.runs = 0
        self.generations = 0
        self.pause = 20.0

        self.cancelled = False
        self.configure()
        self.cancelled = self.cancelled or "repro" in self.params.shared_path

        if self.cancelled:
            print("\nCancelled\n")
            return

        self.utilities = Utilities(self.params)
        self.utilities.toolbox = self.utilities.setupToolboxGP(None)
        self.redundancy = Redundancy(self.params)

        self.objective = self.params.objectives[self.params.indexes[0]]
        self.description = self.utilities.getExperimentDescription(self.params.indexes[0], self.params.repertoire_type)
        self.directory = self.utilities.getExperimentDirectory(self.params.indexes[0], self.params.repertoire_type)

        if self.seed == 0:
            self.seeds = []
            for seed in range(1, self.runs + 1):
                self.seeds.append(seed)
        else:
            self.seeds = [self.seed]

        print()

    def configure(self):
        permitted = ["project", "algorithm", "repertoire_type", "experiment", "objectives",
                     "objective", "bins", "domain", "seed", "runs", "generations", "pause"]
        with open(self.params.shared_path+"/extrema.txt", 'r') as f:
            for line in f:
                data = line.split()
                if len(data) > 0:
                    if data[0] in permitted:
                        print(line.strip('\t\n\r'))
                        self.update(data)
                    else:
                        print("\nConfig entry not recognised: "+data[0]+"\n")
                        self.cancelled = True

    def update(self, data):

        if data[0] == "algorithm":
            algorithms = ["gp", "qdpy", "cma-es", "ga"]
            if data[1] in algorithms:
                self.params.algorithm = data[1]
            else:
                print("\nAlgorithm not recognised: "+data[1]+"\n")
                self.cancelled = True

        if data[0] == "repertoire_type":
            algorithms = ["gp", "mtc", "mti", "qd"]
            if data[1] in algorithms:
                self.params.repertoire_type = data[1]
            else:
                print("\nRepertoire type not recognised: "+data[1]+"\n")
                self.cancelled = True

        if data[0] == "objectives" and len(data) > 1:
            self.params.objectives = []
            for objective in data[1:]:
                self.params.objectives.append(objective)

        if data[0] == "objective":
            self.params.indexes = [int(data[1])]
            self.params.description = self.params.objectives[int(data[1])]

        if data[0] == "bins" and len(data) > 1:
            self.bins = []
            for bins in data[1:]:
                self.bins.append(int(bins))

        if data[0] == "domain" and len(data) > 1:
            self.domain = []
            for i in range(1, len(data), 2):
                self.domain.append((float(data[i]), float(data[i+1])))

        if data[0] == "project": self.params.project = data[1]
        if data[0] == "experiment" and len(data) > 1: self.params.experiment = data[1]
        if data[0] == "seed": self.seed = int(data[1])
        if data[0] == "runs": self.runs = int(data[1])
        if data[0] == "generations": self.generations = int(data[1])
        if data[0] == "pause": self.pause = float(data[1])

    def checkContainerFiles(self):

        input_path = self.params.input_path+"/"+self.params.algorithm+"/"+self.params.directoryPath()
        suffix = str(self.generations)+"-"+self.objective+".txt"

        missing = 0
        for seed in self.seeds:

            input_filename = input_path+"/"+str(seed)+"/checkpoint-"+self.description+"-"+str(seed)+"-"+suffix

            if not os.path.exists(input_filename):
                missing += 1
                print("Can't find "+input_filename)

        if missing > 0:
            print("\n"+str(missing)+" files missing\n")
            self.cancelled = True
            return

        if missing == 0:
            print("Found all files\n")

    def combineContainers(self):

        if self.cancelled:
            return []

        input_path = self.params.input_path+"/"+self.params.algorithm+"/"+self.params.directoryPath()
        suffix = str(self.generations)+"-"+self.objective+".txt"

        container = self.utilities.createContainer(self.bins, self.domain, 1)

        for seed in self.seeds:
            input_filename = input_path+"/"+str(seed)+"/checkpoint-"+self.description+"-"+str(seed)+"-"+suffix
            print("Reading "+input_filename)
            container = self.utilities.updateContainerFromString(self.redundancy, self.utilities.toolbox, container, input_filename, 0, 0)
            print("pausing for "+str(self.pause)+"s\n")
            time.sleep(self.pause)

        return container

    def printExtrema(self, container):

        if self.cancelled:
            return

        print()
        print("Max per axis")
        print(self.utilities.printExtrema(container, True))
        print()

        best = self.utilities.getBestFromContainer(container)
        print("Best individual")
        print(best.fitness.values[0])
        print(best.features)
        print(best)
        print()

if __name__ == "__main__":

    extrema = Extrema()

    extrema.checkContainerFiles()
    container = extrema.combineContainers()
    extrema.printExtrema(container)
