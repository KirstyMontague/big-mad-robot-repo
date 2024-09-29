import sys
sys.path.insert(0, '..')

import subprocess
import os

from params import eaParams
from utilities import Utilities

def checkLogs(description, indexes):

    params = eaParams()
    params.deapSeed = 2
    params.description = description
    params.indexes = indexes
    
    utilities = Utilities(params)

    generations = 50

    queries = ["best", "coverage", "qd-scores"]

    os.chdir("../gp")


    # load expected csv data

    expected = {}

    for query in queries:

        filename = "./test/"+description+"/expected-"+query+str(generations)+".csv"
        f = open(filename, "r")

        expected[query] = []
        for line in f:
            items = line.split(",")
            if len(items) > 1 and items[2] != "Seed":
                for i in range(len(items)):
                    if i != 1:
                        expected[query].append(str(items[i]))

    # run EA

    indexes_string = ""
    for index in indexes:
        indexes_string += str(index)+" "
    indexes_string = indexes_string[0:-1]

    with open("../config.txt", 'w') as f:
        f.write("description "+description+"\n")
        f.write("indexes "+indexes_string+"\n")
        f.write("features "+str(len(indexes))+"\n")
        f.write("tournamentSize "+str(len(indexes)+2)+"\n")
        f.write("populationSize "+str(len(indexes)*25)+"\n")
        f.write("generations "+str(generations)+"\n")
        f.write("saveOutput True\n")
        f.write("saveCSV True\n")
        f.write("csv_save_period 50\n")

    ret = subprocess.call(["python3", "main.py", "--seed",  str(params.deapSeed)], stdout=subprocess.DEVNULL)


    # load new csv data

    actual = {}

    for query in queries:

        filename = "./test/"+description+"/"+query+str(generations)+".csv"
        f = open(filename, "r")

        actual[query] = []
        for line in f:
            items = line.split(",")
            if len(items) > 1 and items[2] != "Seed":
                for i in range(len(items)):
                    if i != 1:
                        actual[query].append(str(items[i]))


    # check results

    for query in queries:
        
        result = query+" passed"

        if expected[query] != actual[query]:
            result = query+" failed"
            print("expected size "+str(len(expected[query])))
            print("actual size "+str(len(actual[query])))
    
        for i in range(len(expected[query])):
            if len(actual[query]) < i:
                result = result = query+" failed"
                print("actual results smaller than expected results ("+str(i)+")")
                break
            elif expected[query][i] != actual[query][i]:
                result = query+" failed"
                print(i)
                print(expected[query][i])
                print(actual[query][i])
                break
        
        print(result)
        print("")


    # clean up

    with open("../config.txt", 'w') as f:
        f.write("\n")

    for query in queries:
        if os.path.isfile(params.csvInputFilename(generations, query)):
            os.remove(params.csvInputFilename(generations, query))


if __name__ == "__main__":
    checkLogs("testing", [0])
    checkLogs("test1-test2-test3", [0,1,2])
