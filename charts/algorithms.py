
class Algorithms():

    def __init__(self):

        self.info = {

            "gp" : {
                "name" : "gp",
                "description" : "GP",
                "path" : "gp",
            },
            "mtc" : {
                "name" : "mtc",
                "description" : "MTC",
                "path" : "gp",
            },
            "mti" : {
                "name" : "mti",
                "description" : "MTI",
                "path" : "gp",
            },
            "qdpy" : {
                "name" : "qd",
                "description" : "QD",
                "path" : "qdpy",
            },
            "cma-es" : {
                "name" : "gp",
                "description" : "CMA",
                "path" : "cma-es",
            },
            "baseline" : {
                "name" : "baseline",
                "description" : "Baseline",
                "path" : "gp",
            },
        }

    def getRepertoireName(self, repertoire):
        if repertoire == "baseline":
            return "Baseline"
        else:
            repertoire_type = ''.join([i.upper() for i in repertoire if not i.isdigit()])
            repertoire_size = ''.join([i for i in repertoire if i.isdigit()])
            return repertoire_type + repertoire_size


