from analysis import Analysis

analysis = Analysis()


objective = 6
generation = 1000
runs = 30
query = "extrema"
bias = 2
bins = 6
axis = 3

path = "./best"
filename = "temp.png"

parameters = [

    {"algorithm" : "ga",   "experiment" : "cropped-048-bias-0", "repertoire" : "bins-"+str(bins), "axis" : str(axis), "label" : "Green Bias"},
    {"algorithm" : "ga",   "experiment" : "cropped-048-bias-1", "repertoire" : "bins-"+str(bins), "axis" : str(axis), "label" : "Blue Bias"},
    {"algorithm" : "ga",   "experiment" : "cropped-048-bias-2", "repertoire" : "bins-"+str(bins), "axis" : str(axis), "label" : "Purple Bias"},
]


analysis.drawOneGenerationCombo(path, filename, query, objective, parameters, runs, generation)
