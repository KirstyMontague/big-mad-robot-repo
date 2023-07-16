import matplotlib.pyplot as plt
import statistics

from analysis import Analysis
analyse = Analysis()


y = {
	"density" : {
		"best" : [0.5,0.61],
		"qd-score" : [0.0,0.35],
		"coverage" : [0.0,0.65],
	},
	"nest" : {
		"best" : [0.6,0.9],
		"qd-score" : [0.0,0.45],
		"coverage" : [0.0,0.65],
	},
	"food" : {
		"best" : [0.75,0.88],
		"qd-score" : [0.0,0.5],
		"coverage" : [0.0,0.65],
	},
}


objective = "density"
query = "best"
runs = 10
generations = 2000

analyse.drawLineGraphFromQdpy(analyse.objectives_info[objective], analyse.queries[query], generations, runs, y[objective][query])
# analyse.drawLineGraphFromDeap(analyse.objectives_info[objective], analyse.queries[query], generations, runs, y[objective][query])
# analyse.drawLineGraphFromMT(analyse.objectives_info[objective], analyse.queries[query], generations, runs, y[objective][query])
