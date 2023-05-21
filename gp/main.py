import sys
sys.path.insert(0, '..')

from params import eaParams
params = eaParams()
params.configure()

# from redundancy import Redundancy
# redundancy = Redundancy()
# redundancy.mapNodesToArchive("seqm2(f, f)")
# redundancy.checkRedundancy()
# redundancy.checkProbmNodes()
# redundancy.removeRedundancy("selm4(ifOnFood, seqm2(seqm2(seqm2(seqm3(selm2(r, ifOnFood), ifOnFood, rl), seqm2(ifOnFood, ifRobotToRight)), seqm2(seqm2(seqm2(selm2(ifOnFood, ifOnFood), seqm2(seqm2(seqm2(seqm2(seqm2(seqm2(selm3(fl, seqm2(rr, seqm2(seqm2(rr, ifInNest), ifRobotToLeft)), selm3(seqm2(r, ifOnFood), seqm2(fl, fl), rl)), seqm2(seqm2(ifOnFood, rr), seqm2(selm2(ifOnFood, seqm2(seqm2(seqm2(seqm2(selm3(fr, fr, ifRobotToLeft), seqm2(fl, fl)), rr), seqm2(fl, fl)), rr)), ifOnFood))), rr), fl), fl), seqm2(ifOnFood, fl)), rr)), seqm2(seqm2(selm2(selm3(seqm2(r, seqm2(seqm2(fl, fl), rr)), rr, rl), seqm2(selm3(seqm2(ifNestToRight, fl), seqm2(selm3(fl, seqm2(ifInNest, seqm2(seqm2(r, ifOnFood), ifOnFood)), selm3(seqm2(r, ifOnFood), seqm2(seqm2(ifOnFood, ifOnFood), fl), rl)), seqm2(selm2(r, ifNestToLeft), seqm2(selm2(ifOnFood, seqm2(seqm2(seqm2(fl, rr), seqm2(selm3(seqm2(ifNestToRight, fl), ifRobotToRight, ifNestToLeft), fl)), rr)), ifOnFood))), seqm2(ifOnFood, ifNestToLeft)), seqm2(seqm2(selm3(seqm2(ifNestToRight, ifOnFood), rr, seqm2(seqm2(seqm2(seqm2(selm3(ifRobotToRight, fr, r), seqm2(fl, fl)), rr), seqm2(selm3(seqm2(rr, fl), ifNestToRight, rl), f)), rl)), seqm2(fl, fl)), ifRobotToRight))), rr), seqm2(seqm2(seqm2(seqm2(seqm2(seqm2(selm2(ifOnFood, seqm2(seqm2(seqm2(seqm2(selm3(ifRobotToRight, fr, ifOnFood), seqm2(fl, fl)), rr), seqm2(selm3(seqm2(fl, fl), ifNestToRight, seqm2(ifNestToRight, fl)), rr)), fl)), seqm2(seqm2(ifOnFood, rr), seqm2(selm2(ifOnFood, seqm2(seqm2(seqm2(seqm2(selm3(f, fr, ifOnFood), seqm2(fl, rr)), rr), seqm2(seqm3(seqm2(rr, fl), ifRobotToRight, rl), rr)), fl)), ifOnFood))), seqm2(seqm2(seqm2(selm3(ifOnFood, ifInNest, ifOnFood), seqm2(fl, fl)), fr), ifNestToRight)), seqm2(seqm2(seqm2(seqm2(seqm3(selm2(r, ifNestToLeft), ifOnFood, rl), seqm2(ifOnFood, ifOnFood)), seqm2(fl, seqm2(ifOnFood, fl))), seqm2(selm3(seqm2(seqm2(selm3(seqm2(rr, fl), ifNestToRight, ifRobotToLeft), rr), fl), seqm2(rr, seqm2(ifOnFood, ifRobotToRight)), seqm2(ifNestToRight, fl)), rr)), fl)), fl), seqm2(ifOnFood, ifRobotToLeft)), rr))), ifNestToLeft)), fr), seqm2(seqm2(ifOnFood, rr), fl), ifOnFood)")

# if False and not params.stop:
if not params.stop:

	import time
	import copy
	import random
	import subprocess
	import os
	import pickle
	import argparse
	from pathlib import Path

	import numpy

	from functools import partial

	from deap import algorithms
	from deap import base
	from deap import creator
	from deap import tools
	from deap import gp


	from ea import EA
	from utilities import Utilities

	ea = EA()
	ea.setParams(params)
	utilities = Utilities(params)

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
			# if int(params.start_gen) == 0:
				# params.loadCheckpoint = False

		if args.end != None:
			params.generations = args.end
		
	def evaluateOneIndividual():
		
		individual = ""
		
		f = open("../txt/best.txt", "r")
		for line in f:
			if line == "3": continue
			else:
				individual = line
		
		# invalid_ind = [creator.Individual.from_string(individual, pset)]
		# fitness = toolbox.map(toolbox.evaluate, invalid_ind)
		
		fitness = utilities.evaluateRobot(individual, 1)
		print (fitness)
		# for ind, fit in zip(invalid_ind, fitness):
			# print (fit)
			# ind.fitness.values = fit

		
		
	"""
	toolbox = base.Toolbox()

	pset = gp.PrimitiveSet("MAIN", 0)
	params.addNodes(pset)

	weights = []
	for i in range(params.features): weights.append(1.0)
	# qdpy optimisation
	weights.append(1.0)
	weights.append(1.0)
	weights.append(1.0)
	# end qdpy
	weights2 = (weights)
	creator.create("Fitness", base.Fitness, weights=weights2)
	creator.create("Individual", gp.PrimitiveTree, fitness=creator.Fitness)

	toolbox.register("expr_init", gp.genFull, pset=pset, min_=1, max_=4)

	toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr_init)
	toolbox.register("population", tools.initRepeat, list, toolbox.individual)

	toolbox.register("evaluate", utilities.evaluateRobot, thread_index=1)
	toolbox.register("evaluate1", utilities.evaluateRobot, thread_index=1)
	toolbox.register("evaluate2", utilities.evaluateRobot, thread_index=2)
	toolbox.register("evaluate3", utilities.evaluateRobot, thread_index=3)
	toolbox.register("evaluate4", utilities.evaluateRobot, thread_index=4)
	toolbox.register("select", ea.selTournament, tournsize=params.tournamentSize)

	toolbox.register("mate", gp.cxOnePoint)
	toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
	toolbox.register("mutSubtreeReplace", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)
	toolbox.register("mutSubtreeShrink", gp.mutShrink)
	toolbox.register("mutNodeReplace", gp.mutNodeReplacement, pset=pset)
	"""

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
