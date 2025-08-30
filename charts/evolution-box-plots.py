"""

Draw box plots for a range of generations for one algorithm

"""

from analysis import Analysis
analyse = Analysis()

def drawEvolution(algorithm, objective_name,  runs,  min_gen, max_gen, increment, x_axis_increment):

    analyse.drawEvolution(analyse.algorithms.info[algorithm],
                          analyse.queries.info["best"],
                          objective_name,
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

drawEvolution("gp", "density", runs, min_gen, max_gen, increment, x_axis_increment)






