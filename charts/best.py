from analysis import Analysis

analysis = Analysis()

objective = 6
generation = 0
runs = 30

query = "best"

algorithms = ["mtc", "mti", "qdpy"]
experiments = ["arena-1", "arena-1-combo"]
repertoires = ["baseline", "mtc64", "mti64", "qd64"]

algorithms = ["gp"]
# experiments = ["arena-4"]
repertoires = ["qd1"]

rep = "qd"
arena = "arena-1"

something_else = [

    {"algorithm" : "gp", "experiment" : arena, "repertoire" : "baseline"},
    {"algorithm" : "gp", "experiment" : arena, "repertoire" : rep+"1"},
    {"algorithm" : "gp", "experiment" : arena+"-combo", "repertoire" : rep+"1"},
    {"algorithm" : "gp", "experiment" : arena, "repertoire" : rep+"8"},
    {"algorithm" : "gp", "experiment" : arena+"-combo", "repertoire" : rep+"8"},
    {"algorithm" : "gp", "experiment" : arena, "repertoire" : rep+"64"},
    {"algorithm" : "gp", "experiment" : arena+"-combo", "repertoire" : rep+"64"},
]

filename = "./"+query+"/no-labels/foraging/temp.png"

# analysis.drawOneGeneration(filename, query, objective, algorithms, experiments, repertoires, runs, generation)
analysis.drawOneGenerationCombo2(filename, query, objective, something_else, runs, generation)
