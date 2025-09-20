
import random

from deap import base
from deap import creator
from deap import tools

from archive import Archive
from params import Params
from utilities import Utilities

class EA():
    
    def __init__(self):

        self.params = Params()
        self.utilities = Utilities(self.params)

        self.utilities.configure()
        if self.params.cancelled:
            return

        if self.params.seed == 0: self.params.seed = self.utilities.parseArguments()
        if self.params.seed == None:
            print("no seed")
            return

        self.archive = Archive(self.utilities, self.params)
        self.eaInit()

    def eaInit(self):

        random.seed(self.params.seed)

        self.archive.loadArchives()

        pop = self.utilities.toolbox.population(n=self.params.population_size)
        self.evaluateNewPopulation(0, pop)

        self.eaLoop(pop)

        if self.params.save_output:
            self.archive.saveArchive()

        best = tools.selBest(pop, 1)[0]
        csv_string = str(self.params.objective) +","
        csv_string += str(self.params.seed) +","
        csv_string += str(self.params.generations) +","
        csv_string += str(best.fitness.getValues()[0]) +","
        for c in best:
            csv_string += str(c) + " "
        csv_string = csv_string[0:-1]
        csv_string += "\n"

        if self.params.print_csv:
            print()
            print(csv_string)
            print()

        if self.params.save_csv:
            with open(self.params.csv, 'a') as f:
                f.write(csv_string)


    def eaLoop(self, pop):

        gen = 0

        while gen < self.params.generations:

            gen = gen + 1

            elites = tools.selBest(pop, self.params.elites)

            offspring = self.utilities.toolbox.select(pop, len(pop) - len(elites))
            offspring = list(map(self.utilities.toolbox.clone, offspring))

            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < self.params.CXPB:
                    self.utilities.toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values

            for mutant in offspring:
                if random.random() < self.params.MUTPB:
                    self.utilities.toolbox.mutate(mutant)
                    del mutant.fitness.values

            pop[:] = self.evaluateNewPopulation(gen, elites + offspring)

            self.utilities.configure()

    def evaluateNewPopulation(self, generation, offspring):

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        invalid_orig = len(invalid_ind)

        matched = [0,0]
        invalid_ind = self.archive.assignDuplicateFitness(invalid_ind, self.assignFitness, matched)
        archive_ind = invalid_ind

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        invalid_new = len(invalid_ind)

        trimmed = self.utilities.trimPopulationPrecision(invalid_ind)
        self.utilities.evaluate(self.assignPopulationFitness, trimmed)
        self.transferTrimmedFitnessScores(invalid_ind, trimmed)

        for ind in invalid_ind:
            self.archive.addToArchive(ind)

        for ind in archive_ind:
            self.archive.addToCompleteArchive(ind)

        best = tools.selBest(offspring, 1)[0]
        score = str("%.7f" % best.fitness.values[0]) + "\t"

        if (generation % 1 == 0 or invalid_new > 0):
            print ("\t"+str(self.params.seed)+" - "+str(generation)+" - "+str(score)+"\tinvalid "+str(invalid_new)+" / "+str(invalid_orig)+" (matched "+str(matched[0])+" & "+str(matched[1])+")")

        return offspring

    def transferTrimmedFitnessScores(self, invalid_ind, trimmed):
        for i in range(len(invalid_ind)):
            invalid_ind[i].fitness.values = trimmed[i].fitness.values

    def assignFitness(self, offspring, fitness):
        offspring.fitness.values = fitness

    def assignPopulationFitness(self, population, fitnesses):
        for ind, fit in zip(population, fitnesses):
            ind.fitness.values = fit
