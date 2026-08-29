"""

Draw box plots for a range of generations for one algorithm

"""

from analysis import Analysis
analyse = Analysis()

def drawEvolution(experiment, algorithm, query_name, objective_name, repertoire, csv_index, runs,  min_gen, max_gen, increment, x_axis_increment):

    analyse.drawEvolution(experiment,
                          analyse.algorithms.info[algorithm],
                          analyse.queries.info[query_name],
                          objective_name,
                          repertoire,
                          csv_index,
                          runs,
                          min_gen,
                          max_gen,
                          increment,
                          x_axis_increment)


runs = 30
min_gen = 0
max_gen = 1000
csv_index = 1000
increment = 10
x_axis_increment = 100

experiment = "arena-1"
algorithm = "qdpy"

query = "best"
objective = "density"
repertoire = "baseline"


if algorithm in ["gp", "mtc", "mti", "qdpy", "ga"]:
    drawEvolution(experiment, algorithm, query, objective, repertoire, csv_index, runs, min_gen, max_gen, increment, x_axis_increment)
else:
    print("Algorithm not recognised")






