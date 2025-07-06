
import pickle

from deap import creator

from analysis import Analysis
from redundancy import Redundancy

analyse = Analysis()
analyse.setupDeapToolbox()

redundancy = Redundancy()



bins = 1 # 1, 2 or 4
save = True



sub_behaviours = {"density" : "increaseDensity",
				  "nest" : "gotoNest",
				  "food" : "gotoFood",
				  "idensity" : "reduceDensity",
				  "inest" : "goAwayFromNest",
				  "ifood" : "goAwayFromFood"}
			
x = 0
y = 0
z = 0

suffix = bins * bins * bins

def getQdRepertoire():

	output_filename = "../repertoires/sub-behaviours-qd"+str(suffix)+"-1000gen.txt"
	print(output_filename)

	if save:
		with open(output_filename, 'w') as f:
			f.write("")

	for objective in sub_behaviours:

		containers = []

		for seed in range(1,31):
			
			input_filename = "../qdpy/results/"+objective+"/"+str(seed)+"/seed"+str(seed)+"-iteration1000.p"
			
			with open(input_filename, "rb") as f:
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
						# output += sub_behaviours[objective]+str(index)+" "+str(ind.fitness)
						# print (sub_behaviours[objective]+str(index)+" "+str(trimmed))
						# output += "\n"

						if save:
							with open(output_filename, 'a') as f:
								f.write(sub_behaviours[objective]+str(index)+" "+str(trimmed))
								f.write("\n")

						print (output)

					else:
						output += objective+str(index)+" not found"
						print(output)


sublists = [["food", "idensity", "inest"],
			["density", "nest", "ifood"]]

subsets = ["food-idensity-inest", "density-nest-ifood"]

def getMtRepertoire():

	output_filename = "../repertoires/sub-behaviours-mt"+str(suffix)+"-1000gen.txt"
	print(output_filename)

	if save:
		with open(output_filename, 'w') as f:
			f.write("")

	for combination in range(len(sublists)):

		subset = subsets[combination]
		sublist = sublists[combination]

		seeds = []

		for seed in range(1,31):

			input_filename = "../gp/results/"+subset+"/"+str(seed)+"/checkpoint-"+subset+"-"+str(seed)+"-1000.pkl"
			with open(input_filename, "rb") as f:
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
							# output += "\n"+str(ind.fitness)
							# output += "\n"
							print (output)

							if save:
								with open(output_filename, 'a') as f:
									f.write(sub_behaviours[objective]+str(index)+" "+str(trimmed))
									f.write("\n")

						else:
							output += sub_behaviours[objective]+str(index)
							output += " "+str(xa)+" "+str(yb)+" "+str(zc)
							output += " not found"



getMtRepertoire()
