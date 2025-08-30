from analysis import Analysis

analyse = Analysis()

gp_algorithms = []
qdpy_algorithms = []

def getMtcIndex(objective):
    if objective in [0, 2]: mtc_index = 0
    if objective in [1, 3]: mtc_index = 1
    if objective in [4, 5]: mtc_index = 2
    if objective == 6: mtc_index = -1
    return mtc_index

def getMtiIndex(objective):
    if objective in [0, 3]: mti_index = 0
    if objective in [1, 4]: mti_index = 1
    if objective in [2, 5]: mti_index = 2
    if objective == 6: mti_index = -1
    return mti_index


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

analyse.drawOneGeneration(analyse.queries.info["best"], objective, analyse.objectives.index[objective], gp_algorithms, qdpy_algorithms, generation, runs, getMtcIndex(objective), getMtiIndex(objective))
analyse.drawOneGeneration(analyse.queries.info["qd-score"], objective, analyse.objectives.index[objective], gp_algorithms, qdpy_algorithms, generation, runs, getMtcIndex(objective), getMtiIndex(objective))
analyse.drawOneGeneration(analyse.queries.info["coverage"], objective, analyse.objectives.index[objective], gp_algorithms, qdpy_algorithms, generation, runs, getMtcIndex(objective), getMtiIndex(objective))

