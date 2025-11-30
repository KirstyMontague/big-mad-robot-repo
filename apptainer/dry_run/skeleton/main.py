
import argparse
import os
import subprocess

from params import eaParams

class Utilities():

    def __init__(self, params):
        self.params = params
    
    def parseArguments(self):
        
        parser = argparse.ArgumentParser()
        parser.add_argument('--seed', type=int, default=None, help="DEAP random seed")
        args = parser.parse_args()

        if args.seed != None:
            self.params.deapSeed = args.seed

    def evaluateRobot(self):
        
        text_input = "empty"
        with open(self.params.shared_path+"/input"+str(self.params.deapSeed)+".txt", "r") as f:
            for line in f:
                text_input = line
        print(text_input)
        
        print(self.params.local_path+"/chromosome"+str(self.params.deapSeed)+".txt")
        with open(self.params.local_path+"/chromosome"+str(self.params.deapSeed)+".txt", "w") as f:
            f.write(text_input)
        
        subprocess.call(["/bin/bash", "evaluate", self.params.local_path, str(self.params.deapSeed), "./"])
        
        result = ""
        with open(self.params.local_path+"/result"+str(self.params.deapSeed)+".txt", "r") as f:
            for line in f:
                result = line[0:-1]
        
        return result

if __name__ == "__main__":

    params = eaParams()

    utilities = Utilities(params)
    utilities.parseArguments()

    result = utilities.evaluateRobot()

    path = params.shared_path+"/result"+str(params.deapSeed)+".txt"

    with open(path, "w") as f:
        f.write(result +" from seed "+str(params.deapSeed)+"\n")

    message = "no result\n" + path
    with open(path, "r") as f:
        for line in f:
            message = line

    chromosome_file = params.local_path+"/chromosome"+str(params.deapSeed)+".txt"
    if os.path.exists(chromosome_file):
        os.remove(chromosome_file)

    results_file = params.local_path+"/result"+str(params.deapSeed)+".txt"
    if os.path.exists(results_file):
        os.remove(results_file)

    print("\n"+message+"\n")
