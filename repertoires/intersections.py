
import os
import sys
sys.path.insert(0, '..')

from pathlib import Path

from containers import *
from params import eaParams
from utilities import Utilities
from redundancy import Redundancy


class Intersections():

    def __init__(self):

        self.params = eaParams()

        self.save = self.params.saveOutput
        self.from_csv = False
        self.whole_repertoire = False
        self.count_duplicates = False

        self.params.algorithm = "gp"
        self.params.description = "foraging"
        self.params.using_repertoire = True

        self.cancelled = False

        self.configure()
        print()

        self.redundancy = Redundancy(self.params)
        if self.save:
            Path(self.params.shared_path+"/gp/"+self.params.experiment+"/intersections").mkdir(parents=True, exist_ok=True)

        self.experiments = {}
        for experiment in self.params.experiments:
            self.experiments[experiment] = {}

        self.objectives = {
                            "increaseDensity": {"filename": "density", "behaviours" : {}},
                            "gotoNest": {"filename": "nest", "behaviours" : {}},
                            "gotoFood": {"filename": "food", "behaviours" : {}},
                            "reduceDensity": {"filename": "idensity", "behaviours" : {}},
                            "goAwayFromNest": {"filename": "inest", "behaviours" : {}},
                            "goAwayFromFood": {"filename": "ifood-perceived-position", "behaviours" : {}},
                          }
        self.getSubBehaviours()

    def configure(self):
        permitted = ["repertoire_type", "bins_per_axis", "experiment", "experiments", "generations",
                     "from_csv", "whole_repertoire", "count_duplicates", "save"]
        with open(self.params.local_path+"/intersections.txt", 'r') as f:
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

        if data[0] == "experiments":
            for i in range(1, len(data)):
                self.params.experiments.append(data[i])

        if data[0] == "repertoire_type":
            self.params.repertoire_type = data[1]

        if data[0] == "bins_per_axis":
            self.params.bins_per_axis = int(data[1])
            self.params.repertoire_size = self.params.bins_per_axis ** self.params.characteristics

        if data[0] == "generations":
            self.params.generations = int(data[1])

        if data[0] == "from_csv":
            self.from_csv = True if data[1] == "True" else False

        if data[0] == "whole_repertoire":
            self.whole_repertoire = True if data[1] == "True" else False

        if data[0] == "count_duplicates":
            self.count_duplicates = True if data[1] == "True" else False

        if data[0] == "save":
            self.save = True if data[1] == "True" else False

    def saveToFile(self, output, suffix):

        if suffix == "duplicates":
            filename = suffix
        else:
            filename = self.params.repertoire_type + str(self.params.repertoire_size)+"-"+suffix
        filename = self.params.shared_path+"/gp/"+self.params.experiment+"/intersections/"+filename+".txt"

        if self.save:

            confirm = input("Output file already exists at "+filename+"\n\nContinue? (y/N)\n")
            if confirm == "y":
                print()
            else:
                print("Cancelled\n")
                return

            config = ""
            with open(self.params.local_path+"/intersections.txt", 'r') as f:
                for line in f:
                    config += line

            print("Writing to "+filename+"\n")
            with open(filename, "w") as f:
                f.write(config+"\n")
                f.write(output+"\n")

        else:
            print("Output filename: "+filename)

        print()

    def getSubBehaviours(self):

        # get trees from sub-behaviours.txt

        repertoire = self.params.repertoire_type + str(self.params.repertoire_size)
        dst = self.params.shared_path+"/gp/"+self.params.experiment+"/foraging/"+repertoire+"/sub-behaviours.txt"

        with open(dst, "r") as f:
            for line in f:
                for objective, data in self.objectives.items():
                    if objective in line:
                        info = line.split(" ", 1)
                        data["behaviours"][info[0]] = info[1][0:-1]

        # get sub-behaviours from each arena for each objective

        for experiment, behaviours in self.experiments.items():
            for objective, data in self.objectives.items():
                behaviours[objective] = []
 
                src_path = self.params.shared_path+"/gp/"+self.params.experiment+"/repertoires/"+experiment
                src_name = src_path+"/"+data["filename"]+"-"+str(self.params.generations)+".txt"
                with open(src_name, "r") as f:
                    for line in f:
                        data = line.split(":")
                        behaviours[objective].append(data[0])

    def fromCSV(self):

        repertoire = self.params.repertoire_type + str(self.params.repertoire_size)
        csv_filename = self.params.shared_path+"/gp/"+self.params.experiment+"/"
        csv_filename += "foraging/"+repertoire+"/best"+str(self.params.generations)+".csv"

        print("Reading from "+csv_filename+"\n")

        chromosomes = []
        with open(csv_filename, "r") as f:
            for line in f:
                sections = line.split("\"")
                columns = sections[0].split(",")
                if columns[0] not in ["Type", "Objective"]:
                    chromosomes.append(sections[1])

        output = ""
        for i in range(len(chromosomes)):
            chromosome = chromosomes[i]
            output += "---- seed "+str(i+1)+" ------------------------------------\n\n"
            trimmed = self.redundancy.trim(chromosome)
            output += chromosome+"\n\n"
            output += str(trimmed)+"\n\n"
            output += self.fromChromosome(str(trimmed))+"\n"
        print(output)

        self.saveToFile(output, "from-csv")

    def fromChromosome(self, chromosome):

        occurences = {}
        
        chromosome = chromosome.replace("(", " ")
        chromosome = chromosome.replace(")", "")
        chromosome = chromosome.replace(",", "")

        tokens = chromosome.split(" ")
        tokens = set(tokens)
        
        for objective, data in self.objectives.items():
            occurences[objective] = {}
            for token in tokens:
                if objective in token:
                    tree = data["behaviours"][token]
                    occurences[objective][token] = tree

        output = ""
        for objective, data in occurences.items():
            for name, tree in data.items():
                output += self.getMatches(objective, name, tree)

        return output

    def wholeRepertoire(self):

        repertoire = self.params.repertoire_type + str(self.params.repertoire_size)
        filename = self.params.shared_path+"/gp/"+self.params.experiment+"/intersections/"+repertoire+"-sources.txt"

        output = ""
        for objective, data in self.objectives.items():
            for behaviour, tree in data["behaviours"].items():
                output += self.getMatches(objective, behaviour, tree)
            output += "\n"
        print(output)

        self.saveToFile(output, "sources")

    def countDuplicates(self):
        
        experiments = []
        for experiment, data in self.experiments.items():
            experiments.append(experiment)

        output = ""

        for objective, data in self.objectives.items():

            output += "--------\n\n"

            for i in range(len(experiments)):
                for j in range(i+1, len(experiments)):
                    
                    repertoire1 = set(self.experiments[experiments[i]][objective])
                    repertoire2 = set(self.experiments[experiments[j]][objective])
                    intersection = set.intersection(repertoire1, repertoire2)
                    output += experiments[i]+" vs "+experiments[j]+"   "+str(len(intersection))+" duplicates\n"

            total_intersection = set(self.experiments[experiments[0]][objective])
            for i in range(1, len(experiments)):
                
                repertoire = set(self.experiments[experiments[i]][objective])
                total_intersection = set.intersection(total_intersection, repertoire)

            output += "\nDuplicated in all repertoires: "+str(len(total_intersection))+"\n\n"

        print(output)

        self.saveToFile(output, "duplicates")

    def getMatches(self, objective, name, tree):

        found = []
        for experiment, objectives in self.experiments.items():
            behaviours = objectives[objective]
            found.append("yes" if tree in behaviours else "no")

        if len(tree) > 100: tree = tree[0:97]+"..."
        output = ""
        for result in found:
            output += result+"\t|  "
        output += name+"    \t|  "+tree+"\n"
        return output

if __name__ == "__main__":

    intersections = Intersections()

    if not intersections.cancelled:

        if intersections.from_csv:
            intersections.fromCSV()

        if intersections.whole_repertoire:
            intersections.wholeRepertoire()

        if intersections.count_duplicates:
            intersections.countDuplicates()
