import matplotlib.pyplot as plt
import statistics

from analysis import Analysis
analyse = Analysis()


y = {
    "density" : {
        "best" : [0.5,0.61],
        "qd-score" : [0.0,0.35],
        "coverage" : [0.0,350.0],
    },
    "nest" : {
        "best" : [0.6,0.9],
        "qd-score" : [0.0,0.45],
        "coverage" : [0.0,0.65],
    },
    "food" : {
        "best" : [0.75,0.88],
        "qd-score" : [0.0,0.5],
        "coverage" : [0.0,0.65],
    },
    "idensity" : {
        "best" : [0.5,0.55],
        "qd-score" : [0.0,0.35],
        "coverage" : [0.0,0.65],
    },
    "inest" : {
        "best" : [0.6,0.9],
        "qd-score" : [0.0,0.45],
        "coverage" : [0.0,0.65],
    },
    "ifood" : {
        "best" : [0.5,0.75],
        "qd-score" : [0.0,0.4],
        "coverage" : [0.0,0.65],
    },
    "foraging" : {
        # heterogeneous GA
        "best"     : [0.0,4.0],
        # heterogeneous baseline 2000 gen
        "best"     : [0.0,3.0],
        "qd-scores" : [0.0,0.015],
        "avg-quality" : [0.0,1.5],
        "coverage" : [0.0,15000],
        # heterogeneous baseline 1000 gen
        "best"     : [0.0,2.5],
        "qd-scores" : [0.0,0.010],
        "avg-quality" : [0.0,1.2],
        "coverage" : [0.0,10000],
    },
}


def drawLineGraph(experiment, objective, algorithm, repertoire, query, generations, csv, max_bins, runs):
    title = analyse.objectives.info[objective]["description"]+" ("+algorithm.upper()+")"
    analyse.drawLineGraph(title,
                          experiment,
                          objective,
                          algorithm,
                          repertoire,
                          query,
                          generations,
                          csv,
                          max_bins,
                          y[objective][query],
                          runs)

experiment = "heterogeneous"
algorithm = "qdpy"
query = "avg-quality"

objective = "foraging"
repertoire = "baseline"
generations = 1000
csv = 1000
max_bins = 100*100*100

runs = 30

if algorithm in ["gp", "mtc", "mti", "qdpy", "ga"]:
    drawLineGraph(experiment, objective, algorithm, repertoire, query, generations, csv, max_bins, runs)
else:
    print("Algorithm not recognised")
