
import math

class Grid():

    """
    Ad hoc implementation of MAP-Elites to reduce memory usage.
    Only stores one individual per bin, no handling for duplicates
    """

    def __init__(self, nb_bins, features_domain):

        self.container = {}
        self.nb_bins = nb_bins
        self.features_domain = features_domain

        self.bin_sizes = []
        for axis in range(len(self.nb_bins)):
            extent = self.features_domain[axis][1] - self.features_domain[axis][0]
            bin_size = extent / self.nb_bins[axis]
            self.bin_sizes.append(bin_size)

    def update(self, population):

        for ind in population:
            self.add(ind)

    def add(self, individual):

        indexes = []
        for axis in range(len(self.nb_bins)):

            if (individual.features[axis] < self.features_domain[axis][0] or
                individual.features[axis] > self.features_domain[axis][1]):
                raise ValueError(str(individual.features)+" is outside features domain")
            feature_normalised = individual.features[axis] - self.features_domain[axis][0]
            index = math.floor(feature_normalised / self.bin_sizes[axis])
            indexes.append(index)

        location = tuple(indexes)

        if location not in self.container or individual.fitness > self.container[location].fitness:
            self.container[location] = individual

    def values(self):
        return self.container.values()

    def items(self):
        return self.container.items()
