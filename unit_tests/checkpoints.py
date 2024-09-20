import sys
sys.path.insert(0, '..')

import subprocess
import pickle
import os

from params import eaParams

if __name__ == "__main__":

    params = eaParams()
    params.deapSeed = 2
    filename = params.checkpointInputFilename(10)

    # go to gp directory

    os.chdir("../gp")

    # run for 10 generations to get data for comparison

    with open("../config.txt", 'w') as f:
        f.write("generations 10\n")
        f.write("saveOutput True\n")
        f.write("saveCSV False\n")
        f.write("save_period 5")

    subprocess.call(["python3", "main.py", "--seed",  "2"])

    with open(filename, "rb") as checkpoint_file:
        checkpoint = pickle.load(checkpoint_file)
    expected_population = checkpoint["population"]


    # run from 5 to 10 generations to get checkpoint data

    with open("../config.txt", 'w') as f:
        f.write("loadCheckpoint True\n")
        f.write("start_gen 5\n")
        f.write("generations 10\n")
        f.write("saveOutput True\n")
        f.write("saveCSV False")

    subprocess.call(["python3", "main.py", "--seed",  "2"])

    with open(filename, "rb") as checkpoint_file:
        checkpoint = pickle.load(checkpoint_file)
    actual_population = checkpoint["population"]


    # check results

    if expected_population == actual_population:
        print("passed")
    else:
        print("failed")


    # clear config file

    with open("../config.txt", 'w') as f:
        f.write("")
