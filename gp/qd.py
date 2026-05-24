

import pickle
import numpy

from deap import gp
from deap import tools
from deap import base
from deap import creator

# from containers import *
from grid import Grid

import local

class QD():

    def __init__(self, params, utilities):

        self.params = params
        self.utilities = utilities

        if not self.utilities.checkContainerSize():
            return

        def genEmpty():
            return []

        toolbox = base.Toolbox()

        pset = local.PrimitiveSetExtended("MAIN", 0)
        self.params.addNodes(pset)

        creator.create("Single_Objective_Fitness", base.Fitness, weights=(1.0,))
        creator.create("Single_Objective_Individual", gp.PrimitiveTree, fitness=creator.Single_Objective_Fitness, features=list)
        toolbox.register("expr_init", genEmpty)
        toolbox.register("Single_Objective_Individual", tools.initIterate, creator.IndividualGP, toolbox.expr_init)
        toolbox.register("Single_Objective_Population", tools.initRepeat, list, toolbox.Single_Objective_Individual)

        self.qdpy_toolbox = toolbox

        self.grids = []

        for objective in self.params.indexes:

            self.grids.append(self.utilities.createContainer(self.params.nb_bins, self.params.features_domain, 1))

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
            if self.params.usingNewGrid:
                grid.update(pop)
            else:
                try:
                    grid.update(pop, issue_warning = True)
                except UserWarning as error:
                    raise ValueError(error)

    def getQDScores(self):

        qd_scores = []

        for i in range(self.params.features):
            qd_scores.append(str("%.12f" % self.utilities.getQDScore(self.grids[i])))

        return qd_scores

    def save(self, generation):

        if not self.params.saveOutput:
            return

        for i in range(len(self.grids)):

            grid = self.grids[i]

            filename = self.params.path()
            filename += "grid-"+self.params.description+"-"+str(self.params.deapSeed)+"-"
            filename += self.params.objectives[self.params.indexes[i]]+"-"+str(generation)+".pkl"

            with open(filename, "wb") as f:
                pickle.dump(grid, f)
