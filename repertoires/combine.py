
import os
import sys
sys.path.insert(0, '..')

from pathlib import Path

# from containers import *
from grid import Grid

from params import eaParams
from utilities import Utilities
from redundancy import Redundancy

"""

To generate final repertoires src_experiments and dst_experiment need
to be set and config.txt needs to be aligned with the parameters to be
used going forwards. Individuals in the repertoires from each experiment
are selected using their fitness in the training arena before they're
trimmed, evaluated and assigned a fitness in the new arena.

Interim output type saves a combined repertoire to the root directory for
the given objective for easier access without changing its size and only
uses src_experiment and src_bins.

Repertoires for heterogeneous swarms need src_experiment and dst_experiment
set as well as destination. The recycle input type can be used along with
src_bins to generate incrementally smaller repertoires.

"""

class Combine():

    def __init__(self):

        self.params = eaParams()
        self.params.is_qdpy = True
        self.params.using_repertoire = False

        self.save = False
        self.legacy = False
        self.input = "separate"
        self.output_type = "final"
        self.runs = 0
        self.src_experiments = self.params.experiments
        self.src_experiment = self.params.experiment
        self.dst_experiment = self.params.experiment
        self.src_bins = self.params.nb_bins
        self.dst_bins = self.params.nb_bins
        self.domain = self.params.features_domain
        self.destination = self.params.algorithm

        self.cancelled = False
        self.params.configure()
        self.configure()
        self.cancelled = self.cancelled or "repro" in self.params.shared_path

        if self.cancelled:
            print("\nCancelled\n")
            return

        if self.output_type == "final" and len(self.src_experiments) == 0:
            print("\nSource experiments list cannot be empty for generating final repertoires\n")
            self.cancelled = True
            return

        self.utilities = Utilities(self.params)
        self.utilities.toolbox = self.utilities.setupToolboxGP(None)
        self.redundancy = Redundancy(self.params)

        self.params.description = self.params.objectives[self.params.indexes[0]]

        self.objective = self.params.objectives[self.params.indexes[0]]
        self.description = self.utilities.getExperimentDescription(self.params.indexes[0], self.params.repertoire_type)
        self.directory = self.utilities.getExperimentDirectory(self.params.indexes[0], self.params.repertoire_type)

        print()

    def configure(self):
        permitted = ["project", "algorithm", "input", "src_experiment", "src_experiments", "src_bins",
                     "dst_bins", "arena", "objective", "objectives", "domain", "runs", "generations",
                     "output_type", "repertoire_type", "destination", "dst_experiment", "save", "legacy"]
        with open(self.params.shared_path+"/combine.txt", 'r') as f:
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

        if data[0] == "destination":
            algorithms = ["gp", "qdpy", "ga"]
            if data[1] in algorithms:
                self.destination = data[1]
            else:
                print("\nDestination algorithm not recognised: "+data[1]+"\n")
                self.cancelled = True

        if data[0] == "input":
            types = ["separate", "combined", "recycle"]
            if data[1] in types:
                self.input = data[1]
            else:
                print("\nInput type not recognised: "+data[1]+"\n")
                self.cancelled = True

        if data[0] == "output_type":
            algorithms = ["interim", "heterogeneous", "final"]
            if data[1] in algorithms:
                self.output_type = data[1]
            else:
                print("\nOutput not recognised: "+data[1]+"\n")
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
            self.params.max_objectives = len(self.params.objectives)

        if data[0] == "objective":
            self.params.indexes = [int(data[1])]

        if data[0] == "src_experiments" and len(data) > 1:
            self.src_experiments = []
            for i in range(1, len(data)):
                self.src_experiments.append(data[i])

        if data[0] == "src_bins" and len(data) > 1:
            self.src_bins = []
            for bins in data[1:]:
                self.src_bins.append(int(bins))

        if data[0] == "dst_bins" and len(data) > 1:
            self.dst_bins = []
            for bins in data[1:]:
                self.dst_bins.append(int(bins))

        if data[0] == "domain" and len(data) > 1:
            self.domain = []
            for i in range(1, len(data), 2):
                self.domain.append((float(data[i]), float(data[i+1])))

        if data[0] == "project": self.params.project = data[1]
        if data[0] == "src_experiment" and len(data) > 1: self.src_experiment = data[1]
        if data[0] == "dst_experiment" and len(data) > 1: self.dst_experiment = data[1]
        if data[0] == "arena" and len(data) > 1: self.params.arena_layout = int(data[1])
        if data[0] == "runs": self.runs = int(data[1])
        if data[0] == "generations": self.params.generations = int(data[1])
        if data[0] == "save": self.save = True if data[1] == "True" else False
        if data[0] == "legacy": self.legacy = True if data[1] == "True" else False

    def makeContainersFromOtherExperiments(self):

        if self.cancelled:
            return

        containers = []
        self.checkContainerFiles()
        self.checkOutputFiles()
        self.combineContainers(containers)
        if self.output_type == "final":
            self.evaluateRepertoires(containers)
        self.writeContainersToFile(containers)

    def checkContainerFiles(self):

        message = ""

        experiments = self.src_experiments if self.output_type == "final" else [self.src_experiment]

        for experiment in experiments:

            missing = 0

            input_path = self.params.input_path+"/"+self.params.algorithm+"/"+experiment+"/"+self.directory

            if self.input == "combined":

                input_path = self.params.input_path+"/"+self.params.algorithm+"/"+experiment+"/"+self.directory
                input_file = input_path+"/"+self.objective+"-with-all-seeds-small-bins.txt"
                if not os.path.exists(input_file):
                    missing += 1
                    print(input_file)

            if self.input == "recycle":

                input_path = self.params.shared_path+"/"+self.destination+"/"+self.dst_experiment+"/"+self.description
                input_file = input_path+"/"+self.objective+"-"+str(self.src_bins[0])+"-bins.txt"
                if not os.path.exists(input_file):
                    missing += 1
                    print(input_file)

            if self.input == "separate":

                suffix = str(self.params.generations)+".txt" if self.legacy else str(self.params.generations)+"-"+self.objective+".txt"
                for seed in range(1, self.runs + 1):
                    input_file = input_path+"/"+str(seed)+"/checkpoint-"+self.description+"-"+str(seed)+"-"+suffix
                    if not os.path.exists(input_file):
                        missing += 1
                        print(input_file)

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

    def checkOutputFiles(self):

        if self.cancelled or not self.save:
            return

        exists = False

        if self.output_type == "interim":
            output_path = self.params.shared_path+"/"+self.params.algorithm+"/"+self.src_experiment+"/"+self.description
            output_filename = output_path+"/"+self.objective+".txt"
            if os.path.exists(output_filename):
                exists = True
        if self.output_type == "heterogeneous":
            output_path = self.params.shared_path+"/"+self.destination+"/"+self.dst_experiment+"/"+self.description
            output_filename = output_path+"/"+self.objective+"-"+str(self.dst_bins[0])+"-bins.txt"
            if os.path.exists(output_filename):
                exists = True
        else:
            output_path = self.params.shared_path+"/gp/"+self.dst_experiment+"/repertoires/"+self.params.repertoire_type
            for experiment in self.src_experiments:
                output_filename = output_path+"/"+experiment+"/"+self.objective+"-"+str(self.params.generations)+".txt"
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
            return

        experiments = self.src_experiments if self.output_type == "final" else [self.src_experiment]

        for experiment in experiments:

            bins = self.src_bins if self.output_type == "interim" else self.dst_bins
            container = self.utilities.createContainer(bins, self.domain, 1)

            if self.input == "combined":

                input_path = self.params.input_path+"/"+self.params.algorithm+"/"+experiment+"/"+self.directory
                input_filename = input_path+"/"+self.objective+"-with-all-seeds-small-bins.txt"
                self.readContainer(container, input_filename)

            if self.input == "recycle":

                input_path = self.params.shared_path+"/"+self.destination+"/"+self.dst_experiment+"/"+self.description
                input_filename = input_path+"/"+self.objective+"-"+str(self.src_bins[0])+"-bins.txt"
                self.readContainer(container, input_filename)

            if self.input == "separate":

                input_path = self.params.input_path+"/"+self.params.algorithm+"/"+experiment+"/"+self.directory
                suffix = str(self.params.generations)+".txt" if self.legacy else str(self.params.generations)+"-"+self.objective+".txt"
                for seed in range(1, self.runs + 1):
                    input_filename = input_path+"/"+str(seed)+"/checkpoint-"+self.description+"-"+str(seed)+"-"+suffix
                    self.readContainer(container, input_filename)

            print("\nPopulation: "+str(len(container.items()))+"\n")
            containers.append(container)

    def evaluateRepertoires(self, containers):

        if self.cancelled:
            return

        self.params.local_path += "/1"
        Path(self.params.local_path+"/").mkdir(parents=False, exist_ok=True)
        self.utilities.saveConfigurationFile()

        for container in containers:
            population = list(container.values()) if self.params.usingNewGrid else container
            print("Evaluating "+str(len(population))+" trees")
            self.evaluateRepertoire(population)

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

        if self.output_type == "final":
            experiments = self.src_experiments
            output_path = self.params.shared_path+"/gp/"+self.dst_experiment+"/repertoires/"+self.params.repertoire_type
        elif self.output_type == "heterogeneous":
            experiments = [self.dst_experiment]
            output_path = self.params.shared_path+"/"+self.destination+"/"+self.dst_experiment+"/"+self.description
        else:
            experiments = [self.src_experiment]
            output_path = self.params.shared_path+"/"+self.params.algorithm+"/"+self.src_experiment+"/"+self.description

        print()

        for i in range(len(experiments)):

            if self.output_type == "final":
                output_file = output_path+"/"+experiments[i]+"/"+self.objective+"-"+str(self.params.generations)+".txt"
            elif self.output_type == "heterogeneous":
                output_file = output_path+"/"+self.objective+"-"+str(self.dst_bins[0])+"-bins.txt"
            else:
                output_file = output_path+"/"+self.objective+".txt"

            if self.save:

                print("Writing to "+output_file)
                if self.output_type == "heterogeneous":
                    Path(output_path).mkdir(parents=True, exist_ok=True)
                if self.output_type == "final":
                    Path(output_path+"/"+experiments[i]).mkdir(parents=True, exist_ok=True)
                container_string = self.utilities.writeContainerToString(containers[i])

                path = ""
                path += "local:"+self.params.local_path+"\n"
                path += "shared:"+self.params.shared_path+"\n"
                path += "input:"+self.params.input_path+"\n"

                params = ""
                with open(self.params.shared_path+"/combine.txt", 'r') as f:
                    for line in f:
                        params += line

                with open(output_file, "w") as f:
                    f.write(container_string)
                    f.write("\n=====\n\n")
                    f.write(path+"\n")
                    f.write(params+"\n")
            else:
                print("Output file: "+output_file)

        print()

    def readContainer(self, container, input_filename):

        print("Reading from "+input_filename)
        container = self.utilities.updateContainerFromString(self.redundancy,
                                                             self.utilities.toolbox,
                                                             container,
                                                             input_filename,
                                                             0, 0, 0)

    def assignPopulationFitness(self, population, fitnesses):
        for ind, fit in zip(population, fitnesses):
            ind.fitness.values = fit[0]
            ind.features = fit[1]



if __name__ == "__main__":

    combine = Combine()
    combine.makeContainersFromOtherExperiments()

