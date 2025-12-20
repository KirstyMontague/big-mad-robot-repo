
import os
import sys
sys.path.insert(0, '..')

from pathlib import Path

from containers import *
from params import eaParams
from utilities import Utilities


class Combine():

    def __init__(self):

        self.go_away_from_food = "perceived"

        self.params = eaParams()
        self.params.is_qdpy = True
        self.params.using_repertoire = False

        self.utilities = Utilities(self.params)
        self.utilities.setupToolbox(self.selTournament)

        self.cancelled = False
        self.configure()
        self.cancelled = self.cancelled or "repro" in self.params.shared_path

        self.container_path = self.params.shared_path+"/"+self.params.algorithm+"/"+self.params.experiment

    def configure(self):
        permitted = ["algorithm", "experiment", "runs", "generations"]
        with open(self.params.local_path+"/config.txt", 'r') as f:
            for line in f:
                data = line.split()
                if len(data) > 0:
                    if data[0] in permitted:
                        print(line[0:-1])
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
        
        if data[0] == "experiment" and len(data) > 1: self.params.experiment = data[1]
        if data[0] == "runs": self.params.runs = int(data[1])
        if data[0] == "generations": self.params.generations = int(data[1])

    def checkContainerFiles(self):

        message = ""

        for objective in self.params.objectives:

            if objective == "foraging":
                continue

            missing = 0

            results_dir = self.container_path+"/"+objective
            if objective == "ifood":
                results_dir += "-"+self.go_away_from_food+"-position"

            for seed in range(1, self.params.runs + 1):
                input_filename = results_dir+"/"+str(seed)+"/checkpoint-"+objective+"-"+str(seed)+"-"+str(self.params.generations)+".txt"
                if not os.path.exists(input_filename):
                    missing += 1
                    
            if missing > 0:
                message += str(missing)+" files missing for "+objective+"\n"

        if len(message) == 0:
            print("\nFound all files\n")

        else:
            print("\n"+message)
            self.cancelled = True

    def combineContainers(self):

        confirmed = False

        for objective in self.params.objectives:

            if objective == "foraging":
                continue

            output_filename = self.container_path+"/"+objective
            if objective == "ifood":
                output_filename += "-"+self.go_away_from_food+"-position"
            output_filename += ".txt"

            if not confirmed and os.path.exists(output_filename):
                test = input("Container files already exist at "+self.container_path+"\nContinue? (y/N)\n")
                if test == "y":
                    confirmed = True
                    print()
                else:
                    print("\nCancelled\n")
                    return

            results_dir = self.container_path+"/"+objective
            if objective == "ifood":
                results_dir += "-"+self.go_away_from_food+"-position"

            container = (Grid(shape = [8,8,8],
                              max_items_per_bin = 3,
                              fitness_domain = [(0.,1.0),],
                              features_domain = [(-40.0, 40.0), (-40.0, 40.0), (0.0, 1.0)],
                              storage_type=list))

            for seed in range(1, self.params.runs + 1):
                input_filename = results_dir+"/"+str(seed)+"/checkpoint-"+objective+"-"+str(seed)+"-"+str(self.params.generations)+".txt"
                container = self.utilities.readContainerFromString(container, input_filename)

            print("Writing to "+output_filename)

            container_string = self.utilities.writeContainerToString(container)

            with open(output_filename, "w") as f:
                 f.write(container_string)

    def selTournament(self):
        return []



if __name__ == "__main__":

    combine = Combine()

    if combine.cancelled:
        print("\naborted\n")

    else:
        combine.checkContainerFiles()

        if not combine.cancelled:
            combine.combineContainers()

