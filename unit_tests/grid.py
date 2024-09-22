import sys
sys.path.insert(0, '..')

import subprocess
import pickle
import os

from params import eaParams

def checkGrids(description, indexes):

    params = eaParams()
    params.deapSeed = 1
    params.description = description
    params.indexes = indexes
    
    generations = 10

    os.chdir("../gp")

    path = params.path()


    # load expected sub-behaviour grids from pkl

    expected_grids = []
    for i in range(len(params.indexes)):
        filename = path+"expected-"+params.objectives[params.indexes[i]]+".pkl"
        with open(filename, "rb") as f:
            expected_grids.append(pickle.load(f))


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
        f.write("saveCSV False\n")

    subprocess.call(["python3", "main.py", "--seed",  str(params.deapSeed)])


    # load new sub-behaviour grids from pkl

    actual_grids = []
    for i in range(len(params.indexes)):
        filename = path+params.objectives[params.indexes[i]]+".pkl"
        with open(filename, "rb") as f:
            actual_grids.append(pickle.load(f))


    # check results

    passed = True
    for i in range(len(expected_grids)):
        for j in range(len(expected_grids[i])):
            if actual_grids[i][j] != expected_grids[i][j]:
                passed = False
                print(str(i)+", "+str(j))
                print(actual_grids[i][j])
                print()
                print(expected_grids[i][j])

    if passed:
        print("passed")
    else:
        print("failed")


    # clean up

    with open("../config.txt", 'w') as f:
        f.write("")



if __name__ == "__main__":
    checkGrids("test1-test2-test3", [0,1,2])
    checkGrids("testing", [0])
