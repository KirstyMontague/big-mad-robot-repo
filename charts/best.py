from analysis import Analysis

analyse = Analysis()

objectives = ["density", "nest", "food", "idensity", "inest", "ifood", "foraging"]
features = 3
feature = 0
mtc_index = 0
mti_index = 0
generation = 1000

# objectives = ["foraging"]
# features = 1
# feature = 0
# generation = 1000

runs = 10

gp_algorithms = []

# gp_algorithms.append(analyse.algorithms["foraging_baseline"])
# gp_algorithms.append(analyse.algorithms["foraging_qd1"])
# gp_algorithms.append(analyse.algorithms["foraging_mt1"])
# gp_algorithms.append(analyse.algorithms["foraging_qd8"])
# gp_algorithms.append(analyse.algorithms["foraging_mt8"])

gp_algorithms.append(analyse.algorithms["gp"])
gp_algorithms.append(analyse.algorithms["mti"])
gp_algorithms.append(analyse.algorithms["mtc"])

qdpy_algorithms = []
qdpy_algorithms.append(analyse.algorithms["qdpy"])

analyse.drawBestOneGeneration(feature, objectives[feature], gp_algorithms, qdpy_algorithms, generation, features, runs, mtc_index, mti_index)

