
import os
import pickle
import re



class Archive():

    def __init__(self, params, redundancy):
        self.params = params
        self.redundancy = redundancy
        self.library = [[], []]
        self.archive = {}
        self.cumulative_archive = {}
        self.verbose_archive = {}
        self.complete_archive = {}

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

    def setCompleteArchive(self, archive):
        self.complete_archive = archive

    def getArchives(self, redundancy):

        if not self.params.useArchive:
            print("\nDisregarding archive\n")
            return

        archive = self.getArchive()
        cumulative_archive = self.getCumulativeArchive()

        directory_path = self.params.input_path
        if self.params.description == "foraging":
            results_directory = self.params.foraging_path+"/"+self.params.repertoire_type+str(self.params.repertoire_size)
        else:
            results_directory = self.params.subbehaviours_path+"/"+self.params.description

        use_temp_archive = (directory_path == self.params.shared_path and results_directory == self.params.description)

        print()

        for i in range(30):
            archive_path = directory_path+"/gp/"+results_directory+"/"+str(i+1)+"/"
            if not use_temp_archive or archive_path != self.params.path():
                if os.path.exists(archive_path+"archive.pkl"):
                    with open(archive_path+"archive.pkl", "rb") as archive_file:
                        cumulative_archive.update(pickle.load(archive_file))
            else:
                print ("disregarding "+archive_path)

        for i in range(30):
            archive_path = directory_path+"/qdpy/"+results_directory+"/"+str(i+1)+"/"
            if not use_temp_archive or archive_path != self.params.path():
                if os.path.exists(archive_path+"archive.pkl"):
                    with open(archive_path+"archive.pkl", "rb") as archive_file:
                        cumulative_archive.update(pickle.load(archive_file))
            else:
                print ("disregarding "+archive_path)

        temp_archive = {}
        if use_temp_archive and os.path.exists(self.params.path()+"archive.pkl"):
            with open(self.params.path()+"archive.pkl", "rb") as archive_file:
                temp_archive = pickle.load(archive_file)

        for chromosome, scores in temp_archive.items():
            archive.update({str(chromosome) : scores})

        self.setArchive(archive)
        self.setCumulativeArchive(cumulative_archive)
        self.setCompleteArchive(temp_archive)

        print("archive length "+str(len(archive)))
        print("cumulative archive length "+str(len(cumulative_archive)))
        print()

    def saveArchive(self, redundancy, generation):

        if self.params.saveOutput and generation % self.params.csv_save_period == 0:
            archive = self.getCompleteArchive()
            archive_string = ""
            archive_dict = {}
            for chromosome, scores in archive.items():
                archive_dict.update({str(chromosome) : scores})

            with open(self.params.path()+"archive.pkl", "wb") as archive_file:
                 pickle.dump(archive_dict, archive_file)

    def mapNodesToArchive(self, chromosome):
        mapping = {
            "seqm2" : "a",
            "seqm3" : "b",
            "seqm4" : "c",
            "selm2" : "d",
            "selm3" : "e",
            "selm4" : "f",
            "probm2" : "g",
            "probm3" : "h",
            "probm4" : "i",
            "ifInNest" : "j",
            "ifOnFood" : "k",
            "ifGotFood" : "l",
            "ifNestToLeft" : "m",
            "ifNestToRight" : "n",
            "ifFoodToLeft" : "o",
            "ifFoodToRight" : "p",
            "ifRobotToLeft" : "q",
            "ifRobotToRight" : "r",
            "stop" : "s",
            "f" : "t",
            "fl" : "u",
            "fr" : "v",
            "r" : "w",
            "rl" : "x",
            "rr" : "y",
        }

        for i in range(1,65):
            leading_zero = "0" if i < 10 and self.params.repertoire_size > 8 else ""
            mapping["increaseDensity"+str(i)] = "0"+leading_zero+str(i)
            mapping["reduceDensity"+str(i)] = "1"+leading_zero+str(i)
            mapping["gotoNest"+str(i)] = "2"+leading_zero+str(i)
            mapping["goAwayFromNest"+str(i)] = "3"+leading_zero+str(i)
            mapping["gotoFood"+str(i)] = "4"+leading_zero+str(i)
            mapping["goAwayFromFood"+str(i)] = "5"+leading_zero+str(i)

        chromosome = chromosome.replace(" ", "")
        tokens = re.split("[ (),]", chromosome)

        string = ""
        for token in tokens:
            if len(token) > 0:
                string += mapping[token]

        return string

    def addToArchive(self, chromosome, fitness):

        new_chromosome = self.redundancy.trim(chromosome)
        mapped_chromosome = self.mapNodesToArchive(str(new_chromosome))

        if mapped_chromosome in self.archive:
            expected = self.archive[mapped_chromosome]
            if expected[0] != fitness[0] or expected[1] != fitness[1] or expected[2] != fitness[2]:

                print ("\nWRONG FITNESS\n")
                print (chromosome)
                print("\n")
                print (new_chromosome)
                print("\n")
                print (mapped_chromosome)
                print("\n")
                print (self.archive[str(mapped_chromosome)])
                print (fitness)
        else:
            self.verbose_archive.update({str(new_chromosome) : fitness})
            self.archive.update({mapped_chromosome : fitness})

    def addToCompleteArchive(self, chromosome, fitness):

        new_chromosome = self.redundancy.trim(chromosome)
        mapped_chromosome = self.mapNodesToArchive(str(new_chromosome))

        if mapped_chromosome not in self.complete_archive:
            self.complete_archive.update({str(mapped_chromosome) : fitness})

    def assignDuplicateFitness(self, offspring, assign_fitness, matched):

        offspring_chromosomes = []
        for ind in offspring:
            trimmed = self.redundancy.removeRedundancy(str(ind))
            trimmed = self.mapNodesToArchive(trimmed)
            offspring_chromosomes.append(trimmed)

        archive = self.getArchive()
        cumulative_archive = self.getCumulativeArchive()

        archive_count = 0
        cumulative_count = 0
        for i in range(len(offspring)):
            if offspring_chromosomes[i] in archive:
                scores = archive.get(offspring_chromosomes[i])
                assign_fitness(offspring[i], scores)
                archive_count += 1

            elif offspring_chromosomes[i] in cumulative_archive:
                scores = cumulative_archive.get(offspring_chromosomes[i])
                assign_fitness(offspring[i], scores)
                cumulative_count += 1

        matched[0] = archive_count
        matched[1] = cumulative_count

        return offspring


