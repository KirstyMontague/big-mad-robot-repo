from analysis import Analysis
import time

analyse = Analysis()


# convertDEAPtoGridWholeRun has hard coded hacks for different types of data - needs updated manually

algorithm = "density-nest-food-idensity-inest-ifood"
features = 6

objective_index = 3 # possibly meant to be 0 for single objective runs

seed = 1
start = 1
generations = 1000

path = "../Extended/test/"
# path = "../../AutoDecomposition/checkpoints/test/"

# analyse.convertDEAPtoGridWholeRun(algorithm, objective_index, seed, start, generations, features, path)
	
for i in range(2,11):
	analyse.convertDEAPtoGridWholeRun(algorithm, objective_index, i, start, generations, features, path)
	time.sleep(2.0)

