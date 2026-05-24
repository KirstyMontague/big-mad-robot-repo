
import sys
sys.path.insert(0, '..')

import time

from params import eaParams
from redundancy import Redundancy
from utilities import Utilities

"""

Work in progress for analysing repertoires and generating CSVs retrospectively

"""

class Repertoire():

    def __init__(self):

        self.params = eaParams()
        self.params.is_qdpy = True

        self.algorithm = "qdpy"
        self.objective = self.params.indexes[0]
        self.objective = self.params.objectives[self.objective]
        self.bins = self.params.nb_bins
        self.domain = self.params.features_domain
        self.generations = 1000
        self.mode = "append"
        self.save = False
        self.pause = 10.0
        self.seeds = []

        self.cancelled = False
        self.configure()

        algorithm_type = "qdpy" if self.algorithm == "qdpy" else "gp"
        self.input_dir = self.params.input_path+"/"+algorithm_type+self.params.directoryPath()
        self.output_dir = self.params.output_path+"/"+algorithm_type+self.params.directoryPath()
        print()
        print("input dir "+self.input_dir)
        print("output dir "+self.output_dir)
        print()

        self.utilities = Utilities(self.params, None)
        self.utilities.toolbox = self.utilities.setupToolboxGP(None)

        self.redundancy = Redundancy(self.params)

    def configure(self):
        permitted = ["algorithm", "project", "experiment", "objective", "bins", "domain", "seeds", "mode", "save", "pause"]
        with open(self.params.shared_path+"/repertoire.txt", 'r') as f:
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

        if data[0] == "mode":
            types = ["write", "append"]
            if data[1] in types:
                self.mode = data[1]
            else:
                print("mode not recognised")
                self.cancelled = True

        if data[0] == "objective":
            self.objective = int(data[1])
            self.params.indexes = [self.objective]
            self.params.description = self.params.objectives[self.objective]

        if data[0] == "bins" and len(data) > 1:
            self.params.nb_bins = []
            for b in data[1:]:
                self.params.nb_bins.append(int(b))

        if data[0] == "domain" and len(data) > 1:
            self.domain = []
            for i in range(1, len(data), 2):
                self.domain.append((float(data[i]), float(data[i+1])))

        if data[0] == "seeds" and len(data) > 1:
            self.seeds = []
            for seed in data[1:]:
                self.seeds.append(int(seed))

        if data[0] == "algorithm": self.algorithm = data[1]
        if data[0] == "project": self.params.project = data[1]
        if data[0] == "experiment" and len(data) > 1: self.params.experiment = data[1]
        if data[0] == "save": self.save = True if data[1] == "True" else False
        if data[0] == "pause": self.pause = float(data[1])

    def loadCombined(self):

        if self.cancelled:
            return

        filename = self.input_dir+"/"+self.params.description+"-with-all-seeds-small-bins.txt"
        print("input "+filename)

        container = self.utilities.createContainer(self.params.nb_bins, self.domain, 1)
        self.utilities.updateContainerFromString(self.redundancy, self.utilities.toolbox, container, filename, 0, 0)
        self.containers = [container]

        print(self.utilities.printExtrema(container))

    def loadSeparate(self):

        if self.cancelled:
            return

        try:
            self.containers = []
            for seed in self.seeds:

                filename = self.input_dir+"/"+str(seed)+"/checkpoint-"
                filename += self.params.description+"-"+str(seed)+"-"+str(self.generations)+"-"+self.params.description+".txt"
                print("input file "+filename)

                container = self.utilities.createContainer(self.params.nb_bins, self.domain, 1)
                self.utilities.updateContainerFromString(self.redundancy, self.utilities.toolbox, container, filename, 0, 0)
                self.containers.append(container)

                print("pausing for "+str(self.pause)+"s\n")
                time.sleep(self.pause)

        except FileNotFoundError as e:
            print("\n"+str(e)+"\n")
            self.cancelled = True

    def generateCSV(self):

        if self.cancelled:
            return

        headings = "Objective,Time,Seed,Robots,Pop,Tourn,Iterations,Params,,0,1000,,Chromosome,,Nodes"

        csv = []
        for i in range(len(self.params.nb_bins)):
            if self.mode == "write":
                csv.append(headings+"\n")
            else:
                csv.append("")

        for seed in range(len(self.containers)):
            extrema = self.utilities.getExtremaFromContainer(self.containers[seed])
            for i in range(len(self.params.nb_bins)):
                csv[i] += self.params.description+",0,"+str(seed)+",3,25,3,6,0.2,,0,"+str(extrema[i].features[i])+",,,,\n"
            print()

        for i in range(len(self.params.nb_bins)):

            output_file = self.output_dir+"/extrema1000-"+str(i+1)+".csv"
            print("output file "+output_file)
            print()

            print(headings.replace(",", "\t"))
            print(csv[i].replace(",", "\t"))
            print()

            mode = "w" if self.mode == "write" else "a"
            if self.save:
                with open(output_file, mode) as f:
                    f.write(csv[i])

    def getBest(self):
        best = self.utilities.getBestFromContainer(self.containers[0])
        print("Best: "+str("%1.6f" % best.fitness.values[0])+"\n")

    def getCoverage(self):
        coverage = self.utilities.getCoverage(self.containers[0])
        print("Coverage: "+str("%1.6f" % coverage)+"\n")

    def getQdScore(self):
        qd_score = self.utilities.getQDScore(self.containers[0], self.params.nb_bins)
        print("QD Score: "+str("%1.6f" % qd_score)+"\n")


if __name__ == "__main__":

    algorithms = ["qdpy"]

    repertoire = Repertoire()

    repertoire.loadSeparate()
    repertoire.generateCSV()

    repertoire.loadCombined()
    if not repertoire.cancelled:
        repertoire.getBest()
        repertoire.getCoverage()
        repertoire.getQdScore()


