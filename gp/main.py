import sys
sys.path.insert(0, '..')

import argparse

from params import eaParams
params = eaParams()

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
        print ("\n"+str(fitness)+"\n")

    def trimOneIndividual():

        ea = EA(params)
        individual = ""
        sqrtRobots = 0

        with open("../argos3/best.txt", "r") as f:
            for line in f:
                individual = line

        print()
        print(individual)
        try:
            trimmed = ea.redundancy.removeRedundancy(individual)
            print (trimmed)
            print ()
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
