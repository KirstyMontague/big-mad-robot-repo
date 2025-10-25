import pickle
import time

from deap import creator

import sys
sys.path.insert(0, '..')
import local

from analysis import Analysis
from redundancy import Redundancy
from params import eaParams


class CrossEvaluation():

    """
    For go away from food results run with params.repertoire_type = gp, mtc, mti and qd.
    For mtc and mti update indexes as well.
    Update output filename for fitness scores in evaluateChromosomes.

    For qdpy results which match csv, derating needs to be applied after selection using
    the derate parameter in self.deratingFactor.

    Use getAbsoluteDifferenceInDistanceFromFoodInverse in argos/controllers/footbot_bt.cpp
    with self.fitness_function = "perceived" to evaluate the absolute position of controllers
    evolved using perceived position.
    .

    Final results in xx-ifood-xxxx-fitness.txt aren't derated
    """

    def __init__(self):

        self.save = True
        self.runs = 30

        self.pset = local.PrimitiveSetExtended("MAIN", 0)
        self.params = eaParams()
        self.params.addUnpackedNodes(self.pset)

        self.redundancy = Redundancy(False)
        self.analyse = Analysis()
        self.analyse.params.is_qdpy = True

        # not tested with more than one bin
        self.bins = self.params.bins_per_axis

        self.sub_behaviours = {"density" : "increaseDensity",
                               "nest" : "gotoNest",
                               "food" : "gotoFood",
                               "idensity" : "reduceDensity",
                               "inest" : "goAwayFromNest",
                               "ifood" : "goAwayFromFood"}

        self.sublists = [["idensity", "inest", "ifood"],
                         ["density", "nest", "ifood"]]

        self.subsets = ["idensity-inest-ifood", "density-nest-ifood"]

        self.fitness_function = "perceived"
        # self.fitness_function = "absolute"

        self.input_path = ".."
        self.input_dir = "results"
        self.output_filename = "../gp/test/ifood/"+self.params.repertoire_type+"-sub-behaviours-"+self.fitness_function+"-position.txt"
        print("\nSaving chromosomes to "+self.output_filename+"\n")

    def run(self):

        if self.params.description[-5:] == "ifood" and self.params.stop == False:
            if self.params.repertoire_type == "gp": self.getGpRepertoire()
            elif self.params.repertoire_type[0:2] == "mt": self.getMtRepertoire()
            else: self.getQdRepertoire()

    def getQdRepertoire(self):

        for objective in self.sub_behaviours:

            if objective != "ifood":
                continue

            if self.save and objective == "ifood":
                with open(self.output_filename, 'w') as f:
                    f.write("")

            containers = []

            results_dir = objective
            if objective == "ifood":
                results_dir = "ifood-"+self.fitness_function+"-position"

            for seed in range(1, self.runs + 1):

                input_filename = self.input_path+"/qdpy/"+self.input_dir+"/"+results_dir+"/"+str(seed)+"/seed"+str(seed)+"-iteration1000.p"

                with open(input_filename, "rb") as f:
                    data = pickle.load(f)

                for i in data:
                    if str(i) == "container":
                        container = data[i]

                containers.append(container)

                best = self.analyse.utilities.getBestMax(container)
                self.printBestFromContainer(best[0])

            for a in range(self.bins):

                xa = int(a*8/self.bins)

                for b in range(self.bins):

                    yb = int(b*8/self.bins)

                    for c in range(self.bins):

                        zc = int(c*8/self.bins)

                        index = a*self.bins*self.bins + b*self.bins + c + 1

                        for container in containers:

                            ind = self.getBestEverFromSubset([container], objective, xa, yb, zc, self.bins, False)
                            self.saveOutput(ind)

    def getMtRepertoire(self):

        for combination in range(len(self.sublists)):

            subset = self.subsets[combination]
            sublist = self.sublists[combination]

            if self.params.repertoire_type == "mti" and subset == "idensity-inest-ifood":
                results_dir = "idensity-inest-ifood-"+self.fitness_function+"-position"

            elif self.params.repertoire_type == "mtc" and subset == "density-nest-ifood":
                results_dir = "density-nest-ifood-"+self.fitness_function+"-position"

            else:
                continue

            seeds = []
            for seed in range(1, self.runs + 1):

                input_filename = self.input_path+"/gp/"+self.input_dir+"/"+results_dir+"/"+str(seed)+"/checkpoint-"+subset+"-"+str(seed)+"-1000.pkl"
                with open(input_filename, "rb") as f:
                    checkpoint = pickle.load(f)

                best = self.analyse.utilities.getBestHDRandom(checkpoint["containers"][2], 0)
                self.printBestFromContainer(best)

                seeds.append(checkpoint["containers"])

            containers = {}
            for objective in range(0, 3):
                containers[sublist[objective]] = []
                for seed in range(0, self.runs):
                    container = seeds[seed][objective]
                    containers[sublist[objective]].append(container)


            for objective in sublist:

                if objective != "ifood":
                    continue

                if self.save:
                    with open(self.output_filename, 'w') as f:
                        f.write("")

                for a in range(self.bins):

                    xa = int(a*8/self.bins)

                    for b in range(self.bins):

                        yb = int(b*8/self.bins)

                        for c in range(self.bins):

                            zc = int(c*8/self.bins)

                            index = a*self.bins*self.bins + b*self.bins + c + 1

                        for container in containers[objective]:

                            ind = self.getBestEverFromSubset([container], objective, xa, yb, zc, self.bins, True)
                            self.saveOutput(ind)

    def getGpRepertoire(self):

        for objective in self.sub_behaviours:

            if objective != "ifood":
                continue

            if self.save and objective == "ifood":
                with open(self.output_filename, 'w') as f:
                    f.write("")

            containers = []

            results_dir = objective
            if objective == "ifood":
                results_dir = "ifood-"+self.fitness_function+"-position"

            for seed in range(1, self.runs + 1):

                checkpoint_filename = self.input_path+"/gp/"+self.input_dir+"/"+results_dir+"/"+str(seed)+"/"
                checkpoint_filename += "checkpoint-"+objective+"-"+str(seed)+"-1000.pkl"
                with open(checkpoint_filename, "rb") as f:
                    checkpoint = pickle.load(f)

                containers.append(checkpoint["containers"])

                best = self.analyse.utilities.getBestHDRandom(checkpoint["containers"][0], 0)
                self.printBestFromContainer(best)

            for a in range(self.bins):

                xa = int(a*8/self.bins)

                for b in range(self.bins):

                    yb = int(b*8/self.bins)

                    for c in range(self.bins):

                        zc = int(c*8/self.bins)

                        index = a*self.bins*self.bins + b*self.bins + c + 1

                        for container in containers:

                            ind = self.getBestEverFromSubset(container, objective, xa, yb, zc, self.bins, True)
                            self.saveOutput(ind)

    def printBestFromContainer(self, best):

        # print("best from container: "+str(best))
        print("best from container: "+str(best.fitness.values[0]))

    def saveOutput(self, ind):

        output = ""

        if ind is not None:
            trimmed = self.redundancy.removeRedundancy(str(ind))
            trimmed = [creator.Individual.from_string(trimmed, self.pset)][0]

            # output += "========\n"
            # output += str(ind)+"\n\n"
            # output += str(trimmed)+"\n\n"
            output += str(ind.fitness.values[0] * self.deratingFactor(trimmed, True))
            output += " ("+str(ind.fitness.values[0])+")"
            # output += "\n"

            if self.save:
                with open(self.output_filename, 'a') as f:
                    f.write(str(trimmed))
                    f.write("\n")

        else:
            output += "goAwayFromFood"+str(index)+" not found"

        print(output)

    def deratingFactor(self, individual, derate = False):

        length = float(len(individual))
        usage = length - 10 if length > 10 else 0
        usage = usage / 990 if length <= 1000 else 1
        usage = 1 - usage

        return usage if derate else 1.0

    def getBestFromBin(self, container, index, derate = False):

        if len(container.solutions[index]) == 0:
            return None

        best = container.solutions[index][0]
        for ind in container.solutions[index]:
            ind_fitness = ind.fitness.values[0] * self.deratingFactor(ind, derate)
            best_fitness = best.fitness.values[0] * self.deratingFactor(best, derate)
            if ind_fitness > best_fitness:
                best = ind

        return best

    def getBestFromSubset(self, container, x, y, z, bins, derate = False):

        best = None
        limit = int(8/bins)

        for i in range(x, x+limit):
            for j in range(y, y+limit):
                for k in range(z, z+limit):
                    ind = self.getBestFromBin(container, (i,j,k), derate)
                    if best == None:
                        best = ind
                    elif not ind == None:
                        ind_fitness = ind.fitness.values[0] * self.deratingFactor(ind, derate)
                        best_fitness = best.fitness.values[0] * self.deratingFactor(best, derate)
                        if ind_fitness > best_fitness:
                            best = ind

        return best

    def getBestEverFromSubset(self, containers, objective, x, y, z, bins, derate = False):

        best = None

        for container in containers:

            ind = self.getBestFromSubset(container, x, y, z, bins, derate)

            if best == None:
                best = ind

            elif not ind == None:
                ind_fitness = ind.fitness.values[0] * self.deratingFactor(ind, derate)
                best_fitness = best.fitness.values[0] * self.deratingFactor(best, derate)
                if ind_fitness > best_fitness:
                    best = ind

        return best

    def evaluateChromosomes(self):

        self.analyse.utilities.saveConfigurationFile()

        filename = "../gp/test/ifood/"+self.params.repertoire_type+"-ifood-perceived-vs-absolute-fitness.txt"
        # filename = "../gp/test/ifood/"+self.params.repertoire_type+"-ifood-"+self.fitness_function+"-fitness.txt"
        print("\nSaving ARGoS results (not derated) to "+filename+"\n")

        scores = []
        run = 0
        with open(self.output_filename, "r") as f:
            for line in f:
                run += 1

                if run <= self.runs:
                    time.sleep(1.0)
                    chromosome = line

                    fitness = self.analyse.utilities.evaluateRobot(chromosome, 1)
                    scores.append(fitness)

                    if self.params.repertoire_type[0:2] == "mt":
                        print(fitness[0][2])
                    else:
                        print(fitness[0][0])

        if self.save:
            with open(filename, 'w') as f:
                for score in scores:
                    if self.params.repertoire_type[0:2] == "mt":
                        f.write(str(score[0][2])+"\n")
                    else:
                        f.write(str(score[0][0])+"\n")


evaluation = CrossEvaluation()

evaluation.run()
evaluation.evaluateChromosomes()
