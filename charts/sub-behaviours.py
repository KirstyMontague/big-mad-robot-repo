
import pickle

from deap import creator

from analysis import Analysis
from redundancy import Redundancy

analyse = Analysis()
analyse.setupDeapToolbox()

redundancy = Redundancy()






sub_behaviours = {"density" : "increaseDensity",
				  "nest" : "gotoNest",
				  "food" : "gotoFood",
				  "idensity" : "reduceDensity",
				  "inest" : "goAwayFromNest",
				  "ifood" : "goAwayFromFood"}
			
x = 0
y = 0
z = 0
bins = 2

# with open('../txt/sub-behaviours.txt', 'w') as f:
	# f.write("")

def getQdRepertoire():

	for objective in sub_behaviours:

		containers = []

		for seed in range(1,31):
			
			filename = "../qdpy/results/"+objective+"/"+str(seed)+"/seed"+str(seed)+"-iteration1000.p"
			
			with open(filename, "rb") as f:
				data = pickle.load(f)
			
			for i in data:
				if str(i) == "container":
					container = data[i]

			containers.append(container)
		
		for a in range(bins):
			
			xa = int(a*8/bins)
		
			for b in range(bins):
		
				yb = int(b*8/bins)
				
				for c in range(bins):
			
					zc = int(c*8/bins)
				
					index = a*bins*bins + b*bins + c + 1
				
					output = ""
					ind = analyse.getBestEverFromSubset(containers, objective, xa, yb, zc, bins)
			
					# output += "analyse.getBestEverFromSubset("+objective+", "+str(xa)+", "+str(yb)+", "+str(zc)+")\n"

					if ind is not None:
						trimmed = redundancy.removeRedundancy(str(ind))
						trimmed = [creator.Individual.from_string(trimmed, analyse.pset)][0]

						output += sub_behaviours[objective]+str(index)
						# output += " was "+str(len(ind)) + " now "
						# output += str(len(trimmed))+"\n"
						output += " "+str(trimmed)
						# output += sub_behaviours[objective]+str(index)+" "+str(trimmed)+"\n"
						# print (sub_behaviours[objective]+str(index)+" "+str(ind.fitness))
						# print (sub_behaviours[objective]+str(index)+" "+str(trimmed))
						print (output)
					else:
						output += objective+str(index)+" not found"

					# with open('../txt/sub-behaviours.txt', 'a') as f:
						# f.write(sub_behaviours[objective]+str(index)+" "+str(trimmed))
						# f.write("\n")


# sublist = ["food", "idensity", "inest"]
# subset = "food-idensity-inest"

sublist = ["density", "nest", "ifood"]
subset = "density-nest-ifood"

def getMtRepertoire():

	seeds = []

	for seed in range(1,31):

		filename = "../gp/results/"+subset+"/"+str(seed)+"/checkpoint-"+subset+"-"+str(seed)+"-1000.pkl"
		with open(filename, "rb") as f:
			checkpoint = pickle.load(f)

		seeds.append(checkpoint["containers"])

	containers = {}
	for objective in range(0,3):
		containers[sublist[objective]] = []
		for seed in range(0,30):
			container = seeds[seed][objective]
			containers[sublist[objective]].append(container)


	for objective in sublist:

		for a in range(bins):

			xa = int(a*8/bins)

			for b in range(bins):

				yb = int(b*8/bins)

				for c in range(bins):

					zc = int(c*8/bins)

					index = a*bins*bins + b*bins + c + 1

					output = ""
					ind = analyse.getBestEverFromSubset(containers[objective], objective, xa, yb, zc, bins)

					if ind is not None:

						trimmed = redundancy.removeRedundancy(str(ind))
						trimmed = [creator.Individual.from_string(trimmed, analyse.pset)][0]

						output += sub_behaviours[objective]+str(index)
						# output += " "+str(xa)+" "+str(yb)+" "+str(zc)
						output += " "+str(trimmed)
						# output += " "+str(len(trimmed))
						# output += " "+str(ind.fitness)
						print (output)

					else:
						output += sub_behaviours[objective]+str(index)
						output += " "+str(xa)+" "+str(yb)+" "+str(zc)
						output += " not found"

					# with open('../txt/sub-behaviours.txt', 'a') as f:
						# f.write(sub_behaviours[objective]+str(index)+" "+str(trimmed))
						# f.write("\n")


getMtRepertoire()
