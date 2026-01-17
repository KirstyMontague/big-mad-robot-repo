import sys
sys.path.insert(0, '..')

import argparse

from params import eaParams
params = eaParams()

def parseArguments():

    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default=None, help="DEAP random seed")
    parser.add_argument('--objective', type=int, default=None, help="Single objective")
    args = parser.parse_args()

    if args.seed != None:
        params.deapSeed = args.seed

    if args.objective != None:
        params.command_line_args.append("indexes "+str(args.objective))


parseArguments()
params.configure()

if not params.stop:

    from ea import EA

    def main():

        ea = EA(params)
        ea.run()

    if __name__ == "__main__":
        main()
