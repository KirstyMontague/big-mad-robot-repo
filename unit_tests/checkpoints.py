import sys
sys.path.insert(0, '..')

import subprocess
import pickle
import os

from params import eaParams

def writeConfig(params):

    indexes_string = ""
    for index in params.indexes:
        indexes_string += str(index)+" "
    indexes_string = indexes_string[0:-1]

    with open("../config.txt", 'w') as f:
        f.write("description "+params.description+"\n")
        f.write("indexes "+indexes_string+"\n")
        f.write("features "+str(len(params.indexes))+"\n")
        f.write("tournamentSize "+str(len(params.indexes)+2)+"\n")
        f.write("populationSize "+str(len(params.indexes)*25)+"\n")
        f.write("generations "+str(params.generations)+"\n")
        f.write("saveOutput True\n")
        f.write("saveCSV True\n")

def checkCheckpoints(description, indexes):

    params = eaParams()
    params.deapSeed = 2
    params.description = description
    params.indexes = indexes

    params.start_gen = 5
    params.generations = 10

    filename = params.checkpointInputFilename(params.generations)

    os.chdir("../gp")


    # run for 10 generations to get data for comparison

    writeConfig(params)

    with open("../config.txt", 'a') as f:
        f.write("save_period 5\n")
        f.write("csv_save_period 5")

    subprocess.call(["python3", "main.py", "--seed",  str(params.deapSeed)], stdout=subprocess.DEVNULL)

    with open(filename, "rb") as checkpoint_file:
        checkpoint = pickle.load(checkpoint_file)
    expected_population = checkpoint["population"]


    # run from 5 to 10 generations to get checkpoint data

    writeConfig(params)

    with open("../config.txt", 'a') as f:
        f.write("loadCheckpoint True\n")
        f.write("start_gen "+str(params.start_gen)+"\n")
        f.write("csv_save_period 10")

    subprocess.call(["python3", "main.py", "--seed",  str(params.deapSeed)], stdout=subprocess.DEVNULL)

    with open(filename, "rb") as checkpoint_file:
        checkpoint = pickle.load(checkpoint_file)
    actual_population = checkpoint["population"]


    # get last two csv entries

    queries = ["best", "qd-scores", "coverage"]

    expected_csvs = {}
    actual_csvs = {}

    for query in queries:

        csvFilename = params.csvInputFilename(params.generations, query)
        f = open(csvFilename, "r")

        expected_csvs[query] = ""
        actual_csvs[query] = ""
        for line in f:
            if len(actual_csvs[query]) > 0:
                expected_csvs[query] = actual_csvs[query]
                actual_csvs[query] = ""
            items = line.split(",")
            for i in range(9, params.generations+10):
                actual_csvs[query] += items[i]+","


    # check results

    result = "passed"

    if expected_population != actual_population:
        result = "failed"
        print("expected_population != actual_population")

    for query in queries:
        if expected_csvs[query] != actual_csvs[query]:
            result = "failed"
            print("expected_csvs["+query+"] != actual_csvs["+query+"]")

    print(result)

    # clean up

    with open("../config.txt", 'w') as f:
        f.write("\n")

    for query in queries:

        if os.path.isfile(params.csvInputFilename(params.start_gen, query)):
            os.remove(params.csvInputFilename(params.start_gen, query))

        if os.path.isfile(params.csvInputFilename(params.generations, query)):
            os.remove(params.csvInputFilename(params.generations, query))


if __name__ == "__main__":
    checkCheckpoints("testing", [0])
    checkCheckpoints("test1-test2-test3", [0,1,2])
