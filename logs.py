
import time
import os

class Logs():

    def __init__(self, params, utilities):
        self.params = params
        self.utilities = utilities

    def logFirst(self):

        # save parameters to the output

        output = self.params.description+","
        output += str(time.time())[0:10]+","
        output += str(self.params.deapSeed)+","
        output += str(self.params.sqrtRobots)+","
        output += str(self.params.populationSize)+","
        output += str(self.params.tournamentSize)+","

        output += str(self.params.iterations)+","

        for param in self.params.arenaParams:
            output += str(param)+" "

        output += ",,"

        return output

    def logFitness(self, best):
        output = ""
        for i in range(self.params.features):
            output += str("%.6f" % best[i].fitness.values[i])+" "
        output += ","
        return output

    def saveCSV(self, generation, population, output):

        if self.params.saveCSV and generation % self.params.csv_save_period == 0:

            logHeaders = "Type,Time,Seed,Robots,Pop,Tourn,Iterations,Params,,"
            for i in range(generation + 1):
                logHeaders += str(i)+","
            logHeaders += ",Chromosome,,Nodes\n"

            allBest = []
            for i in range(self.params.features):
                allBest.append(self.utilities.getBestHDRandom(population, i))

            chromosomes = ",\""
            for best in allBest:
                chromosomes += str(best)+" + "
            chromosomes = chromosomes[0:-3]
            chromosomes += "\",,"

            nodes = ""
            for node in self.params.nodes:
                if node: nodes += node+" "

            filename = self.params.csvOutputFilename(generation)

            output_string = ""
            if not os.path.exists(filename): output_string += logHeaders
            output_string += output
            output_string += chromosomes
            output_string += nodes

            with open(filename, 'a') as f:
                f.write(output_string)


