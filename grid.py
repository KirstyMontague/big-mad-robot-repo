
import math
import numpy

class Grid():

    """
    Ad hoc implementation of MAP-Elites to reduce memory usage.
    Only stores one individual per bin, no handling for duplicates
    """

    def __init__(self, nb_bins, features_domain, bias = -1):

        self.container = {}
        self.nb_bins = nb_bins
        self.features_domain = features_domain
        self.bias = bias
        self.discard_out_of_bounds = False

        self.bin_sizes = []
        for axis in range(len(self.nb_bins)):
            extent = self.features_domain[axis][1] - self.features_domain[axis][0]
            bin_size = extent / self.nb_bins[axis]
            self.bin_sizes.append(bin_size)

    def discardOutOfBounds(self, discard):
        self.discard_out_of_bounds = discard

    def update(self, population):

        count = 0
        for ind in population:
            count += self.add(ind)
        return count

    def add(self, individual):

        indexes = []
        for axis in range(len(self.nb_bins)):

            if (individual.features[axis] < self.features_domain[axis][0] or
                individual.features[axis] > self.features_domain[axis][1]):
                if self.discard_out_of_bounds:
                    print("SKIPPED: "+str(individual.features)+" is outside features domain")
                    return 0
                else:
                    print("WARNING: "+str(individual.features)+" is outside features domain")

            feature_normalised = individual.features[axis] - self.features_domain[axis][0]
            index = math.floor(feature_normalised / self.bin_sizes[axis])

            if individual.features[axis] == self.features_domain[axis][1]:
                index -= 1

            indexes.append(index)

        location = tuple(indexes)

        if location not in self.container:
            self.container[location] = individual
            return 1

        if self.bias > -1:
            if individual.features[self.bias] > self.container[location].features[self.bias]:
                self.container[location] = individual
                return 1

        elif individual.fitness > self.container[location].fitness:
            self.container[location] = individual
            return 1

        return 0

    def values(self):
        return self.container.values()

    def items(self):
        return self.container.items()

    def quality_array(self):

        bins = numpy.empty(tuple(self.nb_bins))
        bins[:] = numpy.nan

        for index, ind in self.container.items():
            bins[index[0], index[1], index[2]] = ind.fitness.values[0]

        return bins
