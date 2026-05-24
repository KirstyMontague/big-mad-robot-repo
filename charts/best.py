from analysis import Analysis

analysis = Analysis()

project = "straight_to_foraging"
objective = 6
generation = 0
runs = 30

query = "best"

algorithms = ["gp", "mtc", "mti", "qdpy"]
experiments = ["arena-1", "arena-1-combo"]
repertoires = ["baseline", "mtc64", "mti64", "qd64"]

algorithms = ["qdpy"]
experiments = ["heterogeneous"]
# repertoires = ["baseline"]

filename = "./"+query+"/"+project+"/"
if len(algorithms) == 1: filename += algorithms[0]+"-"
if len(experiments) == 1: filename += experiments[0]+"-"
if len(repertoires) == 1: filename += repertoires[0]+"-"
filename = filename[:-1]+".png"

analysis.drawOneGeneration(filename, query, objective, algorithms, experiments, repertoires, runs, generation)


rep = "qd"
arena = "arena-1"

combinations = [

    {"algorithm" : "gp", "experiment" : arena, "repertoire" : "baseline"},
    {"algorithm" : "gp", "experiment" : arena, "repertoire" : rep+"1"},
    {"algorithm" : "gp", "experiment" : arena+"-combo", "repertoire" : rep+"1"},
    {"algorithm" : "gp", "experiment" : arena, "repertoire" : rep+"8"},
    {"algorithm" : "gp", "experiment" : arena+"-combo", "repertoire" : rep+"8"},
    {"algorithm" : "gp", "experiment" : arena, "repertoire" : rep+"64"},
    {"algorithm" : "gp", "experiment" : arena+"-combo", "repertoire" : rep+"64"},
]

filename = "./"+query+"/no-labels/foraging/temp.png"

# analysis.drawOneGenerationCombo2(filename, query, objective, combinations, runs, generation)
