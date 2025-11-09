
import os
import sys
sys.path.insert(0, '..')

from params import eaParams
from pathlib import Path

class Aggregator():

    def __init__(self):
        self.params = eaParams()
        self.algorithm = "gp"
        self.objective = self.params.objectives[0]
        self.runs = 0
        self.generations = 0
        self.configure()

    def configure(self):
        with open(self.params.local_path+"/config.txt", 'r') as f:
            for line in f:
                data = line.split()
                if len(data) > 0:
                    print(line[0:-1])
                    self.update(data)

    def update(self, data):
        if data[0] == "algorithm": self.algorithm = data[1]
        if data[0] == "objective": self.objective = self.params.objectives[int(data[1])]
        if data[0] == "runs": self.runs = int(data[1])
        if data[0] == "generations": self.generations = int(data[1])

    def getResults(self):

        print("\nreading...")
        results_per_query = []

        for query in self.queries:

            path = self.params.shared_path+"/"+self.algorithm+"/"+self.objective+"/"+query

            entries = []

            for i in range(1, self.runs + 1):

                filename = path+str(self.generations)+"-"+str(i)+".csv"

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

        print("\nwriting...")
        Path(self.params.local_path+"/"+self.algorithm+"/").mkdir(parents=False, exist_ok=True)
        confirmed = False

        for i in range(len(self.queries)):

            query = self.queries[i]
            entries = results_per_query[i]

            if len(entries) > 0:

                filename = self.params.local_path+"/"+self.algorithm+"/"+query+str(self.generations)+"-"+self.objective+".csv"

                if not confirmed and os.path.exists(filename):
                    test = input("Output files already exist. Continue? (y/N)\n")
                    if test == "y":
                        confirmed = True
                        print()
                    else:
                        return False

                with open(filename, "w") as f:
                    for entry in entries:
                        f.write(entry)

        return True

    def removeOldFiles(self):

        print("\ndeleting...")
        for query in self.queries:

            path = self.params.shared_path+"/"+self.algorithm+"/"+self.objective+"/"+query

            for i in range(1, self.runs + 1):

                filename = path+str(self.generations)+"-"+str(i)+".csv"

                if os.path.exists(filename):
                    os.remove(filename)
                    print(filename+" removed")
                else:
                    print(filename+" not found")
            print()


if __name__ == "__main__":

        aggregator = Aggregator()

        aggregator.queries = ["best", "qd-scores", "coverage"]
        if aggregator.algorithm == "cma-es":
            aggregator.queries = ["best"]

        results_per_query = aggregator.getResults()
        results_saved = aggregator.writeCSV(results_per_query)

        if results_saved:
            aggregator.removeOldFiles()
