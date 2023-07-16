"""

Draw box plots for a range of generations for one algorithm

"""

from analysis import Analysis
analyse = Analysis()



algorithms = {
	"deap1" : {
		"type" : "DEAP",
		"name" : "deap1",
		"categories" : ["EA1a", "EA1b", "EA1c"],
		"ylim" : [[0.5, 0.61], [0.6, 0.9], [0.7, 0.9]],
	},
	"deap3" : {
		"type" : "DEAP",
		"name" : "deap3",
		"categories" : ["EA2","EA2","EA2"],
		"ylim" : [[0.5, 0.61], [0.6, 0.9], [0.7, 0.9]],
	},
	"qdpy1" : {
		"type" : "QDPY",
		"name" : "qdpy1",
		"categories" : ["QD1a", "QD1b", "QD1c"],
		"ylim" : [[0.5, 0.6], [0.6, 0.9], [0.7, 0.9]],
	}
}

runs = 10
min_gen = 10
max_gen = 2000
increment = 20	
x_axis_increment = 5
objective_name = "food"

analyse.drawEvolution(analyse.algorithms["qdpy"], 
					  objective_name, 
					  runs, 
					  min_gen, 
					  max_gen, 
					  increment, 
					  x_axis_increment)






