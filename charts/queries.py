
class Queries():

    def __init__(self):

        self.info = {
            "best" : {
                "name" : "best",
                "description" : "best individuals",
                "ylabel" : "Best fitness",
                "index" : 1,
                "ylim" : [[0.5, 0.61], [0.6, 0.9], [0.83, 0.88]],
            },
            "qd-score" : {
                "name" : "qd-scores",
                "description" : "QD scores",
                "ylabel" : "QD Score",
                "index" : 2,
                "ylim" : [[0.0, 1.0], [0.0, 1.0], [0.0, 1.0]],
            },
            "coverage" : {
                "name" : "coverage",
                "description" : "coverage",
                "ylabel" : "Coverage",
                "index" : 3,
                "ylim" : [[0.0, 1.0], [0.0, 1.0], [0.0, 1.0]],
            }
        }
