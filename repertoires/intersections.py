
import sys
sys.path.insert(0, '..')

from params import eaParams
from utilities import Utilities
from redundancy import Redundancy


class Intersections():

    def __init__(self):

        self.params = eaParams()
        self.params.configure()
        print()

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
 
                src = self.params.shared_path+"/gp/"+self.params.experiment+"/repertoires/"+experiment+"/"+data["filename"]+".txt"
                with open(src, "r") as f:
                    for line in f:
                        data = line.split(":")
                        behaviours[objective].append(data[0])

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

        for objective, data in occurences.items():
            for name, tree in data.items():
                self.printMatches(objective, name, tree)

        print()

    def wholeRepertoire(self):

        for objective, data in self.objectives.items():
            for behaviour, tree in data["behaviours"].items():
                self.printMatches(objective, behaviour, tree)
            print()

    def printMatches(self, objective, name, tree):
                found = []
                for experiment, objectives in self.experiments.items():
                    behaviours = objectives[objective]
                    found.append("yes" if tree in behaviours else "no")

                if len(tree) > 100: tree = tree[0:97]+"..."
                print(found[0]+"\t|  "+found[1]+"\t|  "+found[2]+"\t|  "+name+"    \t|  "+tree)

    def countDuplicates(self):
        
        experiments = []
        for experiment, data in self.experiments.items():
            experiments.append(experiment)

        for objective, data in self.objectives.items():

            for i in range(len(experiments)):
                for j in range(i+1, len(experiments)):
                    
                    repertoire1 = set(self.experiments[experiments[i]][objective])
                    repertoire2 = set(self.experiments[experiments[j]][objective])
                    intersection = set.intersection(repertoire1, repertoire2)
                    print(experiments[i]+" vs "+experiments[j]+"   "+str(len(intersection))+" duplicates")

            print("---")

            total_intersection = set(self.experiments[experiments[0]][objective])
            for i in range(1, len(experiments)):
                
                repertoire = set(self.experiments[experiments[i]][objective])
                total_intersection = set.intersection(total_intersection, repertoire)
                
            print("Duplicated in all repertoires: "+str(len(total_intersection)))

            print("-----------------")


if __name__ == "__main__":

    example = "seqm4(gotoNest6, reduceDensity3, increaseDensity1, seqm3(gotoFood2, increaseDensity3, increaseDensity4))"

    intersections = Intersections()
    intersections.fromChromosome(example)
    intersections.wholeRepertoire()
    intersections.countDuplicates()
