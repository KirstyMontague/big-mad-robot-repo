
import argparse
import os
import time
import warnings

from pathlib import Path
from datetime import datetime

from archive import Archive
from params import Params
from utilities import Utilities

warnings.filterwarnings("error")


class EA():
    
    def __init__(self):

        start_time = round(time.time() * 1000)

        self.params = Params()

        if self.params.seed == 0: self.params.seed = self.parseArguments()
        if self.params.seed == None:
            print("\nno seed\n")
            return

        self.params.configure()
        print()

        if self.params.cancelled:
            self.params.console("\naborted\n")
            return

        if self.params.stop:
            return

        self.params.makePaths()

        self.utilities = Utilities(self.params)

        if self.params.useArchive:
            self.archive = Archive(self.utilities, self.params)
            self.archive.loadArchives()

        self.utilities.setSeed()
        self.best = None

        self.utilities.saveConfigurationFile()

        population = self.eaLoop()

        self.eaFinish(start_time, population)

    def eaFinish(self, start_time, population):

        end_time = round(time.time() * 1000)

        if self.params.saveOutput or self.params.saveCSV or self.params.saveBest:
            Path(self.params.path()).mkdir(parents=True, exist_ok=True)
            self.utilities.saveParams()
        self.utilities.saveDuration(start_time, end_time)

        self.params.deleteTempFiles()

        if self.params.saveBest:
            with open(self.params.bestFilename(), "w") as f:
                f.write(str(self.params.ind_size))
                for s in self.best:
                    f.write(" ")
                    f.write(str(s))

        if self.params.saveOutput and self.params.useArchive:
            self.archive.saveArchive()

        if self.params.saveCSV:
            csv_string = ""
            if not os.path.exists(self.params.csvFilename()):
                csv_string += "Objective,"
                csv_string += "Seed,"
                csv_string += "Hidden Nodes,"
                csv_string += ","+str(self.params.generations)+",,"
                csv_string += "Chromosome\n"
            csv_string += str(self.params.objective) +","
            csv_string += str(self.params.seed) +","
            csv_string += str(self.params.num_hidden) +","
            csv_string += ","+str(self.best.fitness.getValues()[0]) +",,"
            for c in self.best:
                csv_string += str(c) + " "
            csv_string = csv_string[0:-1]
            csv_string += "\n"
            with open(self.params.csvFilename(), 'a') as f:
                f.write(csv_string)

    def eaLoop(self):

        generation = 0

        while generation <= self.params.generations:

            try:
                population = self.utilities.toolbox.generate()
                self.evaluateNewPopulation(generation, population)
                self.utilities.toolbox.update(population)

            except Exception as e:
                now = datetime.now()
                self.params.console(str(e))
                with open(self.params.shared_path+'/cma-es/errors'+str(self.params.seed)+'.txt', 'a') as f:
                    f.write(now.strftime("%H:%M %d/%m/%Y")+" ")
                    f.write(str(e))
                    f.write("\n")
                with open(self.params.local_path+'/runtime.txt', 'a') as f:
                    f.write("stop\n")

            self.params.runtime()
            generation += 1

        return population

    def evaluateNewPopulation(self, generation, population):

        invalid_ind = [ind for ind in population if not ind.fitness.valid]
        invalid_orig = len(invalid_ind)

        matched = [0,0]

        if self.params.useArchive:
            invalid_ind = self.archive.assignDuplicateFitness(invalid_ind, self.assignFitness, matched)
            archive_ind = invalid_ind

        invalid_ind = [ind for ind in population if not ind.fitness.valid]
        invalid_new = len(invalid_ind)

        trimmed = self.utilities.trimPopulationPrecision(invalid_ind)
        self.utilities.evaluate(self.assignPopulationFitness, trimmed)
        self.transferTrimmedFitnessScores(invalid_ind, trimmed)

        if self.params.useArchive:
            for ind in invalid_ind:
                self.archive.addToArchive(ind)
            for ind in archive_ind:
                self.archive.addToCompleteArchive(ind)

        best = self.utilities.getBest(population)[0]

        if self.best == None or best.fitness.getValues()[0] > self.best.fitness.getValues()[0]:
            self.best = best

        output = "\t"+str(self.params.seed)+" - "
        output += str(generation)+" - "
        output += str("%.7f" % best.fitness.getValues()[0]) + "\t"
        output += str("%.7f" % self.best.fitness.getValues()[0]) + "\t"
        output += "invalid "+str(invalid_new)+" / "+str(invalid_orig)+" "
        output += "(matched "+str(matched[0])+" & "+str(matched[1])+")"

        write_out = False
        if generation % self.params.output_interval == 0 and invalid_new > 0: write_out = True
        if generation % 100 == 0 or generation == self.params.generations: write_out = True
        if write_out: self.params.console(output)

    def transferTrimmedFitnessScores(self, invalid_ind, trimmed):
        for i in range(len(invalid_ind)):
            invalid_ind[i].fitness.values = trimmed[i].fitness.values

    def assignFitness(self, offspring, fitness):
        offspring.fitness.values = fitness

    def assignPopulationFitness(self, population, fitnesses):
        for ind, fit in zip(population, fitnesses):
            ind.fitness.values = fit

    def parseArguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--seed', type=int, default=None, help="DEAP random seed")
        args = parser.parse_args()
        if args.seed != None:
            return args.seed
