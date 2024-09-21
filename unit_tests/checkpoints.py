import sys
sys.path.insert(0, '..')

import subprocess
import pickle
import os

from params import eaParams

if __name__ == "__main__":

    params = eaParams()
    params.deapSeed = 2

    start_gen = 5
    generations = 10

    filename = params.checkpointInputFilename(generations)

    os.chdir("../gp")

    # run for 10 generations to get data for comparison

    with open("../config.txt", 'w') as f:
        f.write("generations "+str(generations)+"\n")
        f.write("saveOutput True\n")
        f.write("saveCSV False\n")
        f.write("save_period 5")

    subprocess.call(["python3", "main.py", "--seed",  str(params.deapSeed)])

    with open(filename, "rb") as checkpoint_file:
        checkpoint = pickle.load(checkpoint_file)
    expected_population = checkpoint["population"]


    # run from 5 to 10 generations to get checkpoint data

    with open("../config.txt", 'w') as f:
        f.write("loadCheckpoint True\n")
        f.write("start_gen "+str(start_gen)+"\n")
        f.write("generations "+str(generations)+"\n")
        f.write("saveOutput True\n")
        f.write("saveCSV False")

    subprocess.call(["python3", "main.py", "--seed",  str(params.deapSeed)])

    with open(filename, "rb") as checkpoint_file:
        checkpoint = pickle.load(checkpoint_file)
    actual_population = checkpoint["population"]


    # get last two csv entries

    csvFilename = params.csvInputFilename(generations)
    f = open(csvFilename, "r")

    expected_csv = ""
    actual_csv = ""
    for line in f:
        if len(actual_csv) > 0:
            expected_csv = actual_csv
            actual_csv = ""
        items = line.split(",")
        for i in range(9, generations+10):
            actual_csv += items[i]+","


    # check results

    if expected_population == actual_population and expected_csv == actual_csv:
        print("passed")
    else:
        print("failed")


    # clear config file

    with open("../config.txt", 'w') as f:
        f.write("")
