
import sys
sys.path.insert(0, '..')

import os
from pathlib import Path
import pprint

from containers import *
from params import eaParams
from utilities import Utilities
from redundancy import Redundancy


class Intersections():

    def __init__(self):

        self.params = eaParams()

        self.save = self.params.saveOutput
        self.legacy = False
        self.from_csv = False
        self.whole_repertoire = False
        self.count_duplicates = False
        self.count_sources = False
        self.count_behaviours = False

        self.params.algorithm = "gp"
        self.params.description = "foraging"
        self.params.using_repertoire = True

        self.cancelled = False

        self.configure()
        print()

        # redundancy uses the repertoire at shared_path for adding nodes
        # so need to shoehorn the input path in to use the right repertoire
        # before reverting to shared_path's initial value
        shared_path_backup = self.params.shared_path
        self.params.shared_path = self.params.input_path
        self.redundancy = Redundancy(self.params)
        self.params.shared_path = shared_path_backup

        if self.save:
            Path(self.params.home_path+"/gp/"+self.params.experiment+"/intersections").mkdir(parents=True, exist_ok=True)

        self.repertoires = {}
        for experiment in self.params.experiments:
            self.repertoires[experiment] = {}

        self.objectives = {
                            "increaseDensity":  {"behaviours" : {}, "usage_qty" : 0, "total_qty" : 0, "chromosomes_qty" : 0, "filename": "density"},
                            "gotoNest":         {"behaviours" : {}, "usage_qty" : 0, "total_qty" : 0, "chromosomes_qty" : 0, "filename": "nest"},
                            "gotoFood":         {"behaviours" : {}, "usage_qty" : 0, "total_qty" : 0, "chromosomes_qty" : 0, "filename": "food"},
                            "reduceDensity":    {"behaviours" : {}, "usage_qty" : 0, "total_qty" : 0, "chromosomes_qty" : 0, "filename": "idensity"},
                            "goAwayFromNest":   {"behaviours" : {}, "usage_qty" : 0, "total_qty" : 0, "chromosomes_qty" : 0, "filename": "inest"},
                            "goAwayFromFood":   {"behaviours" : {}, "usage_qty" : 0, "total_qty" : 0, "chromosomes_qty" : 0, "filename": "ifood-perceived-position"},
                          }

        self.chromosomes = [] # not trimmed
        self.all_tokens = [] # trimmed

        self.getSubBehaviours()
        self.countSubBehavioursFromCsv()

    def configure(self):
        permitted = ["repertoire_type", "bins_per_axis", "experiment", "experiments", "generations",
                     "from_csv", "whole_repertoire", "count_duplicates", "count_sources", "count_behaviours", "save", "legacy"]
        with open(self.params.shared_path+"/intersections.txt", 'r') as f:
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
            self.params.experiments = []
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

        if data[0] == "count_sources":
            self.count_sources = True if data[1] == "True" else False

        if data[0] == "count_behaviours":
            self.count_behaviours = True if data[1] == "True" else False

        if data[0] == "save":
            self.save = True if data[1] == "True" else False

        if data[0] == "legacy":
            self.legacy = True if data[1] == "True" else False

    def saveToFile(self, output, suffix):

        filename = self.params.home_path+"/gp/"+self.params.experiment+"/intersections/"
        if suffix == "duplicates":
            filename += suffix+".txt"
        else:
            filename += self.params.repertoire_type + str(self.params.repertoire_size)+"-"+suffix+".csv"

        print()

        if self.save:

            if os.path.exists(filename):
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

        missing = []

        # get trees from sub-behaviours.txt

        repertoire = self.params.repertoire_type + str(self.params.repertoire_size)
        dst = self.params.input_path+"/gp/"+self.params.experiment+"/foraging/"+repertoire+"/sub-behaviours.txt"

        if not os.path.exists(dst):
            missing.append(dst)

        else:
            print("Reading sub-behaviours file from "+dst+"\n")
            with open(dst, "r") as f:
                for line in f:
                    for objective, data in self.objectives.items():
                        if objective in line:
                            info = line.split(" ", 1)
                            data["behaviours"][info[0]] = {"tree" : info[1].strip('\t\n\r'), "total_qty" : 0, "chromosomes_qty" : 0}

        # get sub-behaviours from each arena for each objective

        for experiment, behaviours in self.repertoires.items():

            src_path = self.params.input_path+"/gp/"+self.params.experiment+"/repertoires"
            if not self.legacy:
                src_path += "/"+self.params.repertoire_type
            src_path += "/"+experiment
            print("Reading imported repertoires from "+src_path)

            for objective, objective_data in self.objectives.items():
                behaviours[objective] = []
 
                src_name = src_path+"/"+objective_data["filename"]+"-"+str(self.params.generations)+".txt"

                if not os.path.exists(src_name):
                    missing.append(src_name)
                else:
                    with open(src_name, "r") as f:
                        for line in f:
                            data = line.split(":")
                            behaviours[objective].append(data[0])
        print()

        if len(missing) > 0:
            print(str(len(missing))+" files missing\n")
            for name in missing:
                print(name)
            print()
            self.cancelled = True

    def countSubBehavioursFromCsv(self):

        repertoire = self.params.repertoire_type + str(self.params.repertoire_size)
        csv_filename = self.params.input_path+"/gp/"+self.params.experiment+"/"
        csv_filename += "foraging/"+repertoire+"/best"+str(self.params.generations)+".csv"

        print("Reading from "+csv_filename+"\n")

        try:
            with open(csv_filename, "r") as f:
                for line in f:
                    sections = line.split("\"")
                    columns = sections[0].split(",")
                    if columns[0] not in ["Type", "Objective"]:
                        self.chromosomes.append(sections[1])
        except FileNotFoundError as e:
            print(str(e)+"\n")
            print("Cancelled\n")
            return

        for i in range(len(self.chromosomes)):
            chromosome = str(self.redundancy.trim(self.chromosomes[i]))
            chromosome = chromosome.replace("(", " ")
            chromosome = chromosome.replace(")", "")
            chromosome = chromosome.replace(",", "")
            tokens = chromosome.split(" ")

            for token in tokens:
                for objective, data in self.objectives.items():
                    if objective in token:
                        self.all_tokens.append(token)

            for token in set(tokens):
                for objective, data in self.objectives.items():
                    if objective in token:
                        data["behaviours"][token]["chromosomes_qty"] += 1
                        data["chromosomes_qty"] += 1

        for token in self.all_tokens:
            for objective, data in self.objectives.items():
                if objective in token:
                    data["behaviours"][token]["total_qty"] += 1
                    data["total_qty"] += 1

        for objective, data in self.objectives.items():
            for chromosome in self.chromosomes:
                if objective in chromosome:
                    data["usage_qty"] += 1

    def fromCSV(self):

        for i in range(len(self.chromosomes)):
            trimmed = self.redundancy.trim(self.chromosomes[i])
            self.fromChromosome(str(trimmed))

        csv = ""
        for objective, objective_data in self.objectives.items():
            for subbehaviour, subbehaviour_data in objective_data["behaviours"].items():
                if subbehaviour_data["total_qty"] > 0:
                    for found in subbehaviour_data["found"]:
                        csv += str(found)+","
                    csv += ","
                    csv += subbehaviour+","
                    csv += str(subbehaviour_data["total_qty"])+",,"
                    csv += "\""+str(subbehaviour_data["tree"])+"\"\n"
            csv += "\n"
        print(csv)

        self.saveToFile(csv, "from-csv")

    def fromChromosome(self, chromosome):

        chromosome = chromosome.replace("(", " ")
        chromosome = chromosome.replace(")", "")
        chromosome = chromosome.replace(",", "")

        tokens = chromosome.split(" ")
        
        for objective, data in self.objectives.items():
            for token in tokens:
                if objective in token:
                    data["behaviours"][token]["total_qty"] += 1
            for token in set(tokens):
                if objective in token:
                    data["behaviours"][token]["chromosomes_qty"] += 1

        for objective, objective_data in self.objectives.items():
            for subbehaviour, subbehaviour_data in objective_data["behaviours"].items():
                if subbehaviour_data["chromosomes_qty"] > 0:
                    self.getMatches(objective, subbehaviour_data)

    def wholeRepertoire(self):

        repertoire = self.params.repertoire_type + str(self.params.repertoire_size)
        filename = self.params.input_path+"/gp/"+self.params.experiment+"/intersections/"+repertoire+"-sources.txt"

        for objective, objective_data in self.objectives.items():
            for subbehaviour, subbehaviour_data in objective_data["behaviours"].items():
                self.getMatches(objective, subbehaviour_data)

        csv = ""
        for objective, objective_data in self.objectives.items():
            for subbehaviour, subbehaviour_data in objective_data["behaviours"].items():
                for found in subbehaviour_data["found"]:
                    csv += str(found)+","
                csv += ","
                csv += subbehaviour+",,"
                csv += "\""+str(subbehaviour_data["tree"])+"\"\n"
            csv += "\n"
        print(csv)

        self.saveToFile(csv, "sources")

    def countDuplicates(self):

        experiments = []
        for experiment, data in self.repertoires.items():
            experiments.append(experiment)

        output = ""

        for objective, data in self.objectives.items():

            output += "--------\n\n"

            output += objective+"\n\n"

            for i in range(len(experiments)):
                for j in range(i+1, len(experiments)):
                    
                    repertoire1 = set(self.repertoires[experiments[i]][objective])
                    repertoire2 = set(self.repertoires[experiments[j]][objective])
                    intersection = set.intersection(repertoire1, repertoire2)
                    output += experiments[i]+" vs "+experiments[j]+"   "+str(len(intersection))+" duplicates\n"

            total_intersection = set(self.repertoires[experiments[0]][objective])
            for i in range(1, len(experiments)):

                repertoire = set(self.repertoires[experiments[i]][objective])
                total_intersection = set.intersection(total_intersection, repertoire)

            output += "\nDuplicated in all repertoires: "+str(len(total_intersection))+"\n\n"

        output += "--------\n"
        print(output)

        self.saveToFile(output, "duplicates")

    def getMatches(self, objective, subbehaviour_data):

        tree = subbehaviour_data["tree"]

        found = []
        for experiment, objectives in self.repertoires.items():
            behaviours = objectives[objective]
            found.append("yes" if tree in behaviours else "no")
        subbehaviour_data["found"] = found

    def countBehaviourSources(self):

        print("=====================================================================")
        print("How many subbehaviours in the results from each arena (per objective)")
        print("=====================================================================")

        print()
        for objective, objective_data in self.objectives.items():
            experiments = {}
            for experiment, objectives in self.repertoires.items():
                experiments[experiment] = 0

            # get the trees for this objective's subbehaviours
            trees = []
            for subbehaviour, subbehaviour_data in objective_data["behaviours"].items():
                trees.append(subbehaviour_data["tree"])
            trees = set(trees)

            # count how many appear in the repertoire generated by each
            # arena and add to total for this arena and objective
            for experiment, objectives in self.repertoires.items():
                behaviours = set(objectives[objective])
                experiments[experiment] += len(set.intersection(trees, behaviours))

            # print how many subtrees from behaviours.txt in the results from each arena
            print(objective+"\t"+str(experiments))
        print()

    def countCsvBehavioursTotalAndPerArena(self):

        print("======================================")
        print("how many subbehaviours from each arena")
        print("======================================")

        # create entries for every subbehaviour that appears in the csv
        # with default totals for each subbehaviour and for their objective

        experiments = {}
        for experiment in self.params.experiments:
            experiments[experiment] = {}
            for objective, data in self.objectives.items():
                experiments[experiment][objective] = {}
                experiments[experiment][objective]["total"] = 0

        for objective in self.objectives:
            for token in set(self.all_tokens):
                if objective in token:
                    tree = self.objectives[objective]["behaviours"][token]["tree"]
                    for arena, objectives in self.repertoires.items():
                        behaviours = objectives[objective]
                        if tree in behaviours:
                            experiments[arena][objective][token] = 0

        # for each arena log how many times each objective and subbehaviour
        # appears by counting how many times they occur in the list of all tokens

        for arena, objectives in experiments.items():
            for objective, subbehaviours in objectives.items():
                for subbehaviour, qty in subbehaviours.items():
                    subbehaviours["total"] += self.all_tokens.count(subbehaviour)
                    subbehaviours[subbehaviour] += self.all_tokens.count(subbehaviour)

        # for each arena print how many times each subbehaviour is used

        print("\nHow many times did a subbehviour from the csv appear in the results from each arena\n")
        for arena, objectives in experiments.items():
            print(arena)
            for objective, data in objectives.items():
                print("\t"+objective+": "+str(data["total"]))
            print()

        # how many subbehaviours in total

        print("How many subbehviours in all results")
        total = 0
        for objective, data in self.objectives.items():
            total += data["total_qty"]
        print("\nTotal: "+str(total))
        print()

        # how many subbehaviours per arena

        print("How many subbehviours from each arena (with duplication)\n")
        for arena, objectives in experiments.items():
            total_this_arena = 0
            for subbehaviour, info in objectives.items():
                total_this_arena += objectives[subbehaviour]["total"]
            print(arena+": "+str(total_this_arena))
        print()

    def countCsvBehavioursTotalAndSeeds(self):

        print("=================================================")
        print("how many chromosomes contain each subbehaviour")
        print("how many times each subbehaviour appears in total")
        print("where subbehaviours came from")
        print("=================================================")

        # log which arena(s) contain each subbehaviour

        for token in set(self.all_tokens):
            for objective, data in self.objectives.items():
                if objective in token:
                    tree = data["behaviours"][token]["tree"]
                    data["behaviours"][token]["arenas"] = {}
                    for experiment, objectives in self.repertoires.items():
                        behaviours = objectives[objective]
                        data["behaviours"][token]["arenas"][experiment] = True if tree in behaviours else False


        # print how many chromosomes contain each objective and
        # how many times each objective appears in total

        print()
        for objective, objective_data in self.objectives.items():
            if objective_data["total_qty"] > 0:
                print(objective+": seeds "+str(objective_data["chromosomes_qty"])+", total "+str(objective_data["total_qty"]))
                for subbehaviour, subbehaviour_data in objective_data["behaviours"].items():
                    if subbehaviour_data["total_qty"] > 0:
                        print(subbehaviour+" "+str(subbehaviour_data["arenas"]))
                print()

    def countCsvBehavioursTotalAndSeeds(self):

        print("=================================================")
        print(" how many chromosomes contain each objective and")
        print(" how many times each objective appears in total")
        print("=================================================")

        csv = ""

        # csv += "Experiment,type,size,density,nest,food,idensity,inest,ifood\n"

        csv += self.params.experiment+","
        csv += self.params.repertoire_type+","
        csv += str(self.params.repertoire_size)+","

        output = ""
        for objective, objective_data in self.objectives.items():
            if objective_data["total_qty"] > 0:
                output += objective+":       \t"
                output += "seeds with objective "+str(objective_data["usage_qty"])+"  \t"
                output += "seeds with subbehaviour "+str(objective_data["chromosomes_qty"])+" \t"
                output += "total occurences "+str(objective_data["total_qty"])
                output += "\n"
                csv += str(objective_data["usage_qty"])+","
        csv += "\n"

        print("\n"+output+"\n")

        print("\n"+csv+"\n")

        # filename = self.params.home_path+"/gp/intersections.csv"
        # with open(filename, "a") as f:
            # f.write(csv)

if __name__ == "__main__":

    intersections = Intersections()

    if not intersections.cancelled:

        if intersections.from_csv:
            intersections.fromCSV()

        if intersections.whole_repertoire:
            intersections.wholeRepertoire()

        if intersections.count_duplicates:
            intersections.countDuplicates()

        if intersections.count_sources:
            intersections.countCsvBehavioursTotalAndPerArena()
            intersections.countBehaviourSources()
            intersections.countCsvBehavioursTotalAndSeeds()

        if intersections.count_behaviours:
            intersections.countCsvBehavioursTotalAndSeeds()
