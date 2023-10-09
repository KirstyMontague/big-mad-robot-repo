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
			
objective = "ifood"

x = 0
y = 0
z = 0

# with open('../txt/sub-behaviours.txt', 'w') as f:
	# f.write("")

for a in range(2):
	
	xa = a*4
	
	for b in range(2):
	
		yb = b*4
		
		for c in range(2):
		
			zc = c*4
			
			index = a*4+b*2+c+1
			
			ind = analyse.getBestEverFromAxis(objective, xa, yb, zc)
			
			print()
			print("analyse.getBestEverFromAxis("+objective+", "+str(xa)+", "+str(yb)+", "+str(zc)+")")
			print(objective+str(index))
			print(len(ind))
			
			trimmed = redundancy.removeRedundancy(str(ind))
			trimmed = [creator.Individual.from_string(trimmed, analyse.pset)][0]
			
			print(len(trimmed))
			
			with open('../txt/sub-behaviours.txt', 'a') as f:
				f.write(sub_behaviours[objective]+str(index)+" "+str(trimmed))
				f.write("\n")


