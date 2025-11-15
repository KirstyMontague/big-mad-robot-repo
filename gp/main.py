import sys
sys.path.insert(0, '..')

from params import eaParams
params = eaParams()
params.configure()

if not params.stop:

	import random
	import os
	import argparse
	from pathlib import Path
	import numpy

	from deap import tools


	from ea import EA

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

		ea.utilities.params.deapSeed = 1
		individual = ""
		sqrtRobots = 0

		with open("../txt/best.txt", "r") as f:
			for line in f:
				if sqrtRobots == 0:
					sqrtRobots = line
				elif individual == "":
					individual = line

		fitness = ea.utilities.evaluateRobot(individual, 1)
		print (fitness)

	def trimOneIndividual():

		individual = ""
		sqrtRobots = 0

		with open("../txt/best.txt", "r") as f:
			for line in f:
				if sqrtRobots == 0:
					sqrtRobots = line
				elif individual == "":
					individual = line

		print(individual)
		try:
			trimmed = ea.redundancy.removeRedundancy(individual)
			print ()
			print (trimmed)
		except: return

	def main():

		# evaluateOneIndividual()
		# return

		# trimOneIndividual()
		# return

		parseArguments()

		params.local_path += "/"+str(params.deapSeed)
		Path(params.local_path+"/").mkdir(parents=False, exist_ok=True)

		if params.saveOutput or params.saveCSV or params.saveCheckpoint:
			Path(params.shared_path+"/"+params.algorithm+"/").mkdir(parents=False, exist_ok=True)
			Path(params.shared_path+"/"+params.algorithm+"/"+params.description+"/").mkdir(parents=False, exist_ok=True)

		if params.saveOutput or params.saveCheckpoint:
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

		ea = EA(params)
		ea.eaInit(mstats, halloffame=hof)
		

		if os.path.exists(params.local_path+"/runtime.txt"):
			os.remove(params.local_path+"/runtime.txt")
		if os.path.exists(params.local_path+"/current.txt"):
			os.remove(params.local_path+"/current.txt")
		os.remove(params.local_path+"/configuration.txt")
		if len(os.listdir(params.local_path)) == 0:
			os.rmdir(params.local_path)


	if __name__ == "__main__":
		main()
