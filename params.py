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
		
	def csvInputFilename(self, gen): return "test/"+self.description+"/checkpoint"+str(gen)+".csv"
	def csvOutputFilename(self, gen): return "test/"+self.description+"/checkpoint"+str(gen)+".csv"
	
	def path(self): return "test/"+self.description+"/"+str(self.deapSeed)+"/"
	def checkpointInputFilename(self, gen): return self.path() + "checkpoint-"+self.description+"-"+str(self.deapSeed)+"-"+str(gen)+".pkl"
	def checkpointOutputFilename(self, gen): return self.path() + "checkpoint-"+self.description+"-"+str(self.deapSeed)+"-"+str(gen)+".pkl"

	printEliteScores = False
	printFitnessScores = False
	printBestIndividuals = False

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
				if data[0] == "stop": self.stop = False if data[1] == "False" else True
		

	def addNodes(self, pset):
		
		robot = robotObject()

		self.nodes['selm2'] = True; pset.addPrimitive(robot.selm2, 2)
		self.nodes['seqm2'] = True; pset.addPrimitive(robot.seqm2, 2)
		self.nodes['probm2'] = True; pset.addPrimitive(robot.probm2, 2)
		self.nodes['selm3'] = True; pset.addPrimitive(robot.selm3, 3)
		self.nodes['seqm3'] = True; pset.addPrimitive(robot.seqm3, 3)
		self.nodes['probm3'] = True; pset.addPrimitive(robot.probm3, 3)
		self.nodes['selm4'] = True; pset.addPrimitive(robot.selm4, 4)
		self.nodes['seqm4'] = True; pset.addPrimitive(robot.seqm4, 4)
		self.nodes['probm4'] = True; pset.addPrimitive(robot.probm4, 4)

		self.nodes['ifOnFood'] = True; pset.addTerminal(robot.ifOnFood) # carrying food bug
		self.nodes['ifGotFood'] = True; pset.addTerminal(robot.ifGotFood)
		self.nodes['ifInNest'] = True; pset.addTerminal(robot.ifInNest)
		self.nodes['ifNestToLeft'] = True; pset.addTerminal(robot.ifNestToLeft)
		self.nodes['ifNestToRight'] = True; pset.addTerminal(robot.ifNestToRight)
		self.nodes['ifFoodToLeft'] = True; pset.addTerminal(robot.ifFoodToLeft)
		self.nodes['ifFoodToRight'] = True; pset.addTerminal(robot.ifFoodToRight)
		self.nodes['ifRobotToLeft'] = True; pset.addTerminal(robot.ifRobotToLeft)
		self.nodes['ifRobotToRight'] = True; pset.addTerminal(robot.ifRobotToRight)

		# self.nodes['stop'] = True; pset.addTerminal(robot.stop)
		# self.nodes['f'] = True; pset.addTerminal(robot.f)
		# self.nodes['fl'] = True; pset.addTerminal(robot.fl)
		# self.nodes['fr'] = True; pset.addTerminal(robot.fr)
		# self.nodes['r'] = True; pset.addTerminal(robot.r)
		# self.nodes['rl'] = True; pset.addTerminal(robot.rl)
		# self.nodes['rr'] = True; pset.addTerminal(robot.rr)
		
		for i in range(8):
			index = str(i+1)
			self.nodes['increaseDensity'+index] = True; pset.addTerminal(robot.increaseDensity[i])
			self.nodes['reduceDensity'+index] = True; pset.addTerminal(robot.reduceDensity[i])
			self.nodes['gotoNest'+index] = True; pset.addTerminal(robot.gotoNest[i])
			self.nodes['goAwayFromNest'+index] = True; pset.addTerminal(robot.goAwayFromNest[i])
			self.nodes['gotoFood'+index] = True; pset.addTerminal(robot.gotoFood[i])
			self.nodes['goAwayFromFood'+index] = True; pset.addTerminal(robot.goAwayFromFood[i])

	def addUnpackedNodes(self, pset):
		
		robot = robotObject()

		self.nodes['selm2'] = True; pset.addPrimitive(robot.selm2, 2)
		self.nodes['seqm2'] = True; pset.addPrimitive(robot.seqm2, 2)
		self.nodes['probm2'] = True; pset.addPrimitive(robot.probm2, 2)
		self.nodes['selm3'] = True; pset.addPrimitive(robot.selm3, 3)
		self.nodes['seqm3'] = True; pset.addPrimitive(robot.seqm3, 3)
		self.nodes['probm3'] = True; pset.addPrimitive(robot.probm3, 3)
		self.nodes['selm4'] = True; pset.addPrimitive(robot.selm4, 4)
		self.nodes['seqm4'] = True; pset.addPrimitive(robot.seqm4, 4)
		self.nodes['probm4'] = True; pset.addPrimitive(robot.probm4, 4)

		self.nodes['ifOnFood'] = True; pset.addTerminal(robot.ifOnFood) # carrying food bug
		self.nodes['ifGotFood'] = True; pset.addTerminal(robot.ifGotFood)
		self.nodes['ifInNest'] = True; pset.addTerminal(robot.ifInNest)
		self.nodes['ifNestToLeft'] = True; pset.addTerminal(robot.ifNestToLeft)
		self.nodes['ifNestToRight'] = True; pset.addTerminal(robot.ifNestToRight)
		self.nodes['ifFoodToLeft'] = True; pset.addTerminal(robot.ifFoodToLeft)
		self.nodes['ifFoodToRight'] = True; pset.addTerminal(robot.ifFoodToRight)
		self.nodes['ifRobotToLeft'] = True; pset.addTerminal(robot.ifRobotToLeft)
		self.nodes['ifRobotToRight'] = True; pset.addTerminal(robot.ifRobotToRight)

		self.nodes['stop'] = True; pset.addTerminal(robot.stop)
		self.nodes['f'] = True; pset.addTerminal(robot.f)
		self.nodes['fl'] = True; pset.addTerminal(robot.fl)
		self.nodes['fr'] = True; pset.addTerminal(robot.fr)
		self.nodes['r'] = True; pset.addTerminal(robot.r)
		self.nodes['rl'] = True; pset.addTerminal(robot.rl)
		self.nodes['rr'] = True; pset.addTerminal(robot.rr)
		
	def getNodes(self):
		return self.nodes

