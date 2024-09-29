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

    utilities = Utilities(params)

    generations = 50

    queries = ["best", "coverage", "qd-scores"]

    os.chdir("../qdpy")


    # load expected csv data

    expected_utilities = {}
    expected_logs = {}

    for query in queries:

        filename = params.path()+"expected-csvs/"+query+"-"+str(params.deapSeed)+".csv"
        f = open(filename, "r")

        expected_utilities[query] = []
        for line in f:
            items = line.split(",")
            if len(items) > 0:
                expected_utilities[query].append(float(items[1]))

        filename = "./test/"+description+"/expected-"+query+str(generations)+".csv"
        f = open(filename, "r")

        expected_logs[query] = []
        for line in f:
            items = line.split(",")
            if len(items) > 1 and items[2] != "Seed":
                for i in range(len(items)):
                    if i != 1:
                        expected_logs[query].append(str(items[i]))


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
        f.write("csv_save_period "+str(generations)+"\n")

    ret = subprocess.call(["python3", "main.py", "--seed",  str(params.deapSeed)], stdout=subprocess.DEVNULL)


    # load new csv data

    actual_utilities = {}
    actual_logs = {}

    for query in queries:

        filename = params.path()+"csvs/"+query+"-"+str(params.deapSeed)+".csv"
        f = open(filename, "r")

        actual_utilities[query] = []
        for line in f:
            items = line.split(",")
            if len(items) > 0:
                actual_utilities[query].append(float(items[1]))

        filename = "./test/"+description+"/"+query+str(generations)+".csv"
        f = open(filename, "r")

        actual_logs[query] = []
        for line in f:
            items = line.split(",")
            if len(items) > 1 and items[2] != "Seed":
                for i in range(len(items)):
                    if i != 1:
                        actual_logs[query].append(str(items[i]))


    # check results

    result_utilities = "utilities passed"
    result_logs = "logs passed"
    for query in queries:

        if expected_utilities[query] != actual_utilities[query]:
            result_utilities = "utilities failed"
            print(len(expected_utilities[query]))
            print(len(actual_utilities[query]))

        for i in range(len(expected_utilities[query])):
            if expected_utilities[query][i] != actual_utilities[query][i]:
                result_utilities = "utilities failed"
                print(i)
                print(expected_utilities[query][i])
                print(actual_utilities[query][i])

        if expected_logs[query] != actual_logs[query]:
            result_logs = "logs failed"
            print(len(expected_logs[query]))
            print(len(actual_logs[query]))

        for i in range(len(expected_utilities[query])):
            if expected_logs[query][i] != actual_logs[query][i]:
                result_logs = "logs failed"
                print(i)
                print(expected_logs[query][i])
                print(actual_logs[query][i])
    print(result_utilities)
    print(result_logs)
    print("")


    # clean up

    with open("../config.txt", 'w') as f:
        f.write("\n")

    for query in queries:
        if os.path.isfile(params.csvInputFilename(generations, query)):
            os.remove(params.csvInputFilename(generations, query))




def checkGPLogs(description, indexes):

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
    checkQDLogs("testing", [0])
    checkGPLogs("testing", [0])
    checkGPLogs("test1-test2-test3", [0,1,2])
