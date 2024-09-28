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

    os.chdir("../gp")


    # load expected csv data

    expected = ""
    filename = "./test/"+description+"/expected-checkpoint"+str(generations)+".csv"
    f = open(filename, "r")

    for line in f:
        items = line.split(",")
        if len(items) > 1 and items[2] != "Seed":
            output = ""
            for i in range(len(items)):
                if i != 1:
                    expected += items[i]+","


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

    actual = ""
    filename = "./test/"+description+"/checkpoint"+str(generations)+".csv"
    f = open(filename, "r")

    for line in f:
        items = line.split(",")
        if len(items) > 1 and items[2] != "Seed":
            output = ""
            for i in range(len(items)):
                if i != 1:
                    actual += items[i]+","


    # check results

    if expected == actual:
        print("passed")
    else:
        print("failed")


    # clean up

    with open("../config.txt", 'w') as f:
        f.write("\n")

    if os.path.isfile(filename):
        os.remove(filename)


if __name__ == "__main__":
    checkLogs("testing", [0])
    checkLogs("test1-test2-test3", [0,1,2])
