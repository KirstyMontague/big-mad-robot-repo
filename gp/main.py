import sys
sys.path.insert(0, '..')

import argparse

from params import eaParams
params = eaParams()

def parseArguments():

    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default=None, help="DEAP random seed")
    parser.add_argument('--objective', type=int, default=None, help="Single objective")
    parser.add_argument('--using_repertoire', type=str, default=None, help="Using repertoire")
    parser.add_argument('--bins_per_axis', type=int, default=None, help="Bins per axis")
    args = parser.parse_args()

    if args.seed != None:
        params.deapSeed = args.seed

    if args.objective != None:
        params.command_line_args.append("indexes "+str(args.objective))

    if args.using_repertoire != None:
        params.command_line_args.append("using_repertoire "+str(args.using_repertoire))

    if args.bins_per_axis != None:
        params.command_line_args.append("bins_per_axis "+str(args.bins_per_axis))

parseArguments()
params.configure()

if not params.stop:

    import os
    from ea import EA

    def evaluateOneIndividual():

        from pathlib import Path
        params.local_path += "/1"
        Path(params.local_path+"/").mkdir(parents=False, exist_ok=True)

        individual = ""
        sqrtRobots = 0
        with open("../argos3/best.txt", "r") as f:
            for line in f:
                individual = line

        ea = EA(params)
        fitness = ea.utilities.evaluateRobot(individual, 1)
        print("\n"+str(fitness)+"\n")

    def trimOneIndividual():

        ea = EA(params)
        individual = ""
        sqrtRobots = 0

        with open("../argos3/best.txt", "r") as f:
            for line in f:
                individual = line

        print()
        print(individual)
        print()
        try:
            trimmed = ea.redundancy.removeRedundancy(individual)
            print(trimmed)
            print()
        except: return

    def main():

        # evaluateOneIndividual()
        # return

        # trimOneIndividual()
        # return

        params.makePaths()

        ea = EA(params)
        ea.eaInit()

        params.deleteTempFiles()


    if __name__ == "__main__":
        main()
