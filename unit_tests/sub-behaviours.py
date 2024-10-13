
import sys
sys.path.insert(0, '..')

from deap import gp
from deap import tools
from deap import base
from deap import creator

import local

from params import eaParams
from behaviours import Behaviours


def checkBehaviours():

    params = eaParams()
    behaviours = Behaviours(params, "../repertoires/sub-behaviours-mt8-1000gen.txt")


    pset = local.PrimitiveSetExtended("MAIN", 0)
    params.addNodes(pset)

    weights = [(1.0),(1.0),(1.0)]
    for i in range(params.features): weights.append(1.0)
    creator.create("Fitness", base.Fitness, weights=(weights))
    creator.create("Individual", gp.PrimitiveTree, fitness=creator.Fitness)

    toolbox = base.Toolbox()
    toolbox.register("expr_init", local.genFull, pset=pset, min_=1, max_=4)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr_init)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)


    expected = [113, 126, 100, 125, 89, 90, 75, 100]
    result = "passed"
    
    pop = toolbox.population(n=8)
    for i in range(8):
        index = str(i+1)
        pop[i] = creator.Individual.from_string("seqm3(seqm2(increaseDensity"+index+", reduceDensity"+index+"), seqm2(gotoFood"+index+", goAwayFromFood"+index+"), seqm2(gotoNest"+index+", goAwayFromNest"+index+")", pset)
        if behaviours.unpack(pop[i]) != expected[i]:
            result = "failed"

    print(result)


if __name__ == "__main__":
    checkBehaviours()
