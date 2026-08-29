
class Queries():

    def __init__(self):

        self.info = {
            "best" : {
                "name" : "best",
                "description" : "best individuals",
                "ylabel" : "Best fitness",
                "index" : 1,
                "ylim" : [[0.54, 0.61], [0.65, 0.95], [0.875, 0.96], [0.525, 0.545], [0.75, 0.9], [0.68, 0.82], [0.0, 2.0]], # cma-es hidden nodes
                "ylim" : [[0.56, 0.61], [0.70, 0.90], [0.875, 0.96], [0.525, 0.54], [0.73, 0.88], [0.70, 0.82], [0.0, 2.0]], # cma-es algorithms
                "ylim" : [[0.00, 0.00], [0.00, 0.00], [0.00, 0.00], [0.00, 0.00], [0.00, 0.00], [0.00, 0.00], [0.0, 3.0]], # straight to foraging baseline
                "ylim" : [[0.00, 0.00], [0.00, 0.00], [0.00, 0.00], [0.00, 0.00], [0.00, 0.00], [0.00, 0.00], [0.0, 2.5]], # straight to foraging repertoire generation
                "ylim" : [[0.00, 0.00], [0.00, 0.00], [0.00, 0.00], [0.00, 0.00], [0.00, 0.00], [0.00, 0.00], [0.0, 2.2]], # heterogeneous GA from 150cm comms
                "ylim" : [[0.00, 0.00], [0.00, 0.00], [0.00, 0.00], [0.00, 0.00], [0.00, 0.00], [0.00, 0.00], [0.0, 4.0]], # heterogeneous GA from 200cm comms
                "ylim" : [[0.00, 0.00], [0.00, 0.00], [0.00, 0.00], [0.00, 0.00], [0.00, 0.00], [0.00, 0.00], [0.0, 0.45]], # kilobots
                "ylim" : [[0.00, 0.00], [0.00, 0.00], [0.00, 0.00], [0.00, 0.00], [0.00, 0.00], [0.00, 0.00], [0.0, 2.0]], # objectives in fitness function
            },
            "qd-scores" : {
                "name" : "qd-scores",
                "description" : "QD scores",
                "ylabel" : "QD Score",
                "index" : 2,
                "ylim" : [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.010]], # straight to foraging repertoire generation
                "ylim" : [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.015]], # straight to foraging baseline
            },
            "adjusted-qd-score" : { # uses 0.5 as default instead of 0.0
                "name" : "adjusted-qd-scores",
                "description" : "QD scores",
                "ylabel" : "QD Score",
                "index" : 2,
                "ylim" : [[0.5, 0.525], [0.5, 0.65], [0.5, 0.7], [0.5, 0.515], [0.5, 0.62], [0.48, 0.55], [0.0, 0.01]],
            },
            "avg-quality" : { # doesn't count empty bins
                "name" : "avg-quality",
                "description" : "Avg Quality",
                "ylabel" : "Avg Quality",
                "index" : 2,
                "ylim" : [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 1.25]], # straight to foraging baseline
                "ylim" : [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 1.25]], # straight to foraging repertoire generation
            },
            "coverage" : {
                "name" : "coverage",
                "description" : "coverage",
                "ylabel" : "Coverage",
                "index" : 3,
                "ylim" : [[0.0, 1.0], [0.0, 1.0], [0.0, 1.0], [0.0, 1.0], [0.0, 1.0], [0.0, 1.0], [0.0, 0.01]],
                "ylim" : [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 15000]], # straight to foraging baseline
                "ylim" : [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 10000]], # straight to foraging repertoire generation
            },
            "extrema" : {
                "name" : "extrema",
                "description" : ["green", "blue", "purple"],
                "ylabel" : ["Green Food", "Blue Food", "Purple Food"],
                "ylabel" : "Food Collected",
                "index" : 4,
                "ylim" : [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.5, 1.3]], # heterogeneous GA from 150cm comms
                "ylim" : [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 2.2]], # heterogeneous GA from 200cm comms
                "ylim" : [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 1.7]], # heterogeneous GA from grid extent 0.48
            }
        }
