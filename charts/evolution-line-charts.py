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
        "best" : [0.0,1.0],
    },
}


def drawLineGraph(experiment, objective, algorithm, repertoire, query, generations, max_bins):
    title = analyse.objectives.info[objective]["description"]+" ("+algorithm.upper()+")"
    analyse.drawLineGraph(title,
                          experiment,
                          objective,
                          algorithm,
                          repertoire,
                          query,
                          generations,
                          max_bins,
                          y[objective][query])

experiment = "qd-tests-arena-1"
algorithm = "qdpy"
query = "coverage"

objective = "density"
repertoire = "mtc1"
generations = 1000
max_bins = 8000

if algorithm in ["gp", "mtc", "mti", "qdpy"]:
    drawLineGraph(experiment, objective, algorithm, repertoire, query, generations, max_bins)
