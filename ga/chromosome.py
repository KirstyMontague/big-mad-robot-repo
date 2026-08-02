import sys
sys.path.insert(0, '..')

import re

import warnings
warnings.filterwarnings("error")

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
        self.redundancy = Redundancy(self.params)

        self.gp_toolbox = self.utilities.setupToolboxGP(None)

        if not self.utilities.checkContainerSize():
            return

        self.params.makePaths()

        repertoire_path = self.params.shared_path+"/ga/"+self.params.experiment+"/foraging"
        repertoire_file = repertoire_path+"/foraging-"+str(self.params.src_bins[0])+"-bins.txt"
        self.params.console("\nReading from "+repertoire_file)

        self.repertoire = self.utilities.createContainer(self.params.src_bins,
                                                         self.params.src_domain,
                                                         self.params.max_items_per_bin)
        self.utilities.updateContainerFromString(self.redundancy, self.gp_toolbox,
                                                 self.repertoire, repertoire_file, 0, 0)

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

        max_per_axis = [0,0,0]
        for index in grid_indexes:
            for i in range(len(index)):
                if index[i] > max_per_axis[i]:
                    max_per_axis[i] = index[i]
        print(max_per_axis)
        print()

        with open("../argos3/best.txt", "r") as f:
            for line in f:
                swarm = line

        numbers = re.sub('\D', ' ', swarm)
        bits = numbers.split(" ")

        tokens = []
        for token in bits:
            if token != "":
                tokens.append(int(token))
        swarm = []
        for i in range(0, len(tokens), 3):
            swarm.append((tokens[i], tokens[i+1], tokens[i+2]))

        chromosomes = ""
        for ind in swarm:
            ind = self.repertoire.container[tuple(ind)]
            chromosomes += str(ind)+"\n"

        # with open("../argos3/best.txt", "w") as f:
            # f.write(str(chromosomes[0:-1]))
        print(chromosomes)
        return



def main():

    params = eaParams()
    params.configure()
    chromosome = Chromosome(params)

if __name__ == "__main__":
    main()
