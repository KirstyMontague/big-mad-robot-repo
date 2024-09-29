
import time
import os

class Logs():

    def __init__(self, params, utilities):
        self.params = params
        self.utilities = utilities
        self.output = ""
        self.qd_scores = ""
        self.coverage = ""

    def getParameters(self):

        parameters = self.params.description+","
        parameters += str(time.time())[0:10]+","
        parameters += str(self.params.deapSeed)+","
        parameters += str(self.params.sqrtRobots)+","
        parameters += str(self.params.populationSize)+","
        parameters += str(self.params.tournamentSize)+","

        parameters += str(self.params.iterations)+","

        for param in self.params.arenaParams:
            parameters += str(param)+" "

        parameters += ",,"

        return parameters

    def fitnessFromCheckpoint(self, fitness):
        self.output = fitness

    def logFitness(self, best):

        for i in range(self.params.features):
            self.output += str("%.6f" % best[i].fitness.values[i])+" "
        self.output += ","

    def logQdScore(self, qd_scores):
        for i in range(self.params.features):
            self.qd_scores += str(qd_scores[i])+" "
        self.qd_scores += ","

    def logCoverage(self, coverage):
        self.coverage += str(coverage)+","

    def getHeadings(self, generation):

        headings = "Type,Time,Seed,Robots,Pop,Tourn,Iterations,Params,,"
        for i in range(generation + 1):
            headings += str(i)+","
        headings += ",Chromosome,,Nodes\n"

        return headings

    def getChromosomes(self, population):

        allBest = []
        for i in range(self.params.features):
            allBest.append(self.utilities.getBestHDRandom(population, i))

        chromosomes = ",\""
        for best in allBest:
            chromosomes += str(best)+" + "
        chromosomes = chromosomes[0:-3]
        chromosomes += "\",,"

        return chromosomes

    def getNodes(self):

        nodes = ""
        for node in self.params.nodes:
            if node: nodes += node+" "

        return nodes

    def saveCSV(self, generation, population):

        if self.params.saveCSV and generation % self.params.csv_save_period == 0:

            headings = self.getHeadings(generation)
            parameters = self.getParameters()
            chromosomes = self.getChromosomes(population)
            nodes = self.getNodes()
            self.write("best", generation, headings, parameters, self.output, chromosomes, nodes)
            self.write("qd-scores", generation, headings, parameters, self.qd_scores, chromosomes, nodes)
            self.write("coverage", generation, headings, parameters, self.coverage, chromosomes, nodes)

    def write(self, query, generation, headings, parameters, output, chromosomes, nodes):

        filename = self.params.csvOutputFilename(generation, query)

        output_string = ""
        if not os.path.exists(filename): output_string += headings
        output_string += parameters
        output_string += output
        output_string += chromosomes
        output_string += nodes
        output_string += "\n"

        with open(filename, 'a') as f:
            f.write(output_string)

