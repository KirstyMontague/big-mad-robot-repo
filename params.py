import numpy
import os

"""

to switch between foraging and sub-behaviours/baseline:

indexes
generations, using_repertoire (baseline only)


to change repertoire

params.py - update repertoire_size and repertoire_type
archive.py - update archive path for re-running old experiments
update foraging results directory

"""

class eaParams():

    def __init__(self):

        self.characteristics = 3
        self.saveHeatmap = False
        self.start_point = "final"
        self.max_size = 1000000
        self.max_items_per_bin = 3
        self.nb_bins = [8,8,8]
        self.fitness_domain = [(0., numpy.inf)]
        self.verbose = False
        self.show_warnings = True
        self.printOffspring = False
        self.printContainer = False

        self.sqrtRobots = 3
        self.iterations = 5
        self.num_threads = 8

        self.indexes = [6]
        self.populationSize = 25

        self.start_gen   = 0
        self.generations = 100

        self.using_repertoire = True
        self.repertoire_type = "qd"
        self.bins_per_axis = 1

        self.readCheckpoint = False
        self.loadCheckpoint = False
        self.saveCheckpoint = False
        self.saveOutput = False
        self.saveCSV = False

        self.stop = False

        self.best_save_period = 10 # save best individual for each objective to current.txt

        self.objectives = ["density", "nest", "food", "idensity", "inest", "ifood", "foraging"]

        self.description = ""
        for index in self.indexes:
            self.description += self.objectives[index]+"-"
        self.description = self.description[0:-1]

        self.populationSize *= len(self.indexes)
        self.tournamentSize = 2 + len(self.indexes)
        self.features = len(self.indexes)
        self.repertoire_size = self.bins_per_axis ** self.characteristics

        self.save_period = 1000 # save checkpoint, check duplicates
        self.csv_save_period = 1000 # save csv, save archive
        self.csv_save_interval = 1
        if self.description == "foraging" and not self.using_repertoire:
            self.save_period = 2200
            self.csv_save_period = 2200

        if self.description != "foraging":
            self.using_repertoire = False
            self.features_domain = [(-40.0, 40.0), (-40.0, 40.0), (0.0, 1.0)]
        else:
            self.features_domain = [(-200.0, 200.0), (-200.0, 200.0), (0.0, 1.0)]

        self.printEliteScores = False
        self.printFitnessScores = False
        self.printBestIndividuals = False
        self.printAllIndividuals = False

        self.saveBestIndividuals = True
        self.saveAllIndividuals = True

        self.eaRunSleep = 1.0
        self.genSleep = 0.0
        self.evalSleep = 0.0
        self.trialSleep = 0.0

        # evaluation parameters for evolving and testing
        self.nest = 0.5
        self.arenaParams = [.5, .7]
        self.unseenIterations = 10
        self.unseenParams = [.3, .4, .5, .6, .7, .8, .9, 1.0]

        self.crossoverProbability = .8
        self.mutSRProbability = 0.05         # mutUniform
        self.mutSSProbability = 0.1          # mutShrink
        self.mutNRProbability = 0.5          # mutNodeReplacement

        # timesteps required to turn and move, and total timesteps available
        self.turn180 = 72
        self.forwards1m = 160
        self.totalSteps = 2400

        self.nodes = {}

        with open("../path.txt", "r") as f:
            for line in f:
                data = line.split(":")
                if data[0] == "host": self.host = data[1][0:-1]
                if data[0] == "local": self.local_path = self.host+"/"+data[1][0:-1]
                if data[0] == "shared": self.shared_path = self.host+"/"+data[1][0:-1]

        working_directory = os.getcwd()
        self.algorithm = working_directory.split("/")[-1]

    def csvInputFilename(self, gen, query): return self.shared_path+"/"+self.algorithm+"/"+self.description+"/"+query+""+str(gen)+".csv"
    def csvOutputFilename(self, gen, query): return self.shared_path+"/"+self.algorithm+"/"+self.description+"/"+query+""+str(gen)+".csv"

    def path(self): return self.shared_path+"/"+self.algorithm+"/"+self.description+"/"+str(self.deapSeed)+"/"
    def checkpointInputFilename(self, gen): return self.path() + "checkpoint-"+self.description+"-"+str(self.deapSeed)+"-"+str(gen)+".pkl"
    def checkpointOutputFilename(self, gen): return self.path() + "checkpoint-"+self.description+"-"+str(self.deapSeed)+"-"+str(gen)+".pkl"

    def input_filename(self): return self.path() + "seed"+str(self.deapSeed)+"-"+self.start_point+".p"
    def iteration_filename(self): return self.path() + "seed"+str(self.deapSeed)+"-iteration%i.p"
    def final_filename(self): return self.path() + "seed"+str(self.deapSeed)+"-final.p"

    def configure(self):
        with open(self.shared_path+"/config.txt", "r") as f:
            for line in f:
                data = line.split()
                if len(data) > 0:
                    for d in data:
                        print(d)
                    if data[0] == "description": self.description = data[1]
                    if data[0] == "indexes":
                        self.indexes = []
                        for i in range(1, len(data)):
                            self.indexes.append(int(data[i]))
                    if data[0] == "features": self.features = int(data[1])
                    if data[0] == "tournamentSize": self.tournamentSize = int(data[1])
                    if data[0] == "populationsSize": self.populationsSize = int(data[1])
                    if data[0] == "loadCheckpoint":  self.loadCheckpoint = False if data[1] == "False" else True
                    if data[0] == "runs": self.runs = int(data[1])
                    if data[0] == "start_gen": self.start_gen = int(data[1])
                    if data[0] == "generations": self.generations = int(data[1])
                    if data[0] == "genSleep": self.genSleep = float(data[1])
                    if data[0] == "evalSleep": self.evalSleep = float(data[1])
                    if data[0] == "trialSleep": self.trialSleep = float(data[1])
                    if data[0] == "printEliteScores": self.printEliteScores = False if data[1] == "False" else True
                    if data[0] == "printFitnessScores": self.printFitnessScores = False if data[1] == "False" else True
                    if data[0] == "printBestIndividuals": self.printBestIndividuals = False if data[1] == "False" else True
                    if data[0] == "saveOutput": self.saveOutput = False if data[1] == "False" else True
                    if data[0] == "saveCSV": self.saveCSV = False if data[1] == "False" else True
                    if data[0] == "save_period": self.save_period = int(data[1])
                    if data[0] == "csv_save_period": self.csv_save_period = int(data[1])
                    if data[0] == "best_save_period": self.best_save_period = int(data[1])
                    if data[0] == "stop":
                        if len(data) > 1 and data[1] == "False":
                            self.stop = False
                        else:
                            self.stop = True
                            self.saveCSV = False
                            self.generations = 0
                    if data[0] == "cancel":
                        self.stop = True
                        self.saveOutput = False
                        self.saveCSV = False
                        self.generations = 0

    def getRepertoireFilename(self):
        return self.shared_path+"/"+self.algorithm+"/"+self.description+"/sub-behaviours.txt"

    def getSubbehavioursFromFile(self):

        names = []

        filename = self.getRepertoireFilename()
        with open(filename, "r") as f:
            for line in f:
                first = line[0:line.find(" ")]
                names.append(first)

        return names

    def addNodes(self, pset):

        primitives = ["seqm", "selm", "probm"]

        if self.using_repertoire:
            conditions = ["ifGotFood", "ifOnFood", "ifInNest"]
            actions = ["increaseDensity", "gotoNest", "gotoFood", "reduceDensity", "goAwayFromNest", "goAwayFromFood"]
        else:
            if self.description == "foraging":
                conditions = ["ifGotFood", "ifOnFood", "ifInNest", "ifNestToLeft", "ifNestToRight", "ifFoodToLeft", "ifFoodToRight", "ifRobotToLeft", "ifRobotToRight"]
            else:
                conditions = ["ifOnFood", "ifInNest", "ifNestToLeft", "ifNestToRight", "ifFoodToLeft", "ifFoodToRight", "ifRobotToLeft", "ifRobotToRight"]
            actions = ["stop", "f", "fl", "fr", "r", "rl", "rr"]

        robot = robotObject()
        robot.makeCompositionNodes(primitives)
        robot.makeTerminalNodes("conditions", conditions)

        if self.using_repertoire:
            robot.makeRepertoireNodes(actions)
        else:
            robot.makeTerminalNodes("actions", actions)

        for i in range(3):
            self.nodes['selm'+str(i+2)] = True; pset.addPrimitive(robot.selm[i], i+2)
            self.nodes['seqm'+str(i+2)] = True; pset.addPrimitive(robot.seqm[i], i+2)
            self.nodes['probm'+str(i+2)] = True; pset.addPrimitive(robot.probm[i], i+2)

        for node in conditions:
            self.nodes[node] = True; pset.addCondition(robot.conditions[node])

        if self.using_repertoire:
            names = self.getSubbehavioursFromFile()
            for i in range(self.repertoire_size):
                index = str(i+1)
                if 'increaseDensity'+index in names:
                    self.nodes['increaseDensity'+index] = True
                    pset.addAction(robot.increaseDensity[i])
                if 'reduceDensity'+index in names:
                    self.nodes['reduceDensity'+index] = True
                    pset.addAction(robot.reduceDensity[i])
                if 'gotoNest'+index in names:
                    self.nodes['gotoNest'+index] = True
                    pset.addAction(robot.gotoNest[i])
                if 'goAwayFromNest'+index in names:
                    self.nodes['goAwayFromNest'+index] = True
                    pset.addAction(robot.goAwayFromNest[i])
                if 'gotoFood'+index in names:
                    self.nodes['gotoFood'+index] = True
                    pset.addAction(robot.gotoFood[i])
                if 'goAwayFromFood'+index in names:
                    self.nodes['goAwayFromFood'+index] = True
                    pset.addAction(robot.goAwayFromFood[i])

        else:
            for node in actions:
                pset.addAction(robot.actions[node])

    def addUnpackedNodes(self, pset):

        primitives = ["seqm", "selm", "probm"]
        conditions = ["ifGotFood", "ifOnFood", "ifInNest", "ifNestToLeft", "ifNestToRight", "ifFoodToLeft", "ifFoodToRight", "ifRobotToLeft", "ifRobotToRight"]
        actions = ["stop", "f", "fl", "fr", "r", "rl", "rr"]

        robot = robotObject()

        robot.makeCompositionNodes(primitives)
        robot.makeTerminalNodes("conditions", conditions)
        robot.makeTerminalNodes("actions", actions)

        for i in range(3):
            self.nodes['selm'+str(i+2)] = True; pset.addPrimitive(robot.selm[i], i+2)
            self.nodes['seqm'+str(i+2)] = True; pset.addPrimitive(robot.seqm[i], i+2)
            self.nodes['probm'+str(i+2)] = True; pset.addPrimitive(robot.probm[i], i+2)

        for node in conditions:
            pset.addCondition(robot.conditions[node])

        for node in actions:
            pset.addAction(robot.actions[node])

    def getNodes(self):
        return self.nodes

class robotObject(object):

    def successd(): pass

    def makeCompositionNodes(self, nodes):

        for name in (nodes):
            _list = []
            setattr(robotObject, name, _list)
            for i in range(2,5):
                n = name+str(i)
                _method = self.make_method(n)
                setattr(robotObject, n, _method)
                _list.append(_method)

    def makeTerminalNodes(self, role, nodes):

        _dict = {}

        for name in (nodes):
            _method = self.make_method(name)
            setattr(robotObject, name, _method)
            _dict[name] = _method

        setattr(robotObject, role, _dict)

    def makeRepertoireNodes(self, nodes):

        for name in (nodes):
            _list = []
            setattr(robotObject, name, _list)
            for i in range(64):
                n = name+str(i+1)
                _method = self.make_method(n)
                setattr(robotObject, n, _method)
                _list.append(_method)

    def make_method(self, name):
        def _method(self): pass
        _method.__name__ = name
        return _method
