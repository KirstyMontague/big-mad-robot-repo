
import os
import sys
sys.path.insert(0, '..')

from pathlib import Path

from containers import *
from params import eaParams
from utilities import Utilities
from redundancy import Redundancy

"""

Individuals in the repertoires from each experiment are selected using
their fitness in the training arena before they're trimmed, evaluated
and assigned a fitness in the arena to be used going forward.

"""


class Combine():

    def __init__(self):

        self.save = False
        self.output_type = "final"
        self.go_away_from_food = "perceived"
        self.experiments = []

        self.params = eaParams()
        self.params.is_qdpy = True
        self.params.using_repertoire = False

        self.utilities = Utilities(self.params)
        self.utilities.setupToolbox(self.selTournament)
        self.redundancy = Redundancy(self.params)

        self.cancelled = False
        self.configure()
        self.cancelled = self.cancelled or "repro" in self.params.shared_path

        if self.cancelled:
            print("\nCancelled\n")
            return

        self.objective = self.params.objectives[self.params.indexes[0]]
        self.objective_name = self.objective+"-"+self.go_away_from_food+"-position" if self.objective == "ifood" else self.objective

        print()

    def configure(self):
        permitted = ["algorithm", "output_type", "experiment", "experiments",
                     "arena", "objective", "runs", "generations", "save"]
        with open(self.params.local_path+"/combine.txt", 'r') as f:
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
            algorithms = ["gp", "qdpy", "cma-es"]
            if data[1] in algorithms:
                self.params.algorithm = data[1]
            else:
                print("\nAlgorithm not recognised: "+data[1]+"\n")
                self.cancelled = True
        

        if data[0] == "output_type":
            algorithms = ["interim", "final"]
            if data[1] in algorithms:
                self.output_type = data[1]
            else:
                print("\nOutput not recognised: "+data[1]+"\n")
                self.cancelled = True

        if data[0] == "objective":
            self.params.indexes = [int(data[1])]
            self.params.description = self.params.objectives[int(data[1])]

        if data[0] == "experiments" and len(data) > 1:
            for i in range(1, len(data)):
                self.experiments.append(data[i])

        if data[0] == "experiment" and len(data) > 1: self.experiment = data[1]
        if data[0] == "arena" and len(data) > 1: self.params.arena_layout = int(data[1])
        if data[0] == "runs": self.params.runs = int(data[1])
        if data[0] == "generations": self.params.generations = int(data[1])
        if data[0] == "save": self.save = True if data[1] == "True" else False

    def makeContainersFromOtherExperiments(self):

        if self.cancelled:
            return

        containers = []
        self.checkContainerFiles()
        self.combineContainers(containers)
        if self.output_type == "final":
            self.evaluateRepertoires(containers)
        self.writeContainersToFile(containers)

    def checkContainerFiles(self):

        message = ""

        for experiment in self.experiments:

            missing = 0

            input_path = self.params.shared_path+"/"+self.params.algorithm+"/"+experiment+"/"+self.objective_name
            for seed in range(1, self.params.runs + 1):
                input_filename = input_path+"/"+str(seed)+"/checkpoint-"+self.objective+"-"+str(seed)+"-"+str(self.params.generations)+".txt"
                if not os.path.exists(input_filename):
                    missing += 1
                    
            if missing > 0:
                message += str(missing)+" files missing for "+experiment+"\n"

            if len(message) == 0:
                print("Found all files for "+experiment)

        if len(message) > 0:
            print(message)
            self.cancelled = True
            return
        else:
            print()

        if self.save:

            exists = False

            if self.output_type == "interim":
                output_path = self.params.shared_path+"/"+self.params.algorithm+"/"+self.experiment
                output_filename = output_path+"/"+self.objective_name+".txt"
                if os.path.exists(output_filename):
                    exists = True
            else:
                output_path = self.params.shared_path+"/gp/"+self.experiment+"/repertoires"
                for experiment in self.experiments:
                    output_filename = output_path+"/"+experiment+"/"+self.objective_name+"-"+str(self.params.generations)+".txt"
                    if os.path.exists(output_filename):
                        exists = True

            if exists:
                confirm = input("Output files already exist at "+output_path+"\n\nContinue? (y/N)\n")
                if confirm == "y":
                    print()
                else:
                    self.cancelled = True
                    print("Cancelled\n")

    def combineContainers(self, containers):

        if self.cancelled:
            return []

        experiments = [self.experiment] if self.output_type == "interim" else self.experiments

        for experiment in experiments:

            input_path = self.params.shared_path+"/"+self.params.algorithm+"/"+experiment+"/"+self.objective_name

            container = (Grid(shape = [8,8,8],
                              max_items_per_bin = 1,
                              fitness_domain = [(0.,1.0),],
                              features_domain = [(-40.0, 40.0), (-40.0, 40.0), (0.0, 1.0)],
                              storage_type=list))

            for seed in range(1, self.params.runs + 1):
                input_filename = input_path+"/"+str(seed)+"/checkpoint-"+self.objective+"-"+str(seed)+"-"+str(self.params.generations)+".txt"
                container = self.utilities.updateContainerFromString(self.redundancy, container, input_filename)

            containers.append(container)

    def evaluateRepertoires(self, containers):

        if self.cancelled:
            return

        self.params.local_path += "/1"
        Path(self.params.local_path+"/").mkdir(parents=False, exist_ok=True)
        self.utilities.saveConfigurationFile()

        for container in containers:
            print("Evaluating "+str(len(container))+" trees")
            self.evaluateRepertoire(container)

        self.params.deleteTempFiles()

    def evaluateRepertoire(self, container):

        invalid_ind = []
        for ind in container:
            invalid_ind.append(ind)

        self.utilities.evaluate(self.assignPopulationFitness, invalid_ind)
        for i in range(len(invalid_ind)):
            container[i].fitness.values = invalid_ind[i].fitness.values
            container[i].features = invalid_ind[i].features

    def writeContainersToFile(self, containers):

        if self.cancelled:
            return

        if self.output_type == "interim":
            experiments = [self.experiment]
            output_path = self.params.shared_path+"/"+self.params.algorithm+"/"+self.experiment
        else:
            experiments = self.experiments
            output_path = self.params.shared_path+"/gp/"+self.experiment+"/repertoires"

        print()

        for i in range(len(experiments)):

            if self.output_type == "interim":
                output_file = output_path+"/"+self.objective_name+".txt"
            else:
                output_file = output_path+"/"+experiments[i]+"/"+self.objective_name+"-"+str(self.params.generations)+".txt"
            print("Writing to "+output_file)

            if self.save:
                Path(output_path+"/"+experiments[i]).mkdir(parents=True, exist_ok=True)
                container_string = self.utilities.writeContainerToString(containers[i])
                with open(output_file, "w") as f:
                    f.write(container_string)

        print()

    def selTournament(self):
        return []

    def assignPopulationFitness(self, population, fitnesses):
        for ind, fit in zip(population, fitnesses):
            ind.fitness.values = fit[0]
            ind.features = fit[1]



if __name__ == "__main__":

    combine = Combine()
    combine.makeContainersFromOtherExperiments()

