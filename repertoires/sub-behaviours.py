
import sys
sys.path.insert(0, '..')

import pickle
from pathlib import Path

from deap import creator

import local
from redundancy import Redundancy
from params import eaParams

class SubBehaviours():

    def __init__(self):

        self.save = True
        self.runs = 30
        self.generation = 10
        self.go_away_from_food = "absolute"

        self.pset = local.PrimitiveSetExtended("MAIN", 0)
        self.params = eaParams()
        self.params.addUnpackedNodes(self.pset)
        self.params.configure()

        if self.params.using_repertoire:
            self.params.using_repertoire = False
            self.redundancy = Redundancy(self.params)
            self.params.using_repertoire = True
        else:
            self.redundancy = Redundancy(self.params)

        self.bins = self.params.bins_per_axis

        self.sub_behaviours = {"density" : "increaseDensity",
                               "nest" : "gotoNest",
                               "food" : "gotoFood",
                               "idensity" : "reduceDensity",
                               "inest" : "goAwayFromNest",
                               "ifood" : "goAwayFromFood"}

        self.sublists = [["food", "idensity", "inest"],
                         ["density", "nest", "ifood"]]

        self.subsets = ["food-idensity-inest", "density-nest-ifood"]

        self.input_path = self.params.input_path
        self.input_dir = self.params.experiment
        if len(self.params.subbehaviours_path) > 0:
            self.input_dir += "/"+self.params.subbehaviours_path

        self.output_path = self.params.shared_path+"/gp/"+self.params.experiment+"/foraging/"
        self.output_path += self.params.repertoire_type+str(self.params.repertoire_size)
        self.output_filename = self.output_path+"/sub-behaviours.txt"

        self.cancelled = "repro" in self.params.shared_path

        if self.save and not self.cancelled:
            Path(self.output_path+"/").mkdir(parents=True, exist_ok=True)

    def run(self):

        if self.cancelled:
            print("\naborted\n")
            return

        if self.save:
            with open(self.output_filename, 'w') as f:
                f.write("")

        if self.params.repertoire_type == "mt": self.getMtRepertoire()
        else: self.getQdRepertoire()

    def getQdRepertoire(self):

        for objective in self.sub_behaviours:

            containers = []

            results_dir = self.input_path+"/qdpy/"+self.input_dir+"/"+objective
            if objective == "ifood":
                results_dir += "-"+self.go_away_from_food+"-position"

            for seed in range(1, self.runs + 1):

                input_filename = results_dir+"/"+str(seed)+"/checkpoint-"+objective+"-"+str(seed)+"-"+str(self.generation)+".pkl"

                with open(input_filename, "rb") as f:
                    data = pickle.load(f)

                for i in data:
                    if str(i) == "containers":
                        container = data[i][0]

                containers.append(container)

            for a in range(self.bins):

                xa = int(a*8/self.bins)

                for b in range(self.bins):

                    yb = int(b*8/self.bins)

                    for c in range(self.bins):

                        zc = int(c*8/self.bins)

                        index = a*self.bins*self.bins + b*self.bins + c + 1

                        output = ""
                        ind = self.getBestEverFromSubset(containers, objective, xa, yb, zc, self.bins)

                        if ind is not None:
                            trimmed = self.redundancy.removeRedundancy(str(ind))
                            trimmed = [creator.Individual.from_string(trimmed, self.pset)][0]

                            output += self.sub_behaviours[objective]+str(index)
                            output += " "+str(trimmed)
                            print (output)

                            if self.save:
                                with open(self.output_filename, 'a') as f:
                                    f.write(self.sub_behaviours[objective]+str(index)+" "+str(trimmed))
                                    f.write("\n")

                        else:
                            output += objective+str(index)+" not found"
                            print(output)

    def getMtRepertoire(self):

        for combination in range(len(self.sublists)):

            subset = self.subsets[combination]
            sublist = self.sublists[combination]

            results_dir = self.input_path+"/gp/"+self.input_dir+"/"+subset
            if subset == "density-nest-ifood":
                results_dir += "-"+self.go_away_from_food+"-position"

            seeds = []
            for seed in range(1, self.runs + 1):

                input_filename = results_dir+"/"+str(seed)+"/checkpoint-"+subset+"-"+str(seed)+"-"+str(self.generation)+".pkl"
                with open(input_filename, "rb") as f:
                    checkpoint = pickle.load(f)

                seeds.append(checkpoint["containers"])

            containers = {}
            for objective in range(0, 3):
                containers[sublist[objective]] = []
                for seed in range(0, self.runs):
                    container = seeds[seed][objective]
                    containers[sublist[objective]].append(container)


            for objective in sublist:

                for a in range(self.bins):

                    xa = int(a*8/self.bins)

                    for b in range(self.bins):

                        yb = int(b*8/self.bins)

                        for c in range(self.bins):

                            zc = int(c*8/self.bins)

                            index = a*self.bins*self.bins + b*self.bins + c + 1

                            output = ""
                            ind = self.getBestEverFromSubset(containers[objective], objective, xa, yb, zc, self.bins)

                            if ind is not None:

                                trimmed = self.redundancy.removeRedundancy(str(ind))
                                trimmed = [creator.Individual.from_string(trimmed, self.pset)][0]

                                output += self.sub_behaviours[objective]+str(index)
                                output += " "+str(trimmed)
                                print (output)

                                if self.save:
                                    with open(self.output_filename, 'a') as f:
                                        f.write(self.sub_behaviours[objective]+str(index)+" "+str(trimmed))
                                        f.write("\n")

                            else:
                                output += self.sub_behaviours[objective]+str(index)
                                output += " "+str(xa)+" "+str(yb)+" "+str(zc)
                                output += " not found"

    def deratingFactor(self, individual):

        length = float(len(individual))
        usage = length - 10 if length > 10 else 0
        usage = usage / 990 if length <= 1000 else 1
        usage = 1 - usage

        return usage

    def getBestFromBin(self, container, index):

        if len(container.solutions[index]) == 0:
            return None

        best = container.solutions[index][0]
        for ind in container.solutions[index]:
            ind_fitness = ind.fitness.values[0] * self.deratingFactor(ind)
            best_fitness = best.fitness.values[0] * self.deratingFactor(best)
            if ind_fitness > best_fitness:
                best = ind

        return best

    def getBestFromSubset(self, container, x, y, z, bins):

        best = None
        limit = int(8/bins)

        for i in range(x, x+limit):
            for j in range(y, y+limit):
                for k in range(z, z+limit):
                    ind = self.getBestFromBin(container, (i,j,k))
                    if best == None:
                        best = ind
                    elif not ind == None:
                        ind_fitness = ind.fitness.values[0] * self.deratingFactor(ind)
                        best_fitness = best.fitness.values[0] * self.deratingFactor(best)
                        if ind_fitness > best_fitness:
                            best = ind

        return best

    def getBestEverFromSubset(self, containers, objective, x, y, z, bins):

        best = None

        for container in containers:

            ind = self.getBestFromSubset(container, x, y, z, bins)

            if best == None:
                best = ind

            elif not ind == None:
                ind_fitness = ind.fitness.values[0] * self.deratingFactor(ind)
                best_fitness = best.fitness.values[0] * self.deratingFactor(best)
                if ind_fitness > best_fitness:
                    best = ind

        return best

sub_behaviours = SubBehaviours()
sub_behaviours.run()
