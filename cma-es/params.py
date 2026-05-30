import os
from pathlib import Path

class Params():

    def __init__(self):

        self.objectives = ["density", "nest", "food", "idensity", "inest", "ifood", "foraging"]

        self.experiment = "vanilla"

        self.objective_index = 0
        self.generations = 0

        self.useArchive = False
        self.saveOutput = False
        self.saveCSV = False
        self.saveBest = False

        self.population_size = 25

        self.precision = 0
        self.sigma = 1.0

        num_inputs = 9
        num_hidden = 5
        num_outputs = 1

        self.sqrt_robots = 3
        self.arena_params = [0.5, 0.7]
        self.arena_iterations = 5

        self.seed = 0
        self.stop = False
        self.num_threads = 8
        self.output_to_file = True
        self.output_interval = 10

        self.num_inputs = num_inputs
        self.num_hidden = num_hidden
        self.num_outputs = num_outputs
        self.individualSize()

        self.objective = self.objectives[self.objective_index]

        with open("../path.txt", "r") as f:
            for line in f:
                data = line.split(":")
                if data[0] == "path": path = data[1][0:-1]

        with open(path, "r") as f:
            for line in f:
                data = line.split(":")
                if data[0] == "local": self.local_path = data[1][0:-1]
                if data[0] == "shared": self.shared_path = data[1][0:-1]
                if data[0] == "input": self.input_path = data[1][0:-1]

        if "repro" in self.shared_path:
            self.saveOutput = False
            self.saveCSV = False
            self.saveBest = False

        self.cancelled = "repro" in self.shared_path

    def individualSize(self):
        self.ind_size = self.num_inputs * self.num_hidden
        self.ind_size += self.num_hidden
        self.ind_size += self.num_hidden * self.num_outputs
        self.ind_size += self.num_outputs

    def path(self):
        return self.shared_path+"/cma-es/"+self.experiment+"/"+self.objective+"/"+str(self.seed)

    def csvFilename(self):
        return self.path()+"/best"+str(self.generations)+"-"+str(self.seed)+".csv"

    def bestFilename(self):
        return self.path()+"/best.txt"

    def paramsFilename(self):
        return self.path()+"/params.txt"

    def console(self, text):
        if self.output_to_file:
            with open(self.shared_path+"/cma-es/console"+str(self.seed)+".txt", "a") as f:
                f.write(text+"\n")
        else:
            print(text)

    def makePaths(self):

        if self.experiment == "":
            self.experiment = "vanilla"

        self.console("\nPath: "+self.path())

        self.local_path += "/"+str(self.seed)
        Path(self.local_path+"/").mkdir(parents=False, exist_ok=True)

    def deleteTempFiles(self):

        if os.path.exists(self.local_path+"/runtime.txt"):
            os.remove(self.local_path+"/runtime.txt")
        if os.path.exists(self.local_path+"/current.txt"):
            os.remove(self.local_path+"/current.txt")
        os.remove(self.local_path+"/configuration.txt")

        if len(os.listdir(self.local_path)) == 0:
            os.rmdir(self.local_path)

    def configure(self):
        with open(self.shared_path+"/config.txt", 'r') as f:
            for line in f:
                data = line.split()
                if len(data) > 0:
                    self.update(data)
                    self.console(line[0:-1])
        self.runtime()

    def runtime(self):
        restricted = ["objective", "num_threads", "num_hidden", "useArchive"]
        with open(self.shared_path+"/runtime.txt", 'r') as f:
            for line in f:
                data = line.split()
                if len(data) > 0:
                    if data[0] not in restricted:
                        self.update(data)
                        self.console(line[0:-1])
                    else:
                        self.console(data[0] +" not supported at runtime")
        if os.path.exists(self.local_path+"/runtime.txt"):
            with open(self.local_path+"/runtime.txt", 'r') as f:
                for line in f:
                    data = line.split()
                    if len(data) > 0:
                        if data[0] not in restricted:
                            self.update(data)
                            self.console(line[0:-1])

    def update(self, data):
        if data[0] == "experiment" and len(data) > 1:
            self.experiment = data[1]
        if data[0] == "objective":
            self.objective_index = int(data[1])
            self.objective = self.objectives[self.objective_index]
        if data[0] == "generations": self.generations = int(data[1])
        if data[0] == "useArchive": self.useArchive = True if data[1] == "True" else False
        if data[0] == "saveOutput": self.saveOutput = True if data[1] == "True" else False
        if data[0] == "saveCSV": self.saveCSV = True if data[1] == "True" else False
        if data[0] == "saveBest": self.saveBest = True if data[1] == "True" else False
        if data[0] == "num_threads": self.num_threads = int(data[1])
        if data[0] == "output_to_file": self.output_to_file = False if data[1] == "False" else True
        if data[0] == "output_interval": self.output_interval = int(data[1])
        if data[0] == "num_hidden":
            self.num_hidden = int(data[1])
            self.individualSize()
        if data[0] == "stop":
            self.generations = 0
            self.saveCSV = False
            self.stop = True
        if data[0] == "cancel":
            self.generations = 0
            self.saveOutput = False
            self.saveCSV = False
            self.saveBest = False
            self.stop = True
