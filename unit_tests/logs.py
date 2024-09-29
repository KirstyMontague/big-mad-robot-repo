
import sys
sys.path.insert(0, '..')

import subprocess
import os

from params import eaParams
from utilities import Utilities

def checkQDLogs(description, indexes):

    params = eaParams()
    params.deapSeed = 2
    params.description = description
    params.indexes = indexes
    params.generations = 50

    utilities = Utilities(params)


    queries = ["best", "coverage", "qd-scores"]

    os.chdir("../qdpy")


    # load expected csv data

    expected_utilities = {}
    expected_logs = loadLogsData(queries, description, params.generations, "expected-")

    for query in queries:

        filename = params.path()+"expected-csvs/"+query+"-"+str(params.deapSeed)+".csv"
        f = open(filename, "r")

        expected_utilities[query] = []
        for line in f:
            items = line.split(",")
            if len(items) > 0:
                expected_utilities[query].append(float(items[1]))


    # run EA

    runEA(params)


    # load new csv data

    actual_utilities = {}
    actual_logs = loadLogsData(queries, description, params.generations, "")

    for query in queries:

        filename = params.path()+"csvs/"+query+"-"+str(params.deapSeed)+".csv"
        f = open(filename, "r")

        actual_utilities[query] = []
        for line in f:
            items = line.split(",")
            if len(items) > 0:
                actual_utilities[query].append(float(items[1]))


    # check results

    checkLogResults(queries, expected_logs, actual_logs)

    for query in queries:

        result_utilities = query+" passed (utilities)"
        if expected_utilities[query] != actual_utilities[query]:
            result_utilities = query+" failed (utilities)"
            print(len(expected_utilities[query]))
            print(len(actual_utilities[query]))

        for i in range(len(expected_utilities[query])):
            if expected_utilities[query][i] != actual_utilities[query][i]:
                result_utilities = query+" failed (utilities)"
                print(i)
                print(expected_utilities[query][i])
                print(actual_utilities[query][i])

        print(result_utilities)
    print("")


    # clean up

    cleanUp(queries, params)



def checkGPLogs(description, indexes):

    params = eaParams()
    params.deapSeed = 2
    params.description = description
    params.indexes = indexes
    params.generations = 50

    utilities = Utilities(params)

    queries = ["best", "coverage", "qd-scores"]

    os.chdir("../gp")

    expected = loadLogsData(queries, description, params.generations, "expected-")
    runEA(params)
    actual = loadLogsData(queries, description, params.generations, "")
    checkLogResults(queries, expected, actual)
    cleanUp(queries, params)



def runEA(params):

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
        f.write("csv_save_period 50\n")

    ret = subprocess.call(["python3", "main.py", "--seed",  str(params.deapSeed)], stdout=subprocess.DEVNULL)


def loadLogsData(queries, description, generations, file_prefix):
    
    csv_data = {}

    for query in queries:

        filename = "./test/"+description+"/"+file_prefix+query+str(generations)+".csv"
        f = open(filename, "r")

        csv_data[query] = []
        for line in f:
            items = line.split(",")
            if len(items) > 1 and items[2] != "Seed":
                for i in range(len(items)):
                    if i != 1:
                        csv_data[query].append(str(items[i]))

    return csv_data

def checkLogResults(queries, expected, actual):
    
    for query in queries:
        
        result = query+" passed (logs)"

        if expected[query] != actual[query]:
            result = query+" failed (logs)"
            print("expected size "+str(len(expected[query])))
            print("actual size "+str(len(actual[query])))
    
        for i in range(len(expected[query])):
            if len(actual[query]) < i:
                result = result = query+" failed (logs)"
                print("actual results smaller than expected results (in logs on index "+str(i)+")")
                break
            elif expected[query][i] != actual[query][i]:
                result = query+" failed (logs)"
                print(i)
                print(expected[query][i])
                print(actual[query][i])
                break
        
        print(result)
    print("")

def cleanUp(queries, params):

    with open("../config.txt", 'w') as f:
        f.write("\n")

    for query in queries:
        if os.path.isfile(params.csvInputFilename(params.generations, query)):
            os.remove(params.csvInputFilename(params.generations, query))


if __name__ == "__main__":
    checkQDLogs("testing", [0])
    checkGPLogs("testing", [0])
    checkGPLogs("test1-test2-test3", [0,1,2])
