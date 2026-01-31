"""

Draw box plots for a range of generations for one algorithm

"""

from analysis import Analysis
analyse = Analysis()

def drawEvolution(experiment, algorithm, objective_name, repertoire, runs,  min_gen, max_gen, increment, x_axis_increment):

    analyse.drawEvolution(experiment,
                          analyse.algorithms.info[algorithm],
                          analyse.queries.info["best"],
                          objective_name,
                          repertoire,
                          runs,
                          min_gen,
                          max_gen,
                          increment,
                          x_axis_increment)

runs = 30
min_gen = 0
max_gen = 1000
increment = 10
x_axis_increment = 100

experiment = "arena-1"
algorithm = "qdpy"

objective = "density"
repertoire = None

if algorithm in ["gp", "mtc", "mti", "qdpy"]:
    drawEvolution(experiment, algorithm, objective, repertoire, runs, min_gen, max_gen, increment, x_axis_increment)






