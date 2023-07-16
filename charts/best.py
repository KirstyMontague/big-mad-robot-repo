from analysis import Analysis

analyse = Analysis()


generation = 2000
features = 1
objective = "food"

gp_algorithms = []
# gp_algorithms.append(analyse.algorithms["baseline"])
gp_algorithms.append(analyse.algorithms["mt"])

qdpy_algorithms = []
qdpy_algorithms.append(analyse.algorithms["qdpy"])

analyse.drawBestOneGeneration(objective, gp_algorithms, qdpy_algorithms, generation, features)

