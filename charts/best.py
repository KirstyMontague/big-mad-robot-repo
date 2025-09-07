from analysis import Analysis

analyse = Analysis()

gp_algorithms = []
qdpy_algorithms = []


objective = 0
generation = 1000
runs = 30

# gp_algorithms.append(analyse.algorithms.info["foraging_baseline"])
# gp_algorithms.append(analyse.algorithms.info["foraging_qd1"])
# gp_algorithms.append(analyse.algorithms.info["foraging_qd8"])
# gp_algorithms.append(analyse.algorithms.info["foraging_qd64"])
# gp_algorithms.append(analyse.algorithms.info["foraging_mt1"])
# gp_algorithms.append(analyse.algorithms.info["foraging_mt8"])

gp_algorithms.append(analyse.algorithms.info["gp"])
gp_algorithms.append(analyse.algorithms.info["mtc"])
gp_algorithms.append(analyse.algorithms.info["mti"])

qdpy_algorithms.append(analyse.algorithms.info["qdpy"])

analyse.drawOneGeneration(analyse.queries.info["best"], analyse.objectives.index[objective], gp_algorithms, qdpy_algorithms, generation, runs)
analyse.drawOneGeneration(analyse.queries.info["qd-score"], analyse.objectives.index[objective], gp_algorithms, qdpy_algorithms, generation, runs)
analyse.drawOneGeneration(analyse.queries.info["coverage"], analyse.objectives.index[objective], gp_algorithms, qdpy_algorithms, generation, runs)

