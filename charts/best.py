from analysis import Analysis

analyse = Analysis()

objectives = ["density", "nest", "ifood"]

generation = 2000
features = 3
feature = 2
runs = 10

gp_algorithms = []
gp_algorithms.append(analyse.algorithms["baseline"])
gp_algorithms.append(analyse.algorithms["mt"])

qdpy_algorithms = []
qdpy_algorithms.append(analyse.algorithms["qdpy"])

analyse.drawBestOneGeneration(feature, objectives[feature], gp_algorithms, qdpy_algorithms, generation, features, runs)

