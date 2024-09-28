
import time

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
        output += ","
        
        # self.output += str(self.params.unseenIterations)+", "

        # for param in self.params.unseenParams:
            # self.output += str(param)+" "
        # self.output += ","
        
        # self.output += "\""
        # for node in sorted(self.params.nodes):
            # if (self.params.nodes[node]):
                # self.output += node+", "
        # self.output += "\","
        
        output += ","

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
            logHeaders += ",Chromosome,Nodes,"
            
            # get the best individual at the end of the evolutionary run
            allBest = []
            for i in range(self.params.features):
                bestThisPop = self.utilities.getBestHDRandom(population, i)
                allBest.append(bestThisPop)		
                performance = ""
                for f in bestThisPop.fitness.values:
                    performance += str("%.5f" % f) + " \t"

            chromosomes = ",\""
            for bestThisPop in allBest:
                chromosomes += ""+str(bestThisPop)+" + "
            chromosomes = chromosomes[0:-3]
            chromosomes += "\",,"
            
            nodes = ""
            for node in self.params.nodes:
                if node: nodes += node+" "

            filename = self.params.csvOutputFilename(generation)
            with open(filename, 'a') as f:
                f.write(logHeaders)
                f.write("\n")
                f.write(output)
                f.write(chromosomes)
                f.write(nodes)