class robotObject(object):

	def action(): print ("")
	def seqm2(one, two): print ("")
	def selm2(one, two): print ("")
	def probm2(one, two): print ("")
	def seqm3(one, two): print ("")
	def selm3(one, two): print ("")
	def probm3(one, two): print ("")
	def seqm4(one, two): print ("")
	def selm4(one, two): print ("")
	def probm4(one, two): print ("")
	def successl(): print ("")
	def failurel(): print ("")
	def repeat(): print ("")
	def successd(): print ("")
	def failured(): print ("")
	def ifGotFood(): print ("")
	def ifOnFood(): print ("")
	def ifInNest(): print ("")
	def ifNestToLeft(): print ("")
	def ifNestToRight(): print ("")
	def ifFoodToLeft(): print ("")
	def ifFoodToRight(): print ("")
	def ifRobotToLeft(): print ("")
	def ifRobotToRight(): print ("")
	def set(): print ("")
	def stop(): print ("")
	def f(): print ("")
	def fl(): print ("")
	def fr(): print ("")
	def r(): print ("")
	def rl(): print ("")
	def rr(): print ("")
	def dummy(): print ("")
	
	def increaseDensity1(): print ("")
	def increaseDensity2(): print ("")
	def increaseDensity3(): print ("")
	def increaseDensity4(): print ("")
	def increaseDensity5(): print ("")
	def increaseDensity6(): print ("")
	def increaseDensity7(): print ("")
	def increaseDensity8(): print ("")
	increaseDensity = [increaseDensity1,
					   increaseDensity2,
					   increaseDensity3,
					   increaseDensity4,
					   increaseDensity5,
					   increaseDensity6,
					   increaseDensity7,
					   increaseDensity8]
	
	def reduceDensity1(): print ("")
	def reduceDensity2(): print ("")
	def reduceDensity3(): print ("")
	def reduceDensity4(): print ("")
	def reduceDensity5(): print ("")
	def reduceDensity6(): print ("")
	def reduceDensity7(): print ("")
	def reduceDensity8(): print ("")
	reduceDensity = [reduceDensity1,
					 reduceDensity2,
					 reduceDensity3,
					 reduceDensity4,
					 reduceDensity5,
					 reduceDensity6,
					 reduceDensity7,
					 reduceDensity8]
	
	def gotoNest1(): print ("")
	def gotoNest2(): print ("")
	def gotoNest3(): print ("")
	def gotoNest4(): print ("")
	def gotoNest5(): print ("")
	def gotoNest6(): print ("")
	def gotoNest7(): print ("")
	def gotoNest8(): print ("")
	gotoNest = [gotoNest1,
				gotoNest2,
				gotoNest3,
				gotoNest4,
				gotoNest5,
				gotoNest6,
				gotoNest7,
				gotoNest8]
	
	def goAwayFromNest1(): print ("")
	def goAwayFromNest2(): print ("")
	def goAwayFromNest3(): print ("")
	def goAwayFromNest4(): print ("")
	def goAwayFromNest5(): print ("")
	def goAwayFromNest6(): print ("")
	def goAwayFromNest7(): print ("")
	def goAwayFromNest8(): print ("")
	goAwayFromNest = [goAwayFromNest1,
					  goAwayFromNest2,
					  goAwayFromNest3,
					  goAwayFromNest4,
					  goAwayFromNest5,
					  goAwayFromNest6,
					  goAwayFromNest7,
					  goAwayFromNest8]
	
	def gotoFood1(): print ("")
	def gotoFood2(): print ("")
	def gotoFood3(): print ("")
	def gotoFood4(): print ("")
	def gotoFood5(): print ("")
	def gotoFood6(): print ("")
	def gotoFood7(): print ("")
	def gotoFood8(): print ("")
	gotoFood = [gotoFood1,
				gotoFood2,
				gotoFood3,
				gotoFood4,
				gotoFood5,
				gotoFood6,
				gotoFood7,
				gotoFood8]

	def goAwayFromFood1(): print ("")
	def goAwayFromFood2(): print ("")
	def goAwayFromFood3(): print ("")
	def goAwayFromFood4(): print ("")
	def goAwayFromFood5(): print ("")
	def goAwayFromFood6(): print ("")
	def goAwayFromFood7(): print ("")
	def goAwayFromFood8(): print ("")
	goAwayFromFood = [goAwayFromFood1,
					  goAwayFromFood2,
					  goAwayFromFood3,
					  goAwayFromFood4,
					  goAwayFromFood5,
					  goAwayFromFood6,
					  goAwayFromFood7,
					  goAwayFromFood8]
	
	

class bbReadIndex(): x = 1
class bbWriteIndex(): x = 1
class bbConstant(): x = 1
class repetitionsConstant(): x = 1
