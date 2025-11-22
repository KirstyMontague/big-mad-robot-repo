
import os
import pickle

class Archive():

    def __init__(self, utilities, params):
        self.utilities = utilities
        self.params = params
        self.library = [[], []]
        self.archive = {}
        self.cumulative_archive = {}
        self.verbose_archive = {}
        self.complete_archive = {}
        self.input_path = self.params.input_path+"/cma-es"
        self.input_directory = self.params.objective
        self.output_directory = self.params.shared_path+"/cma-es/"+self.params.objective

    def getArchive(self):
        return self.archive

    def setArchive(self, archive):
        self.archive = archive

    def getVerboseArchive(self):
        return self.verbose_archive

    def getCumulativeArchive(self):
        return self.cumulative_archive

    def setCumulativeArchive(self, archive):
        self.cumulative_archive = archive

    def getCompleteArchive(self):
        return self.complete_archive

    def loadArchives(self):

        archive = self.getArchive()
        cumulative_archive = self.getCumulativeArchive()
        complete_archive = self.getCompleteArchive()

        use_temp_archive = (self.input_path == self.params.shared_path+"/cma-es")

        for i in range(15):
            archive_path = self.input_path+"/"+self.input_directory+"/"
            if not use_temp_archive or self.params.seed != i + 1:
                if os.path.exists(archive_path+"archive"+str(i+1)+".pkl"):
                    with open(archive_path+"archive"+str(i+1)+".pkl", "rb") as archive_file:
                        cumulative_archive.update(pickle.load(archive_file))
            else:
                print ("disregarding "+str(i + 1))

        temp_archive = {}
        if use_temp_archive and os.path.exists(self.output_directory+"/archive"+str(self.params.seed)+".pkl"):
            with open(self.output_directory+"/archive"+str(self.params.seed)+".pkl", "rb") as archive_file:
                temp_archive = pickle.load(archive_file)

        i = 0
        for chromosome, scores in temp_archive.items():
            if i < len(temp_archive) - 0:
                archive.update({str(chromosome) : scores})
                complete_archive.update({str(chromosome) : scores})
                i += 1

        self.setArchive(archive)

        print("archive length "+str(len(archive)))
        print("cumulative archive length "+str(len(cumulative_archive)))

    def saveArchive(self):

        archive = self.getCompleteArchive()
        archive_string = ""
        archive_dict = {}
        for chromosome, scores in archive.items():
            archive_dict.update({chromosome : scores})

        with open(self.output_directory+"/archive"+str(self.params.seed)+".pkl", "wb") as archive_file:
             pickle.dump(archive_dict, archive_file)

    def addToArchive(self, ind):

        trimmed = self.utilities.trimIndividualPrecision(ind)
        chromosome_string = self.getChromosomeString(trimmed)
        
        if chromosome_string in self.getArchive():
            # should only be true if chromosome is new but duplicated in this generation, otherwise would have been caught by assignDuplicateFitnessScores
            expected = self.archive[chromosome_string]
            if expected != ind.fitness.values[0]:
                print ("\nWRONG FITNESS\n")
                print (ind)
                print (self.archive[str(chromosome_string)])
                print (ind.fitness.values)
        else:
            self.archive.update({chromosome_string : ind.fitness.values[0]})
            self.verbose_archive.update({chromosome_string : ind.fitness.values[0]})

    def addToCompleteArchive(self, ind):

        trimmed = self.utilities.trimIndividualPrecision(ind)
        chromosome_string = self.getChromosomeString(trimmed)
        
        if chromosome_string not in self.complete_archive:
            self.complete_archive.update({str(chromosome_string) : ind.fitness.values[0]})


    def assignDuplicateFitness(self, offspring, assign_fitness, matched):

        trimmed = self.utilities.trimPopulationPrecision(offspring)
        offspring_strings = self.getChromosomeStrings(trimmed)
        
        archive = self.getArchive()
        cumulative_archive = self.getCumulativeArchive()

        archive_count = 0
        cumulative_count = 0
        for i in range(len(offspring)):
            if offspring_strings[i] in archive:
                scores = archive.get(offspring_strings[i])
                assign_fitness(offspring[i], (scores,))
                archive_count += 1

            elif offspring_strings[i] in cumulative_archive:
                scores = cumulative_archive.get(offspring_strings[i])
                assign_fitness(offspring[i], (scores,))
                cumulative_count += 1

        matched[0] = archive_count
        matched[1] = cumulative_count

        return offspring


    def getChromosomeStrings(self, population):
        
        chromosome_strings = []
        for ind in population:
            chromosome_strings.append(self.getChromosomeString(ind))
        return chromosome_strings

    def getChromosomeString(self, ind):
        
        chromosome_string = ""
        for c in ind:
            chromosome_string += str(c)+" "
        chromosome_string = chromosome_string[0:-1]
        return chromosome_string

