
import os
import sys
sys.path.insert(0, '..')

from pathlib import Path

class Aggregator():

    def __init__(self):

        self.objectives = ["density", "nest", "food", "idensity", "inest", "ifood", "foraging"]

        with open("../path.txt", "r") as f:
            for line in f:
                data = line.split(":")
                if data[0] == "home": self.home_path = data[1][0:-1]
                if data[0] == "local": self.local_path = data[1][0:-1]
                if data[0] == "shared": self.shared_path = data[1][0:-1]

        self.algorithm = "gp"
        self.using_repertoire = False
        self.repertoire_type = "qd"
        self.repertoire_size = 1
        self.objective = self.objectives[0]
        self.runs = 0
        self.generations = 0

        self.cancelled = False

        self.configure()
        self.cancelled = self.cancelled or "repro" in self.shared_path

    def configure(self):
        permitted = ["algorithm", "using_repertoire", "repertoire_type", "repertoire_size", "objective", "runs", "generations"]
        with open(self.local_path+"/config.txt", 'r') as f:
            for line in f:
                data = line.split()
                if len(data) > 0:
                    if data[0] in permitted:
                        print(line[0:-1])
                        self.update(data)
                    else:
                        print("\nconfig entry not recognised: "+data[0]+"\n")
                        self.cancelled = True

    def update(self, data):
        if data[0] == "algorithm":
            algorithms = ["gp", "qdpy", "cma-es"]
            if data[1] in algorithms:
                self.algorithm = data[1]
            else:
                print("\nalgorithm not recognised: "+data[1]+"\n")
                self.cancelled = True
        if data[0] == "using_repertoire": self.using_repertoire = True if data[1] == "True" else False
        if data[0] == "repertoire_type": self.repertoire_type = data[1]
        if data[0] == "repertoire_size": self.repertoire_size = int(data[1])
        if data[0] == "objective": self.objective = self.objectives[int(data[1])]
        if data[0] == "runs": self.runs = int(data[1])
        if data[0] == "generations": self.generations = int(data[1])

    def addRepertoireDir(self, path):
        if self.objective == "foraging" and self.algorithm == "gp":
            if self.using_repertoire:
                path += "/"+self.repertoire_type+str(self.repertoire_size)
            else:
                path += "/baseline"
        return path

    def getResults(self):

        path = self.shared_path+"/"+self.algorithm+"/"+self.objective
        path = self.addRepertoireDir(path)
        print("\nreading from "+path+"\n")

        results_per_query = []

        for query in self.queries:

            entries = []

            for i in range(1, self.runs + 1):

                filename = path+"/"+query+str(self.generations)+"-"+str(i)+".csv"

                if os.path.exists(filename):

                    with open(filename, "r") as f:

                        indexes = []
                        horizontal_data = []

                        for line in f:

                            columns = line.split(",")

                            if len(entries) == 0 and columns[0] in ["Type", "Objective"]:
                                entries.append(line)

                            if columns[0] not in ["Type", "Objective"]:
                                entries.append(line)
                                break

                else:
                    print(filename+" not found")

            results_per_query.append(entries)

        return results_per_query

    def writeCSV(self, results_per_query):

        Path(self.home_path+"/"+self.algorithm+"/").mkdir(parents=False, exist_ok=True)
        
        filepath = self.home_path+"/"+self.algorithm+"/"+self.objective
        Path(filepath).mkdir(parents=False, exist_ok=True)

        filepath = self.addRepertoireDir(filepath)
        Path(filepath).mkdir(parents=False, exist_ok=True)

        print()
        confirmed = False

        for i in range(len(self.queries)):

            query = self.queries[i]
            entries = results_per_query[i]

            if len(entries) > 0:

                filename = filepath+"/"+query+str(self.generations)+".csv"

                if not confirmed and os.path.exists(filename):

                    test = input("Output files already exist at "+filepath+"\nContinue? (y/N)\n")
                    if test == "y":
                        confirmed = True
                        print()
                    else:
                        print("\ncancelled\n")
                        return False

                print("Writing "+filename)
                with open(filename, "w") as f:
                    for entry in entries:
                        f.write(entry)

        return True

    def removeOldFiles(self):

        print()
        test = input("Delete input files? (y/N)\n")
        if test != "y":
            print("\ncancelled\n")
            return

        path = self.shared_path+"/"+self.algorithm+"/"+self.objective
        path = self.addRepertoireDir(path)
        print("\ndeleting from "+path)

        for query in self.queries:

            for i in range(1, self.runs + 1):

                filename = path+"/"+query+str(self.generations)+"-"+str(i)+".csv"

                if os.path.exists(filename):
                    os.remove(filename)
                    print(filename+" removed")
                else:
                    print(filename+" not found")
            print()


if __name__ == "__main__":

    aggregator = Aggregator()

    if aggregator.cancelled:
        print("\naborted\n")

    else:
        aggregator.queries = ["best", "qd-scores", "coverage"]
        if aggregator.algorithm == "cma-es":
            aggregator.queries = ["best"]

        results_per_query = aggregator.getResults()
        results_saved = aggregator.writeCSV(results_per_query)

        if results_saved:
           aggregator.removeOldFiles()
