import sys
sys.path.insert(0, '..')

from params import eaParams
params = eaParams()
params.configure()

# from redundancy import Redundancy
# redundancy = Redundancy()
# redundancy.params.is_qdpy = False

# redundancy.checkRedundancy()
# redundancy.checkProbmNodes()

# if False:
if not params.stop:

	import random
	import os
	import argparse
	from pathlib import Path
	import numpy

	from deap import tools


	from ea import EA

	ea = EA(params)

	def parseArguments():
		
		parser = argparse.ArgumentParser()
		parser.add_argument('--seed', type=int, default=None, help="DEAP random seed")
		parser.add_argument('--start', type=int, default=None, help="Start generation")
		parser.add_argument('--end', type=int, default=None, help="Max generations")
		args = parser.parse_args()

		if args.seed != None:
			params.deapSeed = args.seed

		if args.start != None:
			params.start_gen = args.start
			if int(args.start) == 0: params.loadCheckpoint = False
			if int(args.start) > 0: params.loadCheckpoint = True

		if args.end != None:
			params.generations = args.end

	def evaluateOneIndividual():

		individual = ""

		f = open("../txt/best.txt", "r")
		for line in f:
			if line == "3": continue
			else:
				individual = line

		fitness = ea.utilities.evaluateRobot(individual, 1)
		print (fitness)

	def main():

		# evaluateOneIndividual()
		# return

		parseArguments()
		
		if params.saveOutput:
			Path(params.path()).mkdir(parents=False, exist_ok=True)

		random.seed(params.deapSeed)
		
		hof = tools.HallOfFame(1)
		
		stats_fit = tools.Statistics(key=lambda ind: ind.fitness.values[0])
		stats_size = tools.Statistics(key=lambda depth: depth.height)
		mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)

		stats = tools.Statistics(lambda ind: ind.fitness.values)
		mstats.register("avg", numpy.mean)
		mstats.register("med", numpy.median)
		mstats.register("std", numpy.std)
		mstats.register("min", numpy.min)
		mstats.register("max", numpy.max)

		ea.eaInit(mstats, halloffame=hof)
		


	if __name__ == "__main__":
		main()
