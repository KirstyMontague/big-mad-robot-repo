from analysis import Analysis

analyse = Analysis()

objectives = ["foraging"]

generation = 500
features = 1
feature = 0
runs = 10

gp_algorithms = []
gp_algorithms.append(analyse.algorithms["foraging_old_derating_modular"])
gp_algorithms.append(analyse.algorithms["foraging_modular"])

qdpy_algorithms = []
# qdpy_algorithms.append(analyse.algorithms["qdpy"])

analyse.drawBestOneGeneration(feature, objectives[feature], gp_algorithms, qdpy_algorithms, generation, features, runs)

