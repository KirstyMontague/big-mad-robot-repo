
"""

Utility class for loading and working with repertoires

"""

class Repertoire():

    def __init__(self, params):

        self.params = params

        self.objective = self.params.objectives[0]
        self.src_bins = self.params.nb_bins
        self.dst_bins = self.params.nb_bins
        self.domain = self.params.features_domain
        self.generations = self.params.generations

        self.algorithms = []
        self.experiments = []

        self.runs = 0
        self.seeds = []

        self.input = "separate"
        self.mode = "append"
        self.output = "combined"

        self.save = False
        self.save_combined = False
        self.pause = 10.0
        self.show = False

        self.cancelled = False

    def setUp(self, utilities, redundancy):
        self.utilities = utilities
        self.redundancy = redundancy

    def configure(self):
        permitted = ["project", "algorithms", "experiments", "domain", "src_domain", "dst_domain", "src_bins", "dst_bins", "repertoire_size",
                     "objective", "seeds", "runs", "generations", "bias", "penalty", "baseline",
                     "input", "save", "save_combined", "pause", "mode", "output", "show",]
        with open(self.params.shared_path+"/repertoire.txt", 'r') as f:
            for line in f:
                data = line.split()
                if len(data) > 0:
                    if data[0] == "#":
                        continue
                    if data[0] in permitted:
                        print(line.strip('\t\n\r'))
                        self.update(data)
                    else:
                        print("\nconfig entry not recognised: "+data[0]+"\n")
                        self.cancelled = True

    def update(self, data):

        if data[0] == "input":
            types = ["separate", "combined", "accumulate", "postpro"]
            if data[1] in types:
                self.input = data[1]
            else:
                print("\nInput type not recognised\n")
                self.cancelled = True

        if data[0] == "output":
            types = ["combined", "qd_score_csv", "extrema_csv", "population"]
            if data[1] in types:
                self.output = data[1]
            else:
                print("\nOutput not recognised\n")
                self.cancelled = True

        if data[0] == "mode":
            types = ["write", "append"]
            if data[1] in types:
                self.mode = data[1]
            else:
                print("\nMode not recognised\n")
                self.cancelled = True

        if data[0] == "algorithms" and len(data) > 1:
            self.algorithms = []
            algorithms = ["qdpy", "mtc", "mti", "gp", "ga"]
            for algorithm in data[1:]:
                if algorithm in algorithms:
                    self.algorithms.append(algorithm)
                else:
                    print("\nAlgorithm not recognised: "+data[1]+"\n")
                    self.cancelled = True

        if data[0] == "experiments" and len(data) > 1:
            self.experiments = []
            for experiment in data[1:]:
                self.experiments.append(experiment)

        if data[0] == "objective":
            self.objective = int(data[1])

        if data[0] == "repertoire_size":
            size = int(data[1])
            self.params.repertoire_size = size
            self.src_bins = [size, size, size]
            self.dst_bins = [size, size, size]

        if data[0] == "src_bins" and len(data) > 1:
            self.src_bins = []
            for b in data[1:]:
                self.src_bins.append(int(b))
            self.params.src_bins = self.src_bins

        if data[0] == "dst_bins" and len(data) > 1:
            self.dst_bins = []
            for b in data[1:]:
                self.dst_bins.append(int(b))

        if data[0] == "domain" and len(data) > 1:
            self.domain = []
            for i in range(1, len(data), 2):
                self.domain.append((float(data[i]), float(data[i+1])))
            self.src_domain = self.domain
            self.dst_domain = self.domain

        if data[0] == "src_domain" and len(data) > 1:
            self.src_domain = []
            for i in range(1, len(data), 2):
                self.src_domain.append((float(data[i]), float(data[i+1])))

        if data[0] == "dst_domain" and len(data) > 1:
            self.dst_domain = []
            for i in range(1, len(data), 2):
                self.dst_domain.append((float(data[i]), float(data[i+1])))
            self.domain = self.dst_domain

        if data[0] == "seeds" and len(data) > 1:
            self.seeds = []
            for seed in data[1:]:
                self.seeds.append(int(seed))

        if data[0] == "project": self.params.project = data[1]
        if data[0] == "baseline": self.params.baseline = data[1]
        if data[0] == "generations": self.generations = int(data[1])
        if data[0] == "runs": self.runs = int(data[1])
        if data[0] == "bias": self.params.bias = int(data[1])
        if data[0] == "penalty": self.params.penalty = float(data[1])
        if data[0] == "save": self.save = True if data[1] == "True" else False
        if data[0] == "save_combined": self.save_combined = True if data[1] == "True" else False
        if data[0] == "show": self.show = True if data[1] == "True" else False
        if data[0] == "pause": self.pause = float(data[1])

    def seedsList(self):
        seeds = []
        if self.runs > 0:
            for i in range(1, self.runs + 1):
                seeds.append(i)
        else:
            seeds = self.seeds
        return seeds

    def isSmallRepertoire(self):
        # legacy = results-without-ifgotfood
        # objectives_in_fitness_function = enucc arena-1-gp etc
        return self.params.project in ["legacy", "objectives_in_fitness_function"]

    def getQualityArray(self, container):
        if self.params.usingNewGrid:
            return container.quality_array()
        else:
            return container.quality_array[..., 0]

    def getAlgorithmDir(self, algorithm):
        if algorithm == "qdpy": return "qdpy"
        elif algorithm == "ga": return "ga"
        else: return "gp"

    def getOutputDir(self, algorithm_type, experiment, description):
        return self.params.output_path+"/"+algorithm_type+self.params.directoryPath(experiment, description)

    def getData(self, seeds, algorithm, experiment, objective):

        objective_name = self.params.objectives[objective]

        container = self.utilities.createContainer(self.dst_bins, self.domain, 1)
        if self.params.usingNewGrid:
            container.discardOutOfBounds(True)

        algorithm_type = self.getAlgorithmDir(algorithm)
        description = self.utilities.getExperimentDescription(objective, algorithm)

        output_dir = self.params.output_path+"/"+algorithm_type+self.params.directoryPath(experiment, description)

        if self.params.project == "legacy":
            output_file = objective_name+"-with-30-seeds.txt"
        elif self.params.project == "objectives_in_fitness_function":
            output_file = objective_name+"-with-all-seeds.txt"
        elif self.params.project == "straight_to_foraging" and algorithm == "qdpy":
            output_file = objective_name+"-with-all-seeds-small-bins.txt"
        elif self.params.project == "heterogeneous_genetic_algorithm":
            output_file = objective_name+"-with-all-seeds-"+str(self.dst_bins[0])+"-bins.txt"
        else:
            output_file = objective_name+"-"+str(self.src_bins[0])+"-bins.txt"

        if self.params.project == "legacy":

            input_dir = self.params.legacy_path+"/"+algorithm_type+self.params.directoryPath(experiment, description)

            if self.input == "separate":
                for seed in seeds:
                    filename = self.utilities.getLegacyCheckpointFilename(input_dir, algorithm, seed, objective, self.generations)
                    print("Seed file "+filename)
                    self.utilities.getLegacyCheckpointContainer(container, algorithm, filename, objective)
                if self.save_combined:
                    print("Output file "+output_dir+"/"+output_file)
                    self.utilities.saveContainer(container, output_dir, output_dir+"/"+output_file)

            elif self.input == "combined":
                filename = input_dir+"/"+output_file
                print("Combined file "+filename)
                self.readContainer(container, filename)

            else:
                print("Input type not supported")
                return

        else:

            input_dir = self.params.input_path+"/"+algorithm_type+self.params.directoryPath(experiment, description)

            if self.input == "accumulate":
                cumulative_file = output_dir+"/"+output_file
                print("Cumulative file "+cumulative_file)
                self.readContainer(container, cumulative_file)
                if self.pause > 0.0:
                    print("pausing for "+str(self.pause)+"s\n")
                    time.sleep(self.pause)

            if self.input == "combined":
                filename = input_dir+"/"+output_file
                print("Combined file "+filename)
                self.readContainer(container, filename)

            elif self.input == "postpro":
                filename = output_dir+"/"+output_file
                print("Postpro file "+filename)
                self.readContainer(container, filename)

            else:
                for seed in seeds:
                    filename = input_dir+"/"+str(seed)+"/checkpoint-"
                    if algorithm_type == "qdpy":
                        if self.params.project == "straight_to_foraging":
                            filename += objective_name+"-"+str(seed)+"-"+str(self.generations)+"-"+objective_name+".txt"
                        else:
                            filename += self.utilities.getIfoodCompacted(objective_name)+"-"+str(seed)+"-"+str(self.generations)+".txt"
                    else:
                        filename += description+"-"+str(seed)+"-"+str(self.generations)+"-"+objective_name+".txt"
                    print("Seed file "+filename)
                    self.readContainer(container, filename)
                    if self.pause > 0.0:
                        print("pausing for "+str(self.pause)+"s\n")
                        time.sleep(self.pause)

            if self.save_combined:
                print("Writing to "+output_dir+"/"+output_file)
                self.utilities.saveContainer(container, output_dir, output_dir+"/"+output_file)
            else:
                print("Output file "+output_dir+"/"+output_file)

        return container

    def readContainer(self, container, filename):
        self.utilities.updateContainerFromString(self.redundancy, self.utilities.toolbox, container, filename, 2000, 0, 0)

