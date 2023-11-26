
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

	def getArchives(self, redundancy):

		archive = self.getArchive()
		cumulative_archive = self.getCumulativeArchive()

		algorithm = "qdpy" if self.params.is_qdpy else "gp"

		for i in range(10):
			archive_path = "../gp/test/"+self.params.description+"/"+str(i+1)+"/"
			if archive_path != "../"+algorithm+"/"+self.params.path():
				if os.path.exists(archive_path+"archive.pkl"):
					with open(archive_path+"archive.pkl", "rb") as archive_file:
						cumulative_archive.update(pickle.load(archive_file))
			else:
				print ("disregarding "+archive_path)

		for i in range(10):
			archive_path = "../qdpy/test/"+self.params.description+"/"+str(i+1)+"/"
			if archive_path != "../"+algorithm+"/"+self.params.path():
				if os.path.exists(archive_path+"archive.pkl"):
					with open(archive_path+"archive.pkl", "rb") as archive_file:
						cumulative_archive.update(pickle.load(archive_file))
			else:
				print ("disregarding "+archive_path)

		temp_archive = {}
		if os.path.exists(self.params.path()+"archive.pkl"):
			with open(self.params.path()+"archive.pkl", "rb") as archive_file:
				temp_archive = pickle.load(archive_file)

		print (len(temp_archive))
		i = 0
		for chromosome, scores in temp_archive.items():
			if i < len(temp_archive) - 0:
				archive.update({str(chromosome) : scores})
				i += 1

		self.setArchive(archive)
		self.setCumulativeArchive(cumulative_archive)

		print("archive length "+str(len(archive)))
		print("cumulative archive length "+str(len(cumulative_archive)))

	def saveArchive(self, redundancy):

		if self.params.saveOutput:
			archive = self.getArchive()
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

		for i in range(1,9):
			mapping["increaseDensity"+str(i)] = "0"+str(i)
			mapping["reduceDensity"+str(i)] = "1"+str(i)
			mapping["gotoNest"+str(i)] = "2"+str(i)
			mapping["goAwayFromNest"+str(i)] = "3"+str(i)
			mapping["gotoFood"+str(i)] = "4"+str(i)
			mapping["goAwayFromFood"+str(i)] = "5"+str(i)

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

