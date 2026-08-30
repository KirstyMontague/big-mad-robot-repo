
import sys
sys.path.insert(0, '..')

import matplotlib.pyplot as plt
import numpy

from params import eaParams
from redundancy import Redundancy
from repertoire import Repertoire
from utilities import Utilities

class Histogram():

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
        self.bins = self.repertoire.src_bins

        self.input = self.repertoire.input

        self.algorithm = self.repertoire.algorithms[0]
        self.experiment = self.repertoire.experiments[0]

        self.params.algorithm = self.algorithm
        self.params.indexes = self.utilities.getExperimentIndexes(self.objective, self.algorithm)
        self.params.description = self.utilities.getExperimentDescription(self.objective, self.algorithm)

    def loadContainers(self):

        if self.cancelled:
            return

        try:

            description = self.utilities.getExperimentDescription(self.objective, self.algorithm)

            self.features = []

            for i in self.params.indexes:

                containers = []

                if self.input == "combined":
                    containers.append(self.repertoire.getData(0, self.algorithm, self.experiment, i))

                else:
                    print("\nInput type not supported\n")
                    self.cancelled = True

                self.features.append(containers)

        except FileNotFoundError as e:
            print("\n"+str(e)+"\n")
            self.cancelled = True

    def draw(self):

        print("\nPopulation size "+str(len(self.features[0][0].values())))

        dist = [[],[],[]]
        for axis in range(len(self.bins)):
            for ind in self.features[0][0].values():
                dist[axis].append(ind.features[axis])

        max_extent = numpy.max(dist)
        if self.bins[0] > 32:
            bins = math.ceil(max_extent * 20)
        elif self.bins[0] > 8:
            bins = self.bins[0] / 2
        else:
            bins = self.bins[0]

        fig, axs = plt.subplots(1, 3, sharey=True, tight_layout=True, figsize=(14, 6))

        for axis in range(len(self.bins)):
            axs[axis].hist(dist[axis], range=[0.0, max_extent], bins=bins)

        filename = "./histograms/temp-"+str(self.bins[0])+".png"
        print("\n"+filename+"\n")

        if self.repertoire.save:
            plt.savefig(filename)

        if self.repertoire.show:
            plt.show()

if __name__ == "__main__":

    histogram = Histogram()
    histogram.loadContainers()
    if not histogram.cancelled:
        histogram.draw()


