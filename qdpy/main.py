import sys
sys.path.insert(0, '..')

from params import eaParams
params = eaParams()
params.configure()

if not params.stop:

    from ea import EA
    import argparse

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

    def main():

        parseArguments()
        ea = EA(params)
        ea.run()

    if __name__ == "__main__":
        main()
