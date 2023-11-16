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

		for a in range(bins):
			
			xa = int(a*8/bins)
			
			for b in range(bins):
			
				yb = int(b*8/bins)
				
				for c in range(bins):
				
					zc = int(c*8/bins)
					
					index = a*4+b*2+c+1 # needs updated from constants to bins
					
					output = ""
					ind = analyse.getBestEverFromAxis(objective, xa, yb, zc, bins)
					
					output += "analyse.getBestEverFromAxis("+objective+", "+str(xa)+", "+str(yb)+", "+str(zc)+")\n"
					output += objective+str(index)+" was "
					output += str(len(ind)) + " now "
					
					trimmed = redundancy.removeRedundancy(str(ind))
					trimmed = [creator.Individual.from_string(trimmed, analyse.pset)][0]
					
					output += str(len(trimmed))+"\n"
					output += sub_behaviours[objective]+str(index)+" "+str(trimmed)+"\n"

					print (output)

					# with open('../txt/sub-behaviours.txt', 'a') as f:
						# f.write(sub_behaviours[objective]+str(index)+" "+str(trimmed))
						# f.write("\n")


# sublist = ["food", "idensity", "inest"]
# subset = "food-idensity-inest"

sublist = ["density", "nest", "ifood"]
subset = "density-nest-ifood"

def getMtRepertoire():

	for objective in sublist:

		for a in range(bins):

			xa = int(a*8/bins)

			for b in range(bins):

				yb = int(b*8/bins)

				for c in range(bins):

					zc = int(c*8/bins)

					index = a*4+b*2+c+1 # needs updated from constants to bins

					output = ""
					ind = analyse.getBestEverFromAxisMT(subset, objective, xa, yb, zc, bins)

					trimmed = redundancy.removeRedundancy(str(ind))
					trimmed = [creator.Individual.from_string(trimmed, analyse.pset)][0]

					output += sub_behaviours[objective]+str(index)+" "+str(trimmed)

					print (output)

					# with open('../txt/sub-behaviours.txt', 'a') as f:
						# f.write(sub_behaviours[objective]+str(index)+" "+str(trimmed))
						# f.write("\n")


getMtRepertoire()
