
class Params():

    def __init__(self):

        self.objectives = ["density", "nest", "food", "idensity", "inest", "ifood", "foraging"]

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

        self.num_inputs = num_inputs
        self.num_hidden = num_hidden
        self.num_outputs = num_outputs
        self.individualSize()

        self.objective = self.objectives[self.objective_index]

        with open("../path.txt", "r") as f:
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

    def csvFilename(self):
        return self.shared_path+"/cma-es/"+self.objective+"/best"+str(self.generations)+"-"+str(self.seed)+".csv"

    def bestFilename(self):
        return self.shared_path+"/cma-es/"+self.objective+"/best-"+str(self.seed)+".txt"
