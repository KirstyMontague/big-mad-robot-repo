
import local

class Behaviours():

    """
    Allows the EA to track the name and size of each sub-behaviour so
    that unpack() can calculate the real length of each chromosome for
    writing to the console and for derating.
    """

    subBehaviourSizes = {}

    def __init__(self, params, filename):

        self.params = params

        self.subBehaviourNodes = []
        for i in range(8):
            self.subBehaviourNodes.append("increaseDensity"+str(i+1))
            self.subBehaviourNodes.append("gotoNest"+str(i+1))
            self.subBehaviourNodes.append("gotoFood"+str(i+1))
            self.subBehaviourNodes.append("reduceDensity"+str(i+1))
            self.subBehaviourNodes.append("goAwayFromNest"+str(i+1))
            self.subBehaviourNodes.append("goAwayFromFood"+str(i+1))

        pset = local.PrimitiveSetExtended("MAIN", 0)
        self.params.addUnpackedNodes(pset)

        f = open(filename, "r")

        for line in f:

            name = line[0:line.find(" ")]

            chromosome = line[line.find(" ")+1:]
            chromosome = chromosome.replace(",", "")
            chromosome = chromosome.replace("(", " ")
            chromosome = chromosome.replace(")", " ")
            size = len(chromosome.split())

            self.subBehaviourSizes[name] = size

    def unpack(self, individual):
        
        packed_size = len(individual)
        unpacked_size = len(individual)
        
        for node in individual:
            for sub_behaviour in self.subBehaviourNodes:
                if node.name == sub_behaviour:
                    unpacked_size += self.subBehaviourSizes[sub_behaviour] - 1
        
        return unpacked_size
    
