from analysis import Analysis

analysis = Analysis()

objective = 6
generation = 0
runs = 30

query = "best"

algorithms = ["gp"]
experiments = ["arena-1"]
repertoires = ["baseline"]

# algorithms = ["gp", "mtc", "mti", "qdpy"]
# experiments = ["arena-1", "arena-2"]
repertoires = ["baseline", "qd1", "qd8", "qd64"]

filename = "./"+query+"/no-labels/foraging/arenas2/arena1.png"

analysis.drawOneGeneration(filename, query, objective, algorithms, experiments, repertoires, runs, generation)
