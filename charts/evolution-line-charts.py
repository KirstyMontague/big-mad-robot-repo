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
runs = 30
generations = 1000

analyse.drawLineGraph(analyse.objectives.info[objective], "qdpy", "qdpy_url", analyse.queries.info[query], generations, runs, y[objective][query])
analyse.drawLineGraph(analyse.objectives.info[objective], "gp", "gp_url", analyse.queries.info[query], generations, runs, y[objective][query])
analyse.drawLineGraph(analyse.objectives.info[objective], "mtc", "mtc_url", analyse.queries.info[query], generations, runs, y[objective][query])
analyse.drawLineGraph(analyse.objectives.info[objective], "mti", "mti_url", analyse.queries.info[query], generations, runs, y[objective][query])
