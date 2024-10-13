

import pickle
import numpy

from deap import gp
from deap import tools
from deap import base
from deap import creator

from containers import *

import local

class QD():

    def __init__(self, params, utilities):

        self.params = params
        self.utilities = utilities

        def genEmpty():
            return []

        toolbox = base.Toolbox()

        pset = local.PrimitiveSetExtended("MAIN", 0)
        self.params.addNodes(pset)

        creator.create("Single_Objective_Fitness", base.Fitness, weights=(1.0,))
        creator.create("Single_Objective_Individual", gp.PrimitiveTree, fitness=creator.Single_Objective_Fitness, features=list)
        toolbox.register("expr_init", genEmpty)
        toolbox.register("Single_Objective_Individual", tools.initIterate, creator.Individual, toolbox.expr_init)
        toolbox.register("Single_Objective_Population", tools.initRepeat, list, toolbox.Single_Objective_Individual)

        self.qdpy_toolbox = toolbox

        self.grids = []

        for objective in self.params.indexes:

            fitness_domain = [(0.,1.0),] if self.params.description != "foraging" else [(0., numpy.inf)]
            features_domain = [(-40.0, 40.0), (-40.0, 40.0), (0.0, 1.0)] if self.params.description != "foraging" else [(-200.0, 200.0), (-200.0, 200.0), (0.0, 1.0)]

            self.grids.append(Grid(shape = [8,8,8],
                              max_items_per_bin = 1,
                              fitness_domain = fitness_domain,
                              features_domain = features_domain,
                              storage_type=list))

    def addPopulation(self, population):

        for i in range(self.params.features):

            pop = self.qdpy_toolbox.Single_Objective_Population(n=len(population))

            for j in range(len(population)):

                pop[j] = creator.Single_Objective_Individual(population[j])

                fitness = [population[j].fitness.values[i]]

                features = []
                features.append(population[j].fitness.values[-3])
                features.append(population[j].fitness.values[-2])
                features.append(population[j].fitness.values[-1])

                pop[j].fitness.values = tuple(fitness)
                pop[j].features = tuple(features)

            grid = self.grids[i]
            self.utilities.removeDuplicates(pop, grid)
            nb_updated = grid.update(pop, issue_warning = True)

    def getQDScores(self):

        qd_scores = []

        for i in range(self.params.features):

            score = 0.0
            for idx, inds in self.grids[i].solutions.items():
                if len(inds) == 0:
                    continue
                for ind in inds:
                    score += ind.fitness.values[0]

            shape = self.grids[i].shape
            score /= shape[0]*shape[1]*shape[2]

            qd_scores.append(score)

        return qd_scores

    def save(self):

        if not self.params.saveOutput:
            return

        for i in range(len(self.grids)):

            grid = self.grids[i]

            filename = "./test/"+self.params.description+"/"+str(self.params.deapSeed)+"/"
            filename += self.params.description+"-"+str(self.params.deapSeed)+"-"+self.params.objectives[self.params.indexes[i]]+".pkl"
            print(filename)

            with open(filename, "wb") as f:
                pickle.dump(grid, f)
