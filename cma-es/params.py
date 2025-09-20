
class Params():

    def __init__(self):

        self.objectives = ["density", "nest", "food", "idensity", "inest", "ifood", "foraging"]

        self.objective_index = 0
        self.generations = 10
        self.saveOutput = False
        self.saveCSV = False

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
        self.cancelled = False
        self.num_threads = 8

        self.num_inputs = num_inputs
        self.num_hidden = num_hidden
        self.num_outputs = num_outputs
        self.ind_size = (num_inputs * num_hidden) + num_hidden + (num_hidden * num_outputs) + num_outputs

        self.objective = self.objectives[self.objective_index]

        self.csv = "./test/"+self.objective+"/results.csv"
