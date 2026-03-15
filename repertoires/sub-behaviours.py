
import sys
sys.path.insert(0, '..')

import os
from pathlib import Path

from deap import creator
from deap import gp
from containers import *

import local
from redundancy import Redundancy
from params import eaParams
from utilities import Utilities

class SubBehaviours():

    def __init__(self):

        self.save = False
        self.legacy = False
        self.runs = 0
        self.generation = 0
        self.repertoire_type = "qd"
        self.repertoire_size = 1
        self.input_type = "separate"

        self.pset = local.PrimitiveSetExtended("MAIN", 0)
        self.params = eaParams()
        self.params.addUnpackedNodes(self.pset)
        self.params.is_qdpy = True

        self.cancelled = False
        self.configure()
        print()

        self.cancelled = self.cancelled or "repro" in self.params.shared_path

        self.utilities = Utilities(self.params)
        self.utilities.setupToolbox(self.selTournament)

        if self.params.using_repertoire:
            self.params.using_repertoire = False
            self.redundancy = Redundancy(self.params)
            self.params.using_repertoire = True
        else:
            self.redundancy = Redundancy(self.params)

        self.bins = self.bins_per_axis

        self.sub_behaviours = {"density" : "increaseDensity",
                               "nest" : "gotoNest",
                               "food" : "gotoFood",
                               "idensity" : "reduceDensity",
                               "inest" : "goAwayFromNest",
                               "ifood-perceived-position" : "goAwayFromFood"}

        if self.repertoire_type == "mtc":
            self.sublists = [["density", "nest", "ifood-perceived-position"],
                             ["food", "idensity", "inest"]]
            self.subsets = [self.utilities.getExperimentDescription(0, "mtc"),
                            self.utilities.getExperimentDescription(3, "mtc")]

        if self.repertoire_type == "mti":
            self.sublists = [["density", "nest", "food"],
                             ["idensity", "inest", "ifood-perceived-position"]]
            self.subsets = [self.utilities.getExperimentDescription(0, "mti"),
                            self.utilities.getExperimentDescription(3, "mti")]

        self.input_path = self.params.input_path
        self.input_dir = self.params.experiment
        if len(self.params.subbehaviours_path) > 0:
            self.input_dir += "/"+self.params.subbehaviours_path

        self.output_path = self.params.shared_path+"/gp/"+self.params.experiment+"/foraging/"
        self.output_path += self.repertoire_type+str(self.repertoire_size)
        self.output_filename = self.output_path+"/sub-behaviours.txt"

        if not self.cancelled:
            if self.save:
                if os.path.exists(self.output_filename):
                    confirm = input("Output file already exists at "+self.output_filename+"\n\nContinue? (y/N)\n")
                    if confirm == "y":
                        print()
                    else:
                        self.save = False
                        print("Switching to dry run\n")
                else:
                    Path(self.output_path+"/").mkdir(parents=True, exist_ok=True)
                    print("Writing to "+self.output_filename+"\n")
            else:
                print("Output filename: "+self.output_filename+"\n")
        else:
            print("Cancelled\n")

    def configure(self):
        permitted = ["experiment", "experiments", "input_type", "save", "legacy",
                     "runs", "generations", "repertoire_type", "bins_per_axis"]
        with open(self.params.shared_path+"/subbehaviours.txt", 'r') as f:
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

        if data[0] == "experiment" and len(data) > 1:
            self.params.experiment = data[1]

        if data[0] == "experiments" and len(data) > 1:
            for i in range(1, len(data)):
                self.params.experiments.append(data[i])

        if data[0] == "input_type":
            types = ["separate", "combined", "external"]
            if data[1] in types:
                self.input_type = data[1]
            else:
                print("\nInput type not recognised: "+data[1]+"\n")
                self.cancelled = True

        if data[0] == "runs":
                self.runs = int(data[1])

        if data[0] == "generations":
                self.generation = int(data[1])

        if data[0] == "repertoire_type":
            algorithms = ["mtc", "mti", "qd"]
            if data[1] in algorithms:
                self.repertoire_type = data[1]
            else:
                print("\nRepertoire type not recognised: "+data[1]+"\n")
                self.cancelled = True

        if data[0] == "bins_per_axis":
            self.bins_per_axis = int(data[1])
            self.repertoire_size = self.bins_per_axis ** self.params.characteristics

        if data[0] == "save":
            self.save = True if data[1] == "True" else False

        if data[0] == "legacy":
            self.legacy = True if data[1] == "True" else False

    def getRepertoires(self):

        containers = []

        algorithm = "gp" if "mt" in self.repertoire_type or self.input_type == "external" else "qdpy"

        for i in range(len(self.sub_behaviours.items())):

            objective = self.params.objectives[i]
            description = self.utilities.getExperimentDescription(i, self.repertoire_type)

            container = (Grid(shape = [8,8,8],
                              max_items_per_bin = 3,
                              fitness_domain = [(0.,1.0),],
                              features_domain = [(-40.0, 40.0), (-40.0, 40.0), (0.0, 1.0)],
                              storage_type=list))

            try:
                if self.input_type == "combined":
                    input_filename = self.input_path+"/"+algorithm+"/"+self.input_dir
                    if not self.legacy:
                        input_filename += "/"+description
                    input_filename += "/"+objective+".txt"
                    self.utilities.updateContainerFromString(self.redundancy, container, input_filename)

                elif self.input_type == "external":
                    for experiment in self.params.experiments:
                        input_filename = self.input_path+"/"+algorithm+"/"+self.input_dir+"/repertoires"
                        if not self.legacy:
                            input_filename += "/"+self.repertoire_type
                        input_filename += "/"+experiment+"/"+objective+"-"+str(self.generation)+".txt"
                        self.utilities.updateContainerFromString(self.redundancy, container, input_filename)

                else:
                    input_path = self.input_path+"/"+algorithm+"/"+self.input_dir+"/"+description
                    for seed in range(1, self.runs + 1):
                        input_filename = input_path+"/"+str(seed)+"/checkpoint-"+description+"-"+str(seed)+"-"+str(self.generation)
                        if not self.legacy:
                            input_filename += "-"+objective
                        input_filename += ".txt"
                        self.utilities.updateContainerFromString(self.redundancy, container, input_filename)

            except FileNotFoundError as e:
                print(str(e)+"\n")
                print("Cancelled\n")
                self.cancelled = True
                break

            containers.append(container)

        return containers

    def writeRepertoires(self, containers):

        if self.save and not self.cancelled:
            with open(self.output_filename, 'w') as f:
                f.write("")

        for i in range(len(self.sub_behaviours.items())):

            objective = self.params.objectives[i]

            for a in range(self.bins):
                for b in range(self.bins):
                    for c in range(self.bins):

                        xa = int(a*8/self.bins)
                        yb = int(b*8/self.bins)
                        zc = int(c*8/self.bins)

                        index = a*self.bins*self.bins + b*self.bins + c + 1

                        output = ""
                        ind = self.getBestFromSubset(containers[i], xa, yb, zc, self.bins)

                        if ind is not None:
                            trimmed = self.redundancy.removeRedundancy(str(ind))
                            trimmed = [creator.Individual.from_string(trimmed, self.pset)][0]

                            output += self.sub_behaviours[objective]+str(index)
                            output += " "+str(trimmed)

                            if self.save:
                                with open(self.output_filename, 'a') as f:
                                    f.write(self.sub_behaviours[objective]+str(index)+" "+str(trimmed))
                                    f.write("\n")

                        else:
                            output += self.sub_behaviours[objective]+str(index)
                            output += " ("+str(a)+", "+str(b)+", "+str(c)+")"
                            output += " not found"

                        print(output)

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

    def selTournament(self):
        return []

if __name__ == "__main__":

    sub_behaviours = SubBehaviours()

    if not sub_behaviours.cancelled:
        containers = sub_behaviours.getRepertoires()

    if not sub_behaviours.cancelled:
        sub_behaviours.writeRepertoires(containers)

