import numpy
# import random


class eaParams():
	
	init_batch_size = 25
	batch_size = 25
	characteristics = 3
	saveHeatmap = False
	start_point = "final"
	fitness_grid = False # QD2
	max_size = 1000000
	max_items_per_bin = 9 if fitness_grid else 3	
	nb_bins = [48,40,40] if fitness_grid else [8,8,8]
	features_domain = [(0.2, 0.8), (0.0, 1.0), (0.0, 1.0)] if fitness_grid else [(-40.0, 40.0), (-40.0, 40.0), (0.0, 1.0)]	
	fitness_domain = [(0., numpy.inf)] if not fitness_grid or features == 1 else [(0.0,1.0),(0.0,1.0),(0.0,1.0)]
	verbose = False
	show_warnings = True
	printOffspring = False
	printContainer = False
	def input_filename(self): return self.path()+"seed"+str(self.deapSeed)+"-"+self.start_point+".p"
	def iteration_filename(self): return self.path()+"seed"+str(self.deapSeed)+"-iteration%i.p"
	def final_filename(self): return self.path()+"seed"+str(self.deapSeed)+"-final.p"


	sqrtRobots = 3
	iterations = 5
	
	populationSize = 25 # EA2
	tournamentSize = 3 # EA2
	features = 1 # EA2

	is_qdpy = False # QD2 # QD1
	
	# description = "density-nest-food-idensity-inest-ifood" # EA2 # EA1
	description = "foraging" # EA2 # EA1
	indexes = [6]
	
	stop = False
	
	start_gen = 0
	generations = 500
	
	readCheckpoint = False
	loadCheckpoint = False
	saveOutput = True
	saveCSV = True
	
	save_period = 100
	csv_save_period = 100
	best_save_period = 10
		
	def csvInputFilename(self, gen): return "test/"+self.description+"/checkpoint"+str(gen)+".csv"
	def csvOutputFilename(self, gen): return "test/"+self.description+"/checkpoint"+str(gen)+".csv"
	
	def path(self): return "test/"+self.description+"/"+str(self.deapSeed)+"/"
	def checkpointInputFilename(self, gen): return self.path() + "checkpoint-"+self.description+"-"+str(self.deapSeed)+"-"+str(gen)+".pkl"
	def checkpointOutputFilename(self, gen): return self.path() + "checkpoint-"+self.description+"-"+str(self.deapSeed)+"-"+str(gen)+".pkl"

	printEliteScores = False
	printFitnessScores = False
	printBestIndividuals = False
	printAllIndividuals = False

	saveBestIndividuals = True
	saveAllIndividuals = True

	eaRunSleep = 1.0
	genSleep = 0.0
	evalSleep = 0.0
	trialSleep = 0.0
	
	# evaluation parameters for evolving and testing
	arenaParams = [.5, .7]
	unseenIterations = 10
	unseenParams = [.3, .4, .5, .6, .7, .8, .9, 1.0]

	crossoverProbability = .8
	mutSRProbability = 0.05 		# mutUniform
	mutSSProbability = 0.1  		# mutShrink
	mutNRProbability = 0.5  		# mutNodeReplacement

	# timesteps required to turn and move, and total timesteps available
	turn180 = 72
	forwards1m = 160
	totalSteps = 2400
	
	nodes = {}
	
	def __init__(self):
		self.nodes = {}
	
	def configure(self):
		f = open("../config.txt", "r")
		for line in f:
			data = line.split()
			if len(data) > 0:
				print (data[0])
				print (data[1])
				if data[0] == "runs": self.runs = int(data[1])
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
				if data[0] == "stop": self.stop = False if data[1] == "False" else True
		

	def addNodes(self, pset):
		
		primitives = ["seqm", "selm", "probm"]
		conditions = ["ifGotFood", "ifOnFood", "ifInNest", "ifNestToLeft", "ifNestToRight", "ifFoodToLeft", "ifFoodToRight", "ifRobotToLeft", "ifRobotToRight"]
		actions = ["increaseDensity", "gotoNest", "gotoFood", "reduceDensity", "goAwayFromNest", "goAwayFromFood"]
		
		robot = robotObject()
		robot.makeCompositionNodes(primitives)
		robot.makeTerminalNodes("conditions", conditions)
		robot.makeRepertoireNodes(actions)
		
		for i in range(3):
			self.nodes['selm'+str(i+2)] = True; pset.addPrimitive(robot.selm[i], i+2)
			self.nodes['seqm'+str(i+2)] = True; pset.addPrimitive(robot.seqm[i], i+2)
			self.nodes['probm'+str(i+2)] = True; pset.addPrimitive(robot.probm[i], i+2)
		
		for node in conditions:
			self.nodes[node] = True; pset.addCondition(robot.conditions[node])

		for i in range(1):
			index = str(i+1)
			self.nodes['increaseDensity'+index] = True; pset.addAction(robot.increaseDensity[i])
			self.nodes['reduceDensity'+index] = True; pset.addAction(robot.reduceDensity[i])
			self.nodes['gotoNest'+index] = True; pset.addAction(robot.gotoNest[i])
			self.nodes['goAwayFromNest'+index] = True; pset.addAction(robot.goAwayFromNest[i])
			self.nodes['gotoFood'+index] = True; pset.addAction(robot.gotoFood[i])
			self.nodes['goAwayFromFood'+index] = True; pset.addAction(robot.goAwayFromFood[i])

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
			for i in range(8):
				n = name+str(i+1)
				_method = self.make_method(n)
				setattr(robotObject, n, _method)
				_list.append(_method)

	def make_method(self, name):
		def _method(self): pass
		_method.__name__ = name
		return _method
