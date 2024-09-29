import sys
sys.path.insert(0, '..')

import subprocess
import pickle
import os

from params import eaParams

if __name__ == "__main__":

    params = eaParams()
    params.deapSeed = 2
    params.description = "testing"

    start_gen = 5
    generations = 10

    filename = params.checkpointInputFilename(generations)

    os.chdir("../gp")


    # run for 10 generations to get data for comparison

    with open("../config.txt", 'w') as f:
        f.write("description testing\n")
        f.write("generations "+str(generations)+"\n")
        f.write("saveOutput True\n")
        f.write("saveCSV True\n")
        f.write("save_period 5\n")
        f.write("csv_save_period 5")

    subprocess.call(["python3", "main.py", "--seed",  str(params.deapSeed)], stdout=subprocess.DEVNULL)

    with open(filename, "rb") as checkpoint_file:
        checkpoint = pickle.load(checkpoint_file)
    expected_population = checkpoint["population"]


    # run from 5 to 10 generations to get checkpoint data

    with open("../config.txt", 'w') as f:
        f.write("loadCheckpoint True\n")
        f.write("description testing\n")
        f.write("start_gen "+str(start_gen)+"\n")
        f.write("generations "+str(generations)+"\n")
        f.write("saveOutput True\n")
        f.write("saveCSV True\n")
        f.write("csv_save_period 10")

    subprocess.call(["python3", "main.py", "--seed",  str(params.deapSeed)], stdout=subprocess.DEVNULL)

    with open(filename, "rb") as checkpoint_file:
        checkpoint = pickle.load(checkpoint_file)
    actual_population = checkpoint["population"]


    # get last two csv entries

    csvFilename = params.csvInputFilename(generations, "best")
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

    result = "passed"

    if expected_population != actual_population:
        result = "failed"
        print("expected_population != actual_population")
    if expected_csv != actual_csv:
        result = "failed"
        print("expected_csv != actual_csv")

    print(result)

    # clean up

    with open("../config.txt", 'w') as f:
        f.write("")

    queries = ["best", "qd-scores", "coverage"]

    for query in queries:

        if os.path.isfile(params.csvInputFilename(start_gen, query)):
            os.remove(params.csvInputFilename(start_gen, query))

        if os.path.isfile(params.csvInputFilename(generations, query)):
            os.remove(params.csvInputFilename(generations, query))

