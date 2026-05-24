
from datetime import datetime
import numpy
import pickle
import random
import subprocess
import threading
import time

from deap import gp
from deap import tools
from deap import base
from deap import creator

import local

# from containers import *
from grid import Grid

# === heatmap =======

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt

from qdpy.plots import *

import scipy

# ====================

class Utilities():
    
    sequenceNodes = ["seqm2", "seqm3", "seqm4"]
    fallbackNodes = ["selm2", "selm3", "selm4"]
    probabilityNodes = ["probm2", "probm3", "probm4"]
    conditionNodes = ["ifNestToLeft", "ifNestToRight", "ifFoodToLeft", "ifFoodToRight", "ifGotFood", "ifOnFood", "ifInNest", "ifRobotToRight", "ifRobotToLeft"]
    compositeNodes = ["ifgevar", "ifltvar", "ifgecon", "ifltcon", "set"]
    decoratorNodes = ["successd", "failured", "repeat"]
    actionNodes = ["f", "fr", "fl", "r", "rr", "rl", "stop"]
    actuationNodes = ["f", "fr", "fl", "r", "rr", "rl", "stop"]
    successNodes = ["successl", "successd", "f", "fr", "fl", "r", "rr", "rl", "stop"]
    failureNodes = ["failurel", "failured"]
    
    def __init__(self, params, behaviours = None):
        self.params = params
        self.behaviours = behaviours
        self.primitivetree = gp.PrimitiveTree([])

    def setupToolboxGP(self, tournament):

        if tournament == None:
            def tournament():
                return []

        toolbox = base.Toolbox()

        self.pset = local.PrimitiveSetExtended("MAIN", 0)
        self.params.addNodes(self.pset)

        weights = [] if self.params.is_qdpy else [(1.0),(1.0),(1.0)]
        for i in range(self.params.features): weights.append(1.0)

        creator.create("FitnessGP", base.Fitness, weights=(weights))
        creator.create("IndividualGP", gp.PrimitiveTree, fitness=creator.FitnessGP)

        toolbox.register("expr_init", local.genFull, pset=self.pset, min_=1, max_=4)

        toolbox.register("individual", tools.initIterate, creator.IndividualGP, toolbox.expr_init)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        toolbox.register("evaluate", self.evaluateRobot, thread_index=1)
        toolbox.register("select", tournament, tournsize=self.params.tournamentSize)

        self.evaluation_functions = []
        for i in range(1, self.params.num_threads + 1):
            toolbox.register("evaluate"+str(i), self.evaluateRobot, thread_index=i)
            self.evaluation_functions.append(self.makeEvaluationFunction("evaluate"+str(i)))

        toolbox.register("mate", gp.cxOnePoint)
        toolbox.register("expr_mut", local.genFull, min_=0, max_=2)
        toolbox.register("mutSubtreeReplace", local.mutUniform, expr=toolbox.expr_mut, pset=self.pset)
        toolbox.register("mutSubtreeShrink", local.mutShrink)
        toolbox.register("mutNodeReplace", local.mutNodeReplacement, pset=self.pset)

        # for creating trimmed population
        toolbox.register("expr_empty", local.genEmpty, pset=self.pset, min_=1, max_=4)
        toolbox.register("empty_individual", tools.initIterate, creator.IndividualGP, toolbox.expr_empty)
        toolbox.register("empty_population", tools.initRepeat, list, toolbox.empty_individual)

        return toolbox

    def setupToolboxGA(self, repertoire, mutation_operator, flat_indexes, grid_indexes):

        self.repertoire = repertoire

        creator.create("FitnessGA", base.Fitness, weights=(1.0,))
        creator.create("IndividualGA", list, fitness=creator.FitnessGA)

        toolbox = base.Toolbox()

        def randomIndex(): return random.choice(grid_indexes)
        toolbox.register("attr_index", randomIndex)
        toolbox.register("individual", tools.initRepeat, creator.IndividualGA, toolbox.attr_index, 9)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        toolbox.register("select", tools.selTournament, tournsize=3)
        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register("mutate", mutation_operator, flat_indexes=flat_indexes, grid_indexes=grid_indexes, indpb=0.05)
        toolbox.register("evaluate", self.evaluateSwarm, thread_index=1)

        self.evaluation_functions = []
        for i in range(1,9):
            toolbox.register("evaluate"+str(i), self.evaluateSwarm, thread_index=i)
            self.evaluation_functions.append(self.makeEvaluationFunction("evaluate"+str(i)))

        def zero(): return [0,0,0]
        toolbox.register("attr_empty", zero)
        toolbox.register("empty_individual", tools.initRepeat, creator.IndividualGA, toolbox.attr_empty, 9)
        toolbox.register("empty_population", tools.initRepeat, list, toolbox.empty_individual)

        return toolbox

    def evaluateRobot(self, individual, thread_index):
        
        # print ("")
        # print (individual)
        
        # save chromosome to file
        with open(self.params.local_path+'/chromosome'+str(thread_index)+'.txt', 'w') as f:
            f.write(str(individual))
        
        totals = []
        # qdpy optimisation
        # for i in range(self.params.features):
        for i in range(self.params.features + 3):
            # end qdpy
            totals.append(0.0)
        
        fitness = []
        features = []
        robots = {}
        seed = 0
        error = False

        num_data = self.params.max_objectives

        for i in self.params.arena_params:
            
            # get maximum food available with the current gap between the nest and food
            # maxFood = self.calculateMaxFood(i)
            
            # write seed and offset to file
            seed += 1
            with open(self.params.local_path+'/seed'+str(thread_index)+'.txt', 'w') as f:
                f.write(str(seed))
                f.write("\n")
                f.write(str(self.params.arenaOffset(i)))

            # run argos
            subprocess.call(["/bin/bash", "../evaluate", str(thread_index), self.params.local_path, "./"])

            # result from file
            with open(self.params.local_path+"/result"+str(thread_index)+".txt", "r") as f:

                for line in f:
                    first = line[0:line.find(" ")]
                    if first == "error":
                        error = True
                        self.raiseError("ARGoS "+line.strip('\t\n\r'))
                        break
                    if error:
                        continue
                    if first == "result":
                        lines = line.split()
                        robotId = int(float(lines[1]))
                        robots[robotId] = []
                        for j in range(num_data):
                            for k in range(self.params.iterations):
                                if j in self.params.indexes:
                                    index = (j * self.params.iterations) + k + 2
                                    robots[robotId].append(float(lines[index]))
                        for j in range(3):
                            for k in range(self.params.iterations):
                                index = (j * self.params.iterations) + (num_data * self.params.iterations) + k + 2
                                robots[robotId].append(float(lines[index]))

            # get scores for each robot and add to cumulative total
            for k in range(self.params.features + 3):
                totals[k] += self.collectFitnessScore(robots, k)

            # increment counter and pause to free up CPU
            time.sleep(self.params.trialSleep)

        # divide to get average per seed and arena configuration then apply derating factor
        deratingFactor = 1.0
        features = []

        for i in range(self.params.features):
            fitness.append(self.getAvgAndDerate(totals[i], individual, deratingFactor))
        for i in range(self.params.characteristics):
            features.append(self.getAvgAndDerate(totals[i + self.params.features], individual, deratingFactor))

        try:
            os.remove(self.params.local_path+"/seed"+str(thread_index)+".txt")
            os.remove(self.params.local_path+"/chromosome"+str(thread_index)+".txt")
            os.remove(self.params.local_path+"/result"+str(thread_index)+".txt")
        except Exception as e:
            self.raiseError(str(e))

        # pause to free up CPU
        time.sleep(self.params.evalSleep)

        if self.params.is_qdpy:
            return (fitness, features)
        else:
            return (fitness + features)

    def evaluateSwarm(self, swarm, thread_index):

        # print ("")
        # print (swarm)

        chromosomes = ""
        for ind in swarm:
            ig = tuple(ind)
            ind = self.repertoire.solutions[ig][0]
            chromosomes += str(ind)+"\n"

        # save chromosomes to file
        with open(self.params.local_path+'/chromosome'+str(thread_index)+'.txt', 'w') as f:
            f.write(str(chromosomes[0:-1]))

        totals = []
        for i in range(self.params.features + 3):
            totals.append(0.0)

        fitness = []
        features = []
        robots = {}
        seed = 0
        error = False

        num_data = self.params.max_objectives

        for i in self.params.arena_params:

            # write seed and offset to file
            seed += 1
            with open(self.params.local_path+'/seed'+str(thread_index)+'.txt', 'w') as f:
                f.write(str(seed))
                f.write("\n")
                f.write(str(self.params.arenaOffset(i)))

            # run argos
            subprocess.call(["/bin/bash", "../evaluate", str(thread_index), self.params.local_path, "./"])

            # result from file
            with open(self.params.local_path+"/result"+str(thread_index)+".txt", "r") as f:

                for line in f:
                    first = line[0:line.find(" ")]
                    if first == "error":
                        error = True
                        self.raiseError("ARGoS "+line.strip('\t\n\r'))
                        break
                    if error:
                        continue
                    if first == "result":
                        lines = line.split()
                        robotId = int(float(lines[1]))
                        robots[robotId] = []
                        for j in range(num_data):
                            for k in range(self.params.iterations):
                                if j in self.params.indexes:
                                    index = (j * self.params.iterations) + k + 2
                                    robots[robotId].append(float(lines[index]))
                        for j in range(3):
                            for k in range(self.params.iterations):
                                index = (j * self.params.iterations) + (num_data * self.params.iterations) + k + 2
                                robots[robotId].append(float(lines[index]))

            # get scores for each robot and add to cumulative total
            for k in range(self.params.features + 3):
                totals[k] += self.collectFitnessScore(robots, k)

            # increment counter and pause to free up CPU
            time.sleep(self.params.trialSleep)

        # divide to get average per seed and arena configuration then apply derating factor
        deratingFactor = 1.0
        features = []

        for i in range(self.params.features):
            fitness.append(self.getAvgAndDerate(totals[i], swarm, deratingFactor))
        for i in range(self.params.characteristics):
            features.append(self.getAvgAndDerate(totals[i + self.params.features], swarm, deratingFactor))

        try:
            os.remove(self.params.local_path+"/seed"+str(thread_index)+".txt")
            os.remove(self.params.local_path+"/chromosome"+str(thread_index)+".txt")
            os.remove(self.params.local_path+"/result"+str(thread_index)+".txt")
        except Exception as e:
            self.raiseError(str(e))

        # pause to free up CPU
        time.sleep(self.params.evalSleep)

        if self.params.is_qdpy:
            return (fitness, features)
        else:
            return (fitness + features)

    def collectFitnessScore(self, robots, feature, maxScore = 1.0):

        thisFitness = 0.0
        
        # get food collected by each robot and add to cumulative total
        for r in (range(len(robots))):
            for i in range(self.params.iterations):
                index = (feature * self.params.iterations) + i
                thisFitness += float(robots[r][index])
        # divide to get average for this iteration, normalise and add to running total
        thisFitness /= self.params.sqrt_robots * self.params.sqrt_robots
        thisFitness /= maxScore

        return thisFitness
    
    def getAvgAndDerate(self, score, individual, deratingFactor):
        fitness = score / self.params.iterations
        fitness = fitness / len(self.params.arena_params)
        fitness /= deratingFactor
        return fitness

    def deratingFactor(self, individual):

        length = float(len(individual))

        # usage = length - 64 if length > 64 else 0
        # usage = usage / 6930 if length <= 6994 else 1
        usage = length - 10 if length > 10 else 0
        usage = usage / 990 if length <= 1000 else 1
        usage = 1 - usage

        return usage

    def deratingFactorHeterogeneous(self, individual):

        if self.params.project == "straight_to_foraging":
            length = float(len(individual))
        elif self.params.project == "multi_food_foraging_with_subbehaviours":
            length = float(self.behaviours.unpack(individual))
        else:
            length = float(len(individual))

        usage = length - 100 if length > 100 else 0
        usage = usage / 9900 if length <= 10000 else 1
        usage = 1 - usage

        return usage

    def deratingFactorForForaging(self, individual):
        
        length = float(self.behaviours.unpack(individual))
        
        usage = length - 100 if length > 100 else 0
        usage = usage / 9900 if length <= 10000 else 1
        usage = 1 - usage
        
        return usage

    def getTrimmedPopulation(self, offspring, redundancy):

        trimmed = self.toolbox.empty_population(n=len(offspring))

        for i in range(len(offspring)):
            trimmed_str = redundancy.removeRedundancy(str(offspring[i]))
            trimmed_tree = self.primitivetree.from_string(trimmed_str, self.pset)
            trimmed_ind = creator.IndividualGP(trimmed_tree)
            trimmed[i] = trimmed_ind
        
        return trimmed

    def printContainer(self, container):

        population = container.items() if self.params.usingNewGrid else container.solutions.items()

        output = "\nPrint all individuals in container\n\n"

        for index, value in population:
            inds = [value] if self.params.usingNewGrid else value
            if len(inds) == 0:
                continue
            output += str(index)+"\n"
            for ind in inds:
                for fitness in ind.fitness.values:
                    output += str("%.9f" % fitness) + "  \t"
                for f in ind.features:
                    output += str("%.4f" % f) + " \t"
                output += "\n"
                # print (self.printTree(ind))
            output += "---\n"

        self.params.console(output)

    def createContainer(self, bins, domain, max_per_bin, bias = -1):

        if self.params.usingNewGrid:
            container = Grid(bins, domain, bias)
        else:
            container = Grid(shape = bins,
                             max_items_per_bin = max_per_bin,
                             fitness_domain = [(0.,numpy.inf),],
                             features_domain = domain,
                             storage_type=list)

        return container

    def writeContainerToString(self, container):

        population = container.values() if self.params.usingNewGrid else container

        container_string = ""
        for ind in population:
            container_string += str(ind)+":"
            container_string += str(ind.fitness)+":"
            container_string += str(ind.features)+"\n"
        return container_string

    def updateContainerFromString(self, redundancy, toolbox, container, filename, start = 0, stop = 0):

        count = 0
        individuals = []

        with open(filename, "r") as f:
            for line in f:

                count += 1

                if count < start:
                    continue

                if count > stop and stop != 0:
                    break

                info = line.split(":")
                ind = info[0]
                fitness = float(info[1][1:-2])
                features = info[2][1:-2].split(", ")
                features[0] = float(features[0])
                features[1] = float(features[1])
                features[2] = float(features[2])

                trimmed = redundancy.removeRedundancy(str(ind))
                tree = self.primitivetree.from_string(trimmed, self.pset)
                individual = creator.IndividualGP(tree)
                individual.fitness.values = (fitness, )
                individual.features = features

                individuals.append(individual)

        population = toolbox.empty_population(n=len(individuals))

        for j in range(len(population)):
            population[j] = individuals[j]

        self.removeDuplicates(population, container)

        if self.params.usingNewGrid:
            container.update(population)
        else:
            container.update(population, issue_warning = True)

        return container

    def getBestMax(self, container, qty = 1):

        population = container.values() if self.params.usingNewGrid else container

        best = []
        for ind in population:
            if len(best) < qty:
                best.append(ind)
            else:
                # worst = 0.0
                worst = 100.0
                worstIndex = qty
                for i in range(qty):
                    if best[i].fitness.values[0] <= worst:
                        worst = best[i].fitness.values[0]
                        worstIndex = i
                
                if ind.fitness.values[0] > worst:
                    best[worstIndex] = ind
        return best

    def printBestMax(self, container, qty = 1):

        best = self.getBestMax(container, qty)

        output = "\nPrint best individual(s)\n\n"
        for ind in best:
            output += str("%.9f" % ind.fitness.values[0]) + "  \t"
            for f in ind.features:
                output += str("%.4f" % f) + " \t"
            if len(ind) > 50:
                output += "\n"+str(ind)+"\n"
            else:
                output += "\n"+self.formatChromosome(ind)+"\n"
                output += "\n"+str(ind)+"\n"

        self.params.console(output)

    def getBestFromContainer(self, container, feature = -1, derate = True):

        population = container.values() if self.params.usingNewGrid else container
        return self.getBestFromPopulation(population, feature, derate)

    def getBestFromPopulation(self, population, feature = -1, derate = True):

        if (feature == -1):
            feature = random.randint(0, self.params.features - 1)

        for individual in population:

            thisFitness = individual.fitness.getValues()[feature]

            if derate:
                if self.params.project in ["straight_to_foraging", "multi_food_foraging_with_subbehaviours"]:
                    thisFitness *= self.deratingFactorHeterogeneous(individual)
                elif self.params.description == "foraging":
                    thisFitness *= self.deratingFactorForForaging(individual)
                else:
                    thisFitness *= self.deratingFactor(individual)

            currentBest = False

            if ('best' not in locals()):
                currentBest = True

            elif (thisFitness > bestFitness):
                currentBest = True

            elif (thisFitness == bestFitness and bestHeight > 3 and individual.height < bestHeight):
                currentBest = True

            if (currentBest):
                best = individual
                bestFitness = thisFitness
                bestHeight = individual.height

        return best

    def getBestHeterogenousSwarm(self, population):

        for individual in population:

            thisFitness = individual.fitness

            currentBest = False

            if ('best' not in locals()):
                currentBest = True

            elif (thisFitness > bestFitness):
                currentBest = True

            if (currentBest):
                best = individual
                bestFitness = thisFitness

        return best

    def getBestAll(self, population, derate = True):

        best = []
        for feature in range(self.params.features):
            best.append(self.getBestFromPopulation(population, feature, derate))
        return best

    def getExtremis(self, container, objective):

        population = container.values() if self.params.usingNewGrid else container

        val = 1.0 if objective < len(self.params.sub_behaviours) / 2 else -1.0

        best = None

        for ind in population:

            i = objective % 3
            if objective < len(self.params.sub_behaviours) / 2:
                if ind.features[i] < val:
                    val = ind.features[i]
                    best = ind
            if objective >= len(self.params.sub_behaviours) / 2:
                if ind.features[i] > val:
                    val = ind.features[i]
                    best = ind

        return best

    def getExtremaFromContainer(self, container):

        population = container.values() if self.params.usingNewGrid else container
        return self.getExtremaFromPopulation(population)

    def getExtremaFromPopulation(self, population):

        maxVals = [-1.0,-1.0,-1.0]
        maxIndividuals = [None, None, None]

        for axis in range(len(self.params.nb_bins)):

            for ind in population:

                if ind.features[axis] >= maxVals[axis]:
                    maxVals[axis] = ind.features[axis]
                    maxIndividuals[axis] = ind

        return maxIndividuals

    def printExtrema(self, container, include_trees = False):

        maxIndividuals = self.getExtremaFromContainer(container)

        output = "---------\n"
        for i in range(len(maxIndividuals)):
            output += str("%.6f" % maxIndividuals[i].features[i])+" "
        output += "\n---------\n"

        if include_trees:
            for ind in maxIndividuals:
                if True or len(ind) > 50 or self.params.algorithm == "ga":
                    output += str(ind)+"\n"
                else:
                    output += self.formatChromosome(ind)+"\n"
                output += "---------\n"

        return "\n"+output+"\n"

    def getBestGeneralist(self, population):

        val = 0.0
        best = None

        for ind in population:
            score = np.min(ind.features)
            if best == None or score > val:
                best = ind
                val = score

        return best

    def removeDuplicates(self, offspring, container):

        # this function is for preventing duplicates from reaching qdpy's
        # update function because of a bug which discards duplicates but
        # also discards the individuals they would have replaced

        population = container.values() if self.params.usingNewGrid else container.items

        for i in reversed(range(len(offspring))):
            ind = offspring[i]
            duplicate = ""
            if ind in population:
                duplicate = "DUPLICATE container"
            else:
                for j in reversed(range(i)):
                    if offspring[j] == ind:
                        duplicate = "DUPLICATE offspring"
                        break
            performance = str("%.5f" % ind.fitness.values[0]) + "  \t"
            for f in ind.features:
                performance += str("%.5f" % f) + " \t"
            
            if len(duplicate) > 0: 
                output = duplicate + "\t" + performance
                offspring.pop(i)

    def convertToNewGrid(self, container, shape):

        if self.params.usingNewGrid:
            population = container.values()
        else:
            population = container

        grid = self.createContainer(shape, self.params.features_domain, 1)
        grid.update(population)
        return grid

    def saveBestToFile(self, best):
        
        if self.params.saveOutput:
            with open(self.params.path()+'best.txt', 'w') as f:
                f.write(str(best))

    def saveBestIndividuals(self, population, generation):

        if self.params.saveBestIndividuals or self.params.saveAllIndividuals:

            if generation % self.params.best_save_period == 0:

                if not self.params.saveAllIndividuals:
                    population = self.getBestAll(population)

                with open(self.params.local_path+'/current.txt', 'w') as f:
                    f.write("\n")

                for b in population:

                    with open(self.params.local_path+'/current.txt', 'a') as f:
                        f.write("\n")
                        f.write(str(b.fitness))
                        f.write("\n\n")
                        f.write(self.formatChromosome(b))
                        f.write("\n============================================\n")

    def formatChromosome(self, chromosome):

        tree = ""
        indent = ""
        lineEnding = "\n"
        
        childrenRemaining = []
        insideComposite = 0
        insideSubtree = True
        
        for i in range(len(chromosome)):
            
            node = chromosome[i].name
            
            # ======= inner nodes =======
            
            if node.lower() in self.sequenceNodes + self.fallbackNodes + self.probabilityNodes + self.decoratorNodes:
                
                if len(childrenRemaining) > 0: childrenRemaining[-1] -= 1
                
                if node.lower() == "repeat": childrenRemaining.append(2)
                elif node.lower() in self.decoratorNodes: childrenRemaining.append(1)
                else: childrenRemaining.append(int(node[-1]))
                
                # check if any children are inner nodes
                insideSubtree = False
                composites = 0
                j = i + 1
                limit = j + childrenRemaining[-1]
                while j < limit:
                    if chromosome[j].name.lower() in self.sequenceNodes + self.fallbackNodes + self.probabilityNodes + self.decoratorNodes:
                        insideSubtree = True
                        break
                    # if chromosome[j].lower() in self.compositeNodes:
                        # limit += 2
                    j += 1
                
                # if all children are terminals print them on one line
                if insideSubtree:
                    tree += indent + node +"(" + lineEnding
                    indent += "   "
                else:
                    lineEnding = ""
                    tree += indent + node +"("
            
            # ==== composite nodes ====
            
            # elif node.lower() in self.compositeNodes:
                # if len(childrenRemaining) > 0: childrenRemaining[-1] -= 1
                # if insideSubtree: tree += indent
                # tree += node + "(" + chromosome[i+1] + ", " + chromosome[i+2] + ")"
                # if len(childrenRemaining) > 0 and childrenRemaining[-1] > 0: tree += ", "
                # tree += lineEnding
                # insideComposite = 2
                
            # elif insideComposite > 0:
                # insideComposite -= 1
                # continue
            
            # ======= terminals =======
            
            else:
                comma = ", " if len(childrenRemaining) > 0 and childrenRemaining[-1] > 1 else ""
                if insideSubtree: tree += indent
                tree += node + comma + lineEnding
                if len(childrenRemaining) > 0: childrenRemaining[-1] -= 1
            
            # ==== closing brackets ====
            
            if len(childrenRemaining) == 0 or childrenRemaining[-1] == 0:
                for i in range(len(childrenRemaining) - 1, -1, -1):
                    if childrenRemaining[i] == 0: 
                        childrenRemaining.pop()
                        if insideSubtree: 
                            indent = indent[0:-3]
                            tree += indent
                        insideSubtree = True
                        lineEnding = "\n"
                        comma = "" if i == 0 or childrenRemaining[i-1] == 0 else ", "
                        tree += ")" + comma + lineEnding
                    else: break
        
        return tree

    def getFilledBins(self, container):

        if self.params.usingNewGrid:
            return len(container.items())
        else:
            return container.filled_bins

    def getCoverage(self, container):
        
        """ get the ratio of filled vs empty bins, returns a value between 0 and 1"""

        filled_bins = self.getFilledBins(container)
        shape = self.params.nb_bins
        filled_bins /= shape[0]*shape[1]*shape[2]
        return filled_bins

    def getGridForQDScore(self, container, shape):

        if shape == self.params.nb_bins and self.params.max_items_per_bin == 1:
            return container
        else:
            return self.convertToNewGrid(container, shape)

    def getQDScore(self, container, shape = None):

        if shape == None:
            shape = self.params.nb_bins

        grid = self.getGridForQDScore(container, shape)

        population = grid.values() if self.params.usingNewGrid else grid

        total_fitness = 0.0
        for ind in population:
            total_fitness += ind.fitness.values[0]
        total_fitness /= shape[0]*shape[1]*shape[2]
        
        return total_fitness

    def getAdjustedQDScore(self, container, shape = None):

        if shape == None:
            shape = self.params.nb_bins

        grid = self.getGridForQDScore(container, shape)

        population = grid.values() if self.params.usingNewGrid else grid

        total_fitness = 0.0
        for ind in population:
            if self.params.description == "foraging":
                total_fitness += ind.fitness.values[0]
            else:
                total_fitness += ind.fitness.values[0] - 0.5
        total_fitness /= shape[0]*shape[1]*shape[2]

        if self.params.description != "foraging":
            total_fitness += 0.5

        return total_fitness

    def printRepertoireQdScores(self, container):

        output = ""
        output += "bins 1: score "+str("%.6f" % self.getAdjustedQDScore(container, [1,1,1]))+"\n"
        output += "bins 2: score "+str("%.6f" % self.getAdjustedQDScore(container, [2,2,2]))+"\n"
        output += "bins 4: score "+str("%.6f" % self.getAdjustedQDScore(container, [4,4,4]))+"\n"
        output += "bins 8: score "+str("%.6f" % self.getAdjustedQDScore(container, [8,8,8]))
        return output

    def saveConfigurationFile(self):

        experiment_length = self.params.trial_length * self.params.iterations

        with open(self.params.local_path+'/configuration.txt', 'w') as f:
            f.write("project:"+str(self.params.project)+"\n")
            f.write("sqrtRobots:"+str(self.params.sqrt_robots)+"\n")
            f.write("iterations:"+str(self.params.iterations)+"\n")
            f.write("experimentLength:"+str(experiment_length)+"\n")
            f.write("repertoireFilename:"+self.params.getRepertoireFilename()+"\n")
            f.write("nestRadius:"+str(self.params.nest_radius)+"\n")
            f.write("foodRadius:"+str(self.params.food_radius)+"\n")
            f.write("commsRange:"+str(self.params.comms_range)+"\n")
            f.write("velocity:"+str(self.params.velocity)+"\n")
            f.write("formation:"+self.params.formation+"\n")
            f.write("arenaLayout:"+str(self.params.arena_layout)+"\n")
            if self.params.arena_layout == 9:
                f.write("arenaBias:"+str(self.params.bias)+"\n")

    def saveParams(self):

        if self.params.saveOutput or self.params.saveCheckpoint or self.params.saveCSV:

            params_string = ""

            with open("../revision.txt", "r") as f:
                for line in f:
                    params_string += "------ revision "+line.strip('\t\n\r')+"----------------------------\n\n"

            params_string += "time: "+str(time.ctime()) + "\n"
            params_string += "seed: "+str(self.params.deapSeed) + "\n"

            params_string += "\n-- config --------------\n\n"

            with open(self.params.shared_path+"/config.txt", "r") as f:
                for line in f:
                    params_string += line

            params_string += "\n-- command line --------\n\n"

            for arg in self.params.command_line_args:
                params_string += arg+"\n"

            with open(self.params.path()+"params.txt", 'a') as f:
                f.write("\n"+params_string+"\n")

    def formatDuration(self, duration):

        hours = int(duration / 3600000)
        minutes = int((duration % 3600000) / 60000)
        seconds = int((duration % 60000) / 1000)

        duration_str = ""
        if hours > 0: duration_str += str(hours)+"h "
        if hours > 0 or minutes > 0: duration_str += str(minutes)+"m "
        duration_str += str(seconds)+"s"

        return duration_str

    def saveDuration(self, start_time, end_time, to_console = True):

        duration = end_time - start_time
        duration_str = self.formatDuration(duration)

        if to_console:
            self.params.console("\nDuration: " + duration_str + "\n")

        if self.params.saveOutput or self.params.saveCheckpoint or self.params.saveCSV:
            with open(self.params.path()+"params.txt", 'a') as f:
                f.write("-- finish --------------\n\n")
                f.write("generations: "+str(self.params.generations) + "\n")
                f.write("duration: "+duration_str+" ("+str(duration) + " ms)\n")
                f.write("\n")

    def getCsvIndex(self, objective, algorithm_name):
        if algorithm_name == "mtc":
            return self.getMtcIndex(objective)
        elif algorithm_name == "mti":
            return self.getMtiIndex(objective)
        else:
            return 0

    def getMtcIndex(self, objective):
        mtc_index = -1
        if objective in [0, 2]: mtc_index = 0
        if objective in [1, 3]: mtc_index = 1
        if objective in [4, 5]: mtc_index = 2
        return mtc_index

    def getMtiIndex(self, objective):
        mti_index = -1
        if objective in [0, 3]: mti_index = 0
        if objective in [1, 4]: mti_index = 1
        if objective in [2, 5]: mti_index = 2
        return mti_index

    def getIfoodLegacyDescription(self, objective, algorithm):

        objectives = []
        for i in range(len(self.params.objectives)):
            if self.params.objectives[i] == "ifood-perceived-position":
                objectives.append("ifood")
            else:
                objectives.append(self.params.objectives[i])
        return self.getExperimentDescription(objective, algorithm, objectives)

    def getExperimentDescription(self, objective, algorithm, objectives = None):

        if objectives == None:
            objectives = self.params.objectives

        if algorithm == "mtc":
            if objective in [0, 1, 5]: return objectives[0]+"-"+objectives[1]+"-"+objectives[5]
            if objective in [2, 3, 4]: return objectives[2]+"-"+objectives[3]+"-"+objectives[4]
        elif algorithm == "mti":
            if objective in [0, 1, 2]: return objectives[0]+"-"+objectives[1]+"-"+objectives[2]
            if objective in [3, 4, 5]: return objectives[3]+"-"+objectives[4]+"-"+objectives[5]
        else:
            return objectives[objective]

    def getExperimentDirectory(self, objective, algorithm):
        if self.params.objectives[objective] == "foraging":
            # currently only used in combine.py and extrema.py so always default to baseline
            return "foraging/baseline"
        else:
            return self.getExperimentDescription(objective, algorithm)

    def getLegacyCheckpointFilename(self, path, algorithm, seed, objective, generations):

        filename = path+"/"+str(seed)+"/"

        if self.params.project == "legacy" and "qd" in algorithm:
            filename += "seed"+str(seed)+"-iteration"+str(generations)+".p"
        elif self.params.project == "legacy":
            description = self.getIfoodLegacyDescription(objective, algorithm)
            filename += "checkpoint-"+description+"-"+str(seed)+"-"+str(generations)+".pkl"
        else:
            objective_name = self.params.objectives[objective]
            filename += "checkpoint-"+objective_name+"-"+str(seed)+"-"+str(generations)+"-"+objective_name+".txt"

        return filename

    def getLegacyCheckpointContainer(self, container, algorithm, filename, objective):

        if self.params.project == "legacy":
            with open(filename, "rb") as checkpoint_file:
                checkpoint = pickle.load(checkpoint_file)
            if algorithm == "qdpy":
                containers = [checkpoint["container"]]
            else:
                containers = checkpoint["containers"]
            population = []

            index = self.getCsvIndex(objective, algorithm)
            for ind in containers[index]:
                population.append(ind)
            container.update(population)

        else:
            container = self.updateContainerFromString(self.redundancy, self.utilities.toolbox, container, filename)

    def saveContainer(self, container, directory, filename):
        container_string = self.writeContainerToString(container)
        Path(directory+"/").mkdir(parents=True, exist_ok=True)
        with open(filename, "w") as f:
            f.write(container_string)


    def evaluate(self, assign_fitness, invalid_ind):

        # fitnesses = self.toolbox.map(self.toolbox.evaluate, invalid_ind)
        # assign_fitness(invalid_ind, fitnesses)

        self.split(assign_fitness, invalid_ind)


    def split(self, assign_fitness, population):

        num_threads = self.params.num_threads

        pop = []
        for i in range(num_threads):
            pop.append([])

        for i in range(len(population)):
            for j in range(num_threads):
                if i % num_threads == j:
                    pop[j].append(population[i])
                    continue

        threads = []
        for i in range(num_threads):
            threads.append(threading.Thread(target=self.evaluation_functions[i], args=(assign_fitness, [pop[i]], getattr(self.toolbox, "evaluate"+str(i+1)))))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()


    def makeEvaluationFunction(self, name):

        def _method(assign_fitness, population, evaluation_function):
            toolbox_function = getattr(self.toolbox, name)
            fitnesses = self.toolbox.map(toolbox_function, population[0])
            assign_fitness(population[0], fitnesses)

        return _method

    def raiseError(self, message):
        now = datetime.now()
        self.params.console(message)
        with open(self.params.shared_path+"/"+self.params.algorithm+"/errors"+str(self.params.deapSeed)+".txt", "a") as f:
            f.write(now.strftime("%H:%M %d/%m/%Y")+" ")
            f.write(message)
            f.write("\n")
        with open(self.params.local_path+"/runtime.txt", "w") as f:
            f.write("cancel\n")

    def printError(self, args):
        self.params.console("\n\nException")
        for arg in args:
            self.params.console(arg)
        print("\n\n")
