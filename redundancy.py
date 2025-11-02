import time
import copy
import random
import subprocess
import time
import os
import re

import numpy

from functools import partial

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

from params import eaParams
from utilities import Utilities
from tests import RedundancyTests

import local



class Redundancy():

	sequenceNodes = ["seqm2", "seqm3", "seqm4"]
	fallbackNodes = ["selm2", "selm3", "selm4"]
	probabilityNodes = ["probm2", "probm3", "probm4"]
	compositionNodes = sequenceNodes + fallbackNodes + probabilityNodes
	conditionBaseNodes = ["ifOnFood", "ifGotFood", "ifInNest", "ifNestToLeft", "ifNestToRight", "ifFoodToLeft", "ifFoodToRight", "ifRobotToLeft", "ifRobotToRight"]
	successNodes = ["stop", "f", "fr", "fl", "r", "rr", "rl"]
	actionNodes = ["stop", "f", "fr", "fl", "r", "rr", "rl"]
	nonEffectiveNodes = ["stop", "ifOnFood", "ifGotFood", "ifInNest", "ifNestToLeft", "ifNestToRight", "ifFoodToLeft", "ifFoodToRight", "ifRobotToLeft", "ifRobotToRight"]
	effectiveNodes = ["stop", "f", "fr", "fl", "r", "rr", "rl"]
	subBehaviourBaseNodes = ["increaseDensity", "gotoNest", "gotoFood", "reduceDensity", "goAwayFromNest", "goAwayFromFood"]
	
	subBehaviourNodes = []
	conditionNodes = []
	
	def addSubBehaviours(self):
		for i in range(64):
			for node in self.subBehaviourBaseNodes:
				self.subBehaviourNodes.append(node+str(i+1))
				self.effectiveNodes.append(node+str(i+1))
				self.successNodes.append(node+str(i+1))
				self.actionNodes.append(node+str(i+1))
	
	def addExtraConditions(self):
		for node in self.conditionBaseNodes:
			self.conditionNodes.append(node)
			for i in range(64):
				self.nonEffectiveNodes.append(node+str(i+1))

	active = [True]
	trailingList = [] # booleans to mark whether the node at the same index is redundant


	def __init__(self, params):
		self.params = params
		self.utilities = Utilities(self.params)
		self.toolbox = base.Toolbox()
		self.primitivetree = gp.PrimitiveTree([])
		self.pset = local.PrimitiveSetExtended("MAIN", 0)
		self.params.addNodes(self.pset)
		self.addSubBehaviours()
		self.addExtraConditions()
		self.probm_chromosomes = []
		self.chromosomes = []
		tests = RedundancyTests()
		self.tests = tests.getTests()
		self.hits = 0
		self.limit = 10000
		self.verbose = False
		self.stop = True

	def printMessage(self, indent, message):
		if self.verbose == True and self.hits > 0:
			print(indent+message)

	def terminate(self):
		if (self.stop and self.hits > self.limit):
			print("more than "+str(self.hits)+" hits")
			return True
		return False

	def writeError(self, chromosome):

		tree = self.primitivetree.from_string(chromosome, self.pset)
		print("\nfailed to remove redundancy from tree\n")
		print("nodes: "+str(len(chromosome))+"   hits: "+str(self.hits))
		print("see "+self.params.shared_path+"/error.txt")

		with open(self.params.shared_path+'/error.txt', 'w') as f:
			f.write("nodes: "+str(len(chromosome))+"   hits: "+str(self.hits)+"\n")
			f.write(str(chromosome))
			f.write("\n")
			f.write(self.formatChromosome(tree))

	def test(tree):
		print ("test")

	def getProbmChromosomes(self):
		
		# node contained by probm is removed
		# self.probm_chromosomes.append("seqm2(f, probm2(selm2(ifFoodToLeft, ifNestToLeft), rr))")
		
		# self.probm_chromosomes.append("probm2(f, probm2(ifOnFood, seqm2(ifNestToLeft, ifNestToLeft)))")
		# self.probm_chromosomes.append("seqm2(probm2(ifRobotToRight, stop), seqm2(fr, ifNestToLeft))")
		
		self.probm_chromosomes.append("probm3(ifRobotToLeft, probm3(ifRobotToRight, ifNestToLeft, probm2(ifFoodToLeft, ifFoodToLeft)), f)")
		
		
		# self.probm_chromosomes.append("probm3(ifNestToLeft, ifNestToRight, probm3(ifRobotToLeft, ifNestToLeft, probm2(ifFoodToRight, probm4(rl, ifFoodToLeft, ifFoodToRight, ifFoodToRight))))")
		# self.probm_chromosomes.append("seqm3(probm4(selm4(ifOnFood, ifFoodToLeft, ifFoodToRight, ifFoodToRight), probm2(ifFoodToLeft, ifFoodToLeft), probm2(fl, f), selm2(ifFoodToRight, ifFoodToLeft)), seqm2(seqm2(ifFoodToLeft, ifFoodToRight), selm3(ifFoodToLeft, stop, ifOnFood)), probm3(selm2(ifFoodToLeft, ifNestToLeft), selm4(ifFoodToRight, rr, fr, fl), selm3(ifFoodToLeft, fl, ifFoodToRight)))")
		# self.probm_chromosomes.append("selm3(f, probm4(probm3(ifFoodToLeft, ifFoodToRight, rr), probm2(f, rr), seqm3(ifRobotToLeft, ifFoodToLeft, fl), probm4(ifRobotToRight, f, ifRobotToLeft, stop)), selm4(seqm3(rr, ifNestToRight, fl), seqm3(stop, ifNestToLeft, ifFoodToLeft), probm4(ifFoodToLeft, ifNestToLeft, ifNestToRight, ifNestToRight), selm4(ifFoodToLeft, stop, ifFoodToLeft, ifFoodToLeft)))")




	def getChromosomes(self):

		self.chromosomes.append("selm2(r, probm4(rl, ifRobotToLeft, ifNestToLeft, ifNestToRight))")

	def trim(self, chromosome):

		tree = self.primitivetree.from_string(chromosome, self.pset)
		
		output = []
		for j in range(len(self.trailingList) - 1, -1, -1):
			self.trailingList.pop()
		
		self.active = [True]
		self.trailingList = []
		self.hits = 0

		try:
			self.parseSubtreeGreedy(tree, "  ", output)
			self.trailingNodesGreedy(tree, output)
			self.capitaliseOutput(output)

			trailing = self.trailingList
			new_chromosome = self.replaceObsoleteConditionsWithStop(tree, tree.searchSubtree(0), trailing, "", 1, True)
			new_chromosome = self.rebuildFromTrailingList(trailing, new_chromosome, new_chromosome.searchSubtree(0), "", 1)

		except:
			self.writeError(chromosome)
			raise

		return new_chromosome

	def removeRedundancy(self, chromosome):
		
		tree = self.primitivetree.from_string(chromosome, self.pset)
		
		output = []
		for j in range(len(self.trailingList) - 1, -1, -1):
			self.trailingList.pop()
		
		self.active = [True]
		self.trailingList = []
		self.hits = 0

		try:
			self.parseSubtreeGreedy(tree, "  ", output)
			self.trailingNodesGreedy(tree, output)
			self.capitaliseOutput(output)

			trailing = self.trailingList
			new_chromosome = self.replaceObsoleteConditionsWithStop(tree, tree.searchSubtree(0), trailing, "", 1, True)
			new_chromosome = self.rebuildFromTrailingList(trailing, new_chromosome, new_chromosome.searchSubtree(0), "", 1)
		
		except:
			self.writeError(chromosome)
			raise
		
		return str(new_chromosome)
	
	def makeTests(self):
		
		self.getChromosomes()
		
		for i in range(len(self.chromosomes)):
			
			# print(i)
			
			chromosome = self.chromosomes[i]
			tree = self.primitivetree.from_string(chromosome, self.pset)
			# print(self.formatChromosome(tree))
			
			
			rType = tree.root.ret
			pType = tree[0]
			
			if True or pType in self.pset.primitives[rType]:
				
			
				# greedy
				output = []
				modified_output = []
				composites = []
				for j in range(len(self.trailingList) - 1, -1, -1):
					self.trailingList.pop()
				
				self.active = [True]
				self.trailingList = []

				# populate trailinglist, marking the areas where seqences fail or fallbacks succeed
				self.parseSubtreeGreedy(tree, "  ", output)
				
				# mark areas of the genome which cannot lead to any actions
				self.trailingNodesGreedy(tree, output)
				
				self.capitaliseOutput(output)
				
				# print("")
				# print(self.trailingList)
				# print(self.formatChromosome(tree))
				# print("-----")
				
				trailing = self.trailingList
				new_chromosome = tree
				new_chromosome = self.replaceObsoleteConditionsWithStop(tree, tree.searchSubtree(0), trailing, "", 1, True)
				new_tree = self.primitivetree.from_string(str(new_chromosome), self.pset)
				
				# print("")
				# print(trailing)
				# print(self.formatChromosome(new_tree))
				# print("-----")
				
				new_chromosome = self.rebuildFromTrailingList(trailing, new_chromosome, new_chromosome.searchSubtree(0), "", 1)
				new_tree = self.primitivetree.from_string(str(new_chromosome), self.pset)
				
				# print("")
				# print(trailing)
				# print(self.formatChromosome(new_tree))
				# print("-----")
				
				expected_fitness = self.utilities.evaluateRobot(tree, 1)
				actual_fitness = self.utilities.evaluateRobot(new_tree, 2)	
				
				if expected_fitness[0] != actual_fitness[0] or expected_fitness[1] != actual_fitness[1] or expected_fitness[2] != actual_fitness[2]:
					print("\nERROR on "+str(i)+"\n")
				
				# print ("evaluating "+str(tree))
				# print ("evaluating "+str(new_tree))			
				# print(fitness)
				
				record = "\t\tself.tests.append({\n"
				record += "\t\t\t\"bt\" : \""+str(tree)+"\",\n"
				record += "\t\t\t\"trimmed\" : \""+str(new_tree)+"\",\n"
				record += "\t\t\t\"fitness\" : "+str(expected_fitness)+"\n"
				record += "\t\t})\n"
				print(record)
	
	def checkRedundancy(self):
		
		# self.makeTests()
		# return
		
		errors = ""
		self.getChromosomes()
		
		for i in range(len(self.tests)):
			
			# print(i)
			
			chromosome = self.tests[i]["bt"]
			tree = self.primitivetree.from_string(chromosome, self.pset)
			# print(self.formatChromosome(tree))
			
			
			rType = tree.root.ret
			pType = tree[0]
			
			if True or pType in self.pset.primitives[rType]:
				
			
				# greedy
				output = []
				modified_output = []
				composites = []
				for j in range(len(self.trailingList) - 1, -1, -1):
					self.trailingList.pop()
				
				self.active = [True]
				self.trailingList = []

				# populate trailinglist, marking the areas where seqences fail or fallbacks succeed
				self.parseSubtreeGreedy(tree, "  ", output)
				
				# mark areas of the genome which cannot lead to any actions
				self.trailingNodesGreedy(tree, output)
				
				self.capitaliseOutput(output)
				
				# print("")
				# print(self.trailingList)
				# print(self.formatChromosome(tree))
				# print("-----")
				
				trailing = self.trailingList
				new_chromosome = tree
				new_chromosome = self.replaceObsoleteConditionsWithStop(tree, tree.searchSubtree(0), trailing, "", 1, True)
				new_tree = self.primitivetree.from_string(str(new_chromosome), self.pset)
				
				# print("")
				# print(trailing)
				# print(self.formatChromosome(new_tree))
				# print("-----")
				
				new_chromosome = self.rebuildFromTrailingList(trailing, new_chromosome, new_chromosome.searchSubtree(0), "", 1)
				new_tree = self.primitivetree.from_string(str(new_chromosome), self.pset)
				
				# print("")
				# print(trailing)
				# print(self.formatChromosome(new_tree))
				# print("-----")
				
				# print ("evaluating "+str(tree))
				# print ("evaluating "+str(new_tree))
				
				print ("difference: "+str(len(tree) - len(new_tree)))
				
				expected_fitness = self.tests[i]["fitness"]
				expected_fitness = self.utilities.evaluateRobot(tree, 1)
				# print(expected_fitness)
				actual_fitness = self.utilities.evaluateRobot(new_tree, 2)
				
				print(expected_fitness)
				print(actual_fitness)
				
				# fitness[3] doesn't need to match because trailing condition
				# nodes affect conditionality in arbitrary ways
				if expected_fitness[0] != actual_fitness[0] or expected_fitness[1] != actual_fitness[1] or expected_fitness[2] != actual_fitness[2]:
					print("FITNESS ERROR on "+str(i))
				
				if str(new_tree) != self.tests[i]["trimmed"]:
					errors += "TREE ERROR on "+str(i)+"\n"
					print("")
					print("TREE ERROR on "+str(i))
					print("")
					print(new_tree)
					print(self.formatChromosome(tree))
					print("")
					print(self.formatChromosome(new_tree))
					print("")
				
				# chromosome = self.rebuildChromosome(output)
				
				# lazy
				# output = []
				# composites = []
				# for j in range(len(self.trailingList) - 1, -1, -1):
					# self.trailingList.pop()
					
				# self.parseSubtreeLazy(rType, tree, "  ", output, composites)
				# self.trailingNodesLazy(tree, output)
				
		print (errors)
		
	def checkProbmNodes(self):
		
		self.getProbmChromosomes()
		
		for i in range(len(self.probm_chromosomes)):
			
			print(i)
			
			chromosome = self.probm_chromosomes[i]
			tree = self.primitivetree.from_string(chromosome, self.pset)
			print(self.formatChromosome(tree))
			
			
			rType = tree.root.ret
			pType = tree[0]
			
			if True or pType in self.pset.primitives[rType]:
				
			
				# greedy
				output = []
				modified_output = []
				composites = []
				for j in range(len(self.trailingList) - 1, -1, -1):
					self.trailingList.pop()
				
				self.active = [True]
				self.trailingList = []

				# populate trailinglist, marking the areas where seqences fail or fallbacks succeed
				self.parseSubtreeGreedy(tree, "  ", output)
				
				# mark areas of the genome which cannot lead to any actions
				self.trailingNodesGreedy(tree, output)
				
				self.capitaliseOutput(output)
				
				# print("greedy\n")
				# print(self.trailingList)
				# print(self.formatChromosome(tree))
				# print("-----")
				
				trailing = self.trailingList
				new_chromosome = tree
				new_chromosome = self.replaceObsoleteConditionsWithStop(tree, tree.searchSubtree(0), trailing, "", 1, True)
				new_tree = self.primitivetree.from_string(str(new_chromosome), self.pset)
				
				# print("replaceObsoleteConditionsWithStop\n")
				# print(trailing)
				# print(self.formatChromosome(new_tree))
				# print("-----")
				
				new_chromosome = self.rebuildFromTrailingList(trailing, new_chromosome, new_chromosome.searchSubtree(0), "", 1)
				new_tree = self.primitivetree.from_string(str(new_chromosome), self.pset)
				
				print("rebuildFromTrailingList\n")
				print(trailing)
				print(self.formatChromosome(new_tree))
				print("-----")
				
				# fitness = self.evaluateRobot(tree, 1)
				# fitness = self.expected[i]
				# fitness2 = self.evaluateRobot(new_tree, 2)	
				# print ("evaluating "+str(tree))
				# print ("evaluating "+str(new_tree))			
				# print(fitness)
				# print(fitness2)
				
				# if fitness[0] != fitness2[0] or fitness[1] != fitness2[1] or fitness[2] != fitness2[2]:
					# print("ERROR on "+str(i))
				
				# return
				
				chromosome = self.rebuildChromosome(output)
				
				
				
				
				
				# lazy
				output = []
				composites = []
				for j in range(len(self.trailingList) - 1, -1, -1):
					self.trailingList.pop()
					
				self.parseSubtreeLazy(rType, tree, "  ", output, composites)				
				self.trailingNodesLazy(tree, output)
				

	def parseSubtreeLazy(self, rType, tree, indent, output, composites):
		
		# print indent+"tree "+str(tree)
		returnStatus = "ambiguous"
		probReturnStatus = ""
		
		output.append(tree[0].name)
		
		# trailinglist entry for this subtree depends on whether the parent is active
		self.trailingList.append(self.active[-1])
			
		# at the bottom of this subtree, return status
		if len(tree) == 1:
			node = str(tree[0].name)
			if node in self.successNodes: returnStatus = "success"
			if node in self.conditionNodes + self.subBehaviourNodes: returnStatus = "ambiguous"
			
		# in a branch, call same funtion on all subtrees		
		else:
			
			sequenceStatus = "success"
			
			# assume that this subtree is active if its parent is active
			self.active.append(self.active[-1])
				
			lenCount = 1
			while (lenCount < len(tree)):
				slice_ = tree.searchSubtree(lenCount)
				chromosome = tree[slice_]
				subtree = gp.PrimitiveTree(chromosome)
				lenCount += len(subtree)
				
				# get the return value of this subtree
				status = self.parseSubtreeLazy(rType, subtree, "  "+indent, output, composites)
				
				# sequence failed, from here in all subtrees are not active
				if tree[0].name in self.sequenceNodes and status == "failure":
					sequenceStatus = "failure"
					self.active[-1] = False
				
				# sequence ambiguous, downgrade  if currently successful				
				if tree[0].name in self.sequenceNodes and status == "ambiguous":
					sequenceStatus = "ambiguous" if sequenceStatus != "failure" else "failure"
				
				# fallback node succeeded, why set sequence to success? from here in all subtrees not active
				if tree[0].name in self.fallbackNodes and status == "success":
					returnStatus = "success"
					self.active[-1] = False
				
				# for probability nodes return value is only certain if all subtrees return success or failure
				if tree[0].name in self.probabilityNodes: 
					returnStatus = self.parseProbabilityNode(probReturnStatus, status)
					probReturnStatus = returnStatus
			
			# finished descending into all subtrees, don't need to know it this tree's list is active now
			self.active.pop()
			
		if tree[0].name in self.sequenceNodes: return sequenceStatus
		else: return returnStatus

	def parseSubtreeGreedy(self, tree, indent, output):
		
		"""
		descends into every subtree and returns success or ambiguous, probably not failure
		uses active list to populate trailinglist
		"""
		
		returnStatus = "ambiguous"
		probReturnStatus = ""
		
		output.append(tree[0].name)
		
		# trailinglist entry for this subtree depends on whether the parent is active
		self.trailingList.append(self.active[-1])
		
		# at the bottom of this subtree, return status
		if len(tree) == 1:
			node = str(tree[0].name)
			if node in self.successNodes: returnStatus = "success"
			if node in self.conditionNodes + self.subBehaviourNodes: returnStatus = "ambiguous"
		
		# in a branch, call same function on all subtrees	
		else:
			
			sequenceStatus = "success"
			
			# assume that this subtree is active if its parent is active
			self.active.append(self.active[-1])
				
			lenCount = 1
			while (lenCount < len(tree)):
				slice_ = tree.searchSubtree(lenCount)
				chromosome = tree[slice_]
				subtree = gp.PrimitiveTree(chromosome)
				lenCount += len(subtree)
				
				# get the return value of this subtree
				status = self.parseSubtreeGreedy(subtree, "  "+indent, output)
				
				# sequence failed, from here in all subtrees are not active
				if tree[0].name in self.sequenceNodes and status == "failure":
					sequenceStatus = "failure"
					self.active[-1] = False
				
				# sequence ambiguous, downgrade  if currently successful
				if tree[0].name in self.sequenceNodes and status == "ambiguous":
					sequenceStatus = "ambiguous" if sequenceStatus != "failure" else "failure"
				
				# fallback node succeeded, why set sequence to success? from here in all subtrees not active
				if tree[0].name in self.fallbackNodes and status == "success":
					returnStatus = "success"
					self.active[-1] = False
				
				# for probability nodes return value is only certain if all subtrees return success or failure
				if tree[0].name in self.probabilityNodes:
					returnStatus = self.parseProbabilityNode(probReturnStatus, status)
					probReturnStatus = returnStatus
			
			# finished descending into all subtrees, don't need to know it this tree's list is active now
			self.active.pop()
		
		# who knows
		if tree[0].name in self.sequenceNodes: return sequenceStatus
		else: return returnStatus

	def parseProbabilityNode(self, returnStatus, status):
		probReturnStatus = ""
		if status == "ambiguous" or returnStatus == "ambiguous":
			probReturnStatus = "ambiguous"
		if probReturnStatus != "ambiguous":
			if status == "success" and returnStatus != "failure":
				probReturnStatus = "success"
			elif status == "failure" and returnStatus != "success":
				probReturnStatus = "failure"
			else:
				probReturnStatus = "ambiguous"
		# print "probReturnStatus " + status + " " +probReturnStatus	
		return probReturnStatus

	def parseSubtreeActivityWithProbabilityNodesToo(self, tree):
		
		if tree[0].name in self.effectiveNodes + self.probabilityNodes:
			# if this is a node which causes an action we can now return true
			return True
		else:
			# check recursively by descending into this tree's subtrees 
			lenCount = 1
			while (lenCount < len(tree)):
				slice_ = tree.searchSubtree(lenCount)
				chromosome = tree[slice_]
				subtree = gp.PrimitiveTree(chromosome)
				lenCount += len(subtree)
				
				activity = self.parseSubtreeActivityWithProbabilityNodesToo(subtree)
				if activity: 
					return True
		
		# none of this tree's subtrees causes any actions
		return False

	def parseSubtreeActivity(self, tree):
		
		if tree[0].name in self.effectiveNodes:
			# if this is a node which causes an action we can now return true
			return True
		else:
			# check recursively by descending into this tree's subtrees 
			lenCount = 1
			while (lenCount < len(tree)):
				slice_ = tree.searchSubtree(lenCount)
				chromosome = tree[slice_]
				subtree = gp.PrimitiveTree(chromosome)
				lenCount += len(subtree)
				
				activity = self.parseSubtreeActivity(subtree)
				if activity: 
					return True
		
		# none of this tree's subtrees causes any actions
		return False

	def trailingNodesLazy(self, tree, output):
		# for node in reversed(output):
			# if node not in effectiveNodes:
				# output.pop()
			# else:
				# break
		
				
		slice_ = tree.searchSubtree(0)
		self.trailingNodes(tree, slice_, 1, True)
		for i in range(len(self.trailingList) - 1, -1, -1):
			if not self.trailingList[i]:
				output.pop(i)

	def trailingNodesGreedy(self, tree, output):
		# for i in range(len(output) - 1, -1, -1):
			# if output[i] not in effectiveNodes:
				# output[i] = output[i].upper()
			# else:
				# break
		
		# for i in range(len(tree)): trailingList.append(True)
		slice_ = tree.searchSubtree(0)
		self.trailingNodes(tree, slice_, 1, True)

	def getSubtreeSlices(self, tree, slice_):
		
		slices = []
		
		slice_index = slice_.start + 1
		while (slice_index < slice_.stop):
			sub_subtree_slice = tree.searchSubtree(slice_index)
			# chromosome = tree[sub_subtree_slice]
			# sub_subtree = gp.PrimitiveTree(chromosome)
			slices.append(sub_subtree_slice)
			slice_index += sub_subtree_slice.stop - sub_subtree_slice.start
			# slice_index += len(sub_subtree)
		
		return slices

	def trailingNodes(self, tree, slice_, first, last):
		
		parent_is_last_subtree = last
		subtree_slice = slice_
		subtree_chromosome = tree[slice_]
		subtree = gp.PrimitiveTree(subtree_chromosome)

		slices = self.getSubtreeSlices(tree, slice_)
		
		subtree_is_active = False
		activity_somewhere_in_subtree = False
		next_subtree_is_active = False
		
		parent = subtree[0].name
		parent_is_prob_node = parent in self.probabilityNodes
		
		# going backwards through all slices
		for i in range(len(slices) - 1, -1, -1):
		
			chromosome = tree[slices[i]]
			sub_subtree = gp.PrimitiveTree(chromosome)
			sub_subtree_start = slices[i].start
			sub_subtree_stop = slices[i].stop
			
			# if not first time round loop and a subtree has already been marked as active and the next (prev
			# in loop) subtree is active and this isn't a probability node then this is not the last subtree
			if i < len(slices) - 1 and subtree_is_active and next_subtree_is_active and not parent_is_prob_node:
				last = False
			
			# check subtree for actions and make subtree_is_active true if trailingList entry for this
			# slice's root node is true and it isn't already
			activity = self.parseSubtreeActivityWithProbabilityNodesToo(sub_subtree)
			if self.trailingList[sub_subtree_start]: subtree_is_active = (subtree_is_active or activity)
			
			# if this is the last subtree which could have actions and doesn't have any actions
			if last and not subtree_is_active:
				
				# if it isn't a probability node make all associated trailingList entries False including the parent
				if not parent_is_prob_node:
					for j in range(sub_subtree_start, sub_subtree_stop):
						self.trailingList[j] = False
				# otherwise make only the children false
				else:
					for j in range(sub_subtree_start+1, sub_subtree_stop):
						if not activity: 
							self.trailingList[j] = False
			
			# if not the last subtree or could have actions recursively descend into this subtree
			else:
				activity_somewhere_in_subtree = True
				trailingSubtree = last
				first += 1
				if (first < 1000): self.trailingNodes(tree, slices[i], first, trailingSubtree)
			
			# if we didn't set trailinglist for the root node of this subtree to False we
			# record that this subtree is active for next time round the loop
			if self.trailingList[sub_subtree_start]:
				next_subtree_is_active = True
		
		# if this whole function was called on the (or a) last (sub?)tree and the root is a
		# probability node and the whole subtree is inactive mark the whole this false in trailinglist
		if parent_is_last_subtree and parent_is_prob_node and not activity_somewhere_in_subtree:
			# for i in range(subtree_slice.start, subtree_slice.stop):
			for i in range(subtree_slice.start + 3, subtree_slice.stop): # edited
				if i > 0: 
					self.trailingList[i] = False

	def capitaliseOutput(self, output):
		for i in range(len(output)):
			if self.trailingList[i] == False:
				output[i] = output[i].upper()
	
	def rebuildFromTrailingList(self, trailing, tree, slice_, indent, first):
		
		removed_node_last_time = True
		count = 0
		
		while removed_node_last_time and count < 10:
			
			removed_node_last_time = False
			count += 1
			
			subtree = gp.PrimitiveTree(tree[slice_])
			
			slices = self.getSubtreeSlices(tree, slice_)
			
			# going backwards through all slices
			for i in range(len(slices) - 1, -1, -1):
				
				# print(indent+str(slices[i]))
				
				parent_name = subtree[0].name
				node_name = tree[slices[i].start].name
				
				if not trailing[slices[i].start]:
					
					# print(indent+str(slices[i].start))
				
					parent_name = parent_name[0:-1] + str(int(parent_name[-1]) - 1)
					parent_index = slices[0].start - 1
						
					if node_name in self.probabilityNodes:
					
						# print(indent+subtree[0].name+" to "+parent_name+" (index "+str(parent_index)+")")
						
						new_list = []
						for node in tree:
							new_list.append(node.name)	
						
						if True or int(parent_name[-1]) > 2:			
							
							del new_list[slices[i].start:slices[i].stop]
							del trailing[slices[i].start:slices[i].stop]
							
							if parent_name[-1] == "1":
								del new_list[parent_index]
								del trailing[parent_index]
							else:	
								new_list[parent_index] = parent_name
						
							tree = self.buildNewTreeFromList(trailing, new_list, indent)
							
							subtree = self.updateSubtree(tree, slices, parent_name)
							
						if parent_name[-1] == "1":
							# print(indent+"removed_node_last_time = True")
							removed_node_last_time = True
							slice_ = tree.searchSubtree(slices[0].start - 1)
							break
							
					else:
						# print(indent+subtree[0].name+" to "+parent_name+" (index "+str(parent_index)+")")
						new_list = []
						for node in tree:
							new_list.append(node.name)	
						# print(indent+str(slices[i].start)+" - "+str(slices[i].stop))			
						del new_list[slices[i].start:slices[i].stop]
						del trailing[slices[i].start:slices[i].stop]
						
						if parent_name[-1] == "1":
							del new_list[parent_index]
							del trailing[parent_index]
						else:	
							new_list[parent_index] = parent_name
						
						tree = self.buildNewTreeFromList(trailing, new_list, indent)
						
						subtree = self.updateSubtree(tree, slices, parent_name)
						
						if parent_name[-1] == "1":
							# print(indent+"removed_node_last_time = True")
							removed_node_last_time = True
							slice_ = tree.searchSubtree(slices[0].start - 1)
							break
						
						
				# otherwise descend into this subtree
				elif not removed_node_last_time and tree[slices[i].start].name in self.compositionNodes:
					first += 1
					if (first < 1000):
						tree = self.rebuildFromTrailingList(trailing, tree, slices[i], indent+"  ", first)
						subtree = self.updateSubtree(tree, slices, parent_name)
			
		return tree
			
	def rebuildFromParse(self, rType, tree, indent, output, composites): # not used
		
		returnStatus = "ambiguous"
		probReturnStatus = ""
		
		output.append(tree[0].name)
		
		# trailinglist entry for this subtree depends on whether the parent is active
		self.trailingList.append(self.active[-1])
		
		# at the bottom of this subtree, return status
		if len(tree) == 1:
			node = str(tree[0].name)
			if node in self.successNodes: returnStatus = "success"
			if node in self.conditionNodes: returnStatus = "ambiguous"
		
		# in a branch, call same function on all subtrees	
		else:
			
			sequenceStatus = "success"
			
			# assume that this subtree is active if its parent is active
			self.active.append(self.active[-1])
				
			lenCount = 1
			while (lenCount < len(tree)):
				slice_ = tree.searchSubtree(lenCount)
				chromosome = tree[slice_]
				subtree = gp.PrimitiveTree(chromosome)
				lenCount += len(subtree)
				
				# get the return value of this subtree
				status = self.parseSubtreeGreedy(rType, subtree, "  "+indent, output, composites)
				
				# sequence failed, from here in all subtrees are not active
				if tree[0].name in self.sequenceNodes and status == "failure":
					sequenceStatus = "failure"
					self.active[-1] = False
				
				# sequence ambiguous, downgrade  if currently successful
				if tree[0].name in self.sequenceNodes and status == "ambiguous":
					sequenceStatus = "ambiguous" if sequenceStatus != "failure" else "failure"
				
				# fallback node succeeded, why set sequence to success? from here in all subtrees not active
				if tree[0].name in self.fallbackNodes and status == "success":
					returnStatus = "success"
					self.active[-1] = False
				
				# for probability nodes return value is only certain if all subtrees return success or failure
				if tree[0].name in self.probabilityNodes:
					returnStatus = self.parseProbabilityNode(probReturnStatus, status)
					probReturnStatus = returnStatus
			
			# finished descending into all subtrees, don't need to know it this tree's list is active now
			self.active.pop()
		
		# who knows
		if tree[0].name in self.sequenceNodes: return sequenceStatus
		else: return returnStatus

	def anyActivityInSubtree(self, tree, index, indent):
		
		subtree_slice = tree.searchSubtree(index)
		for k in range(subtree_slice.start, subtree_slice.stop):
			# if tree[k].name in self.actionNodes: # updated for subbehaviours
			if tree[k].name in self.effectiveNodes:
				return True
		return False

	def changeConditionNode(self , name):
		return "ifInNest"
		return "ifOnFood" if name == "ifInNest" else "ifInNest"

	def buildNewTreeFromList(self, trailing, new_list, indent):

		new_chromosome = ""
		for node in new_list:
			new_chromosome += node + " "
		new_chromosome = new_chromosome[0:-1]
		
		new_tree = self.primitivetree.from_string(new_chromosome, self.pset)
		# print(indent+str(trailing))
		# print(indent+str(new_tree))
		# print("")
		return new_tree

	def neutraliseProbmChildren(self, trailing, new_list, j):
		
		trailing[j] = True
		trailing[j+1] = True
		trailing[j+2] = True
		new_list[j+1] = self.changeConditionNode(new_list[j+1])
		new_list[j+2] = self.changeConditionNode(new_list[j+2])
		
		if int(node[-1]) > 3:
			new_list[j+4] = self.changeConditionNode(new_list[j+4])
			trailing[j+4] = False
		if int(node[-1]) > 2:
			new_list[j+3] = self.changeConditionNode(new_list[j+3])
			trailing[j+3] = False
			
		tree = self.buildNewTreeFromList(trailing, new_list, indent)
		return tree

	def updateSubtree(self, tree, slices, node):
		slice_start = slices[0].start - 1
		slice_stop = slices[int(node[-1]) - 1].stop
		subtree = tree[slice_start:slice_stop]
		return subtree

	def replaceObsoleteConditionsWithStop(self, tree, slice_, trailing, indent, first, last):
		
		removed_node_last_time = True
		count = 0
		self.hits += 1
		if self.terminate(): return

		# removed_node_last_time is true if we removed a seqm or selm node last
		# time round, or descending into a subtree caused the tree to be changed
		while removed_node_last_time and count < 100:

			removed_node_last_time = False

			if self.terminate(): return

			count += 1
			# print(indent+str(slice_))

			parent_is_last_subtree = last
			
			subtree_slice = slice_
			subtree_chromosome = tree[slice_]
			subtree = gp.PrimitiveTree(subtree_chromosome)
			
			slices = self.getSubtreeSlices(tree, slice_)
			
			subtree_is_active = False
			nextSubtreeActive = False
			
			parent = subtree[0].name
			parent_is_prob_node = parent in self.probabilityNodes
			
			self.printMessage(indent, parent+" "+str(slice_))

			# going backwards through all slices
			for i in range(len(slices) - count, -1, -1):
			
				if self.terminate(): return

				active_subtree_this_iteration = False
				chromosome = tree[slices[i]]
				subSubtree = gp.PrimitiveTree(chromosome)

				# self.printMessage(indent, str(slices[i].start)+" - "+str(slices[i].stop)+"  "+str(subSubtree))

				sub_subtree_parent = subSubtree[0].name
				
				# if not first time round loop and a subtree has already been marked as active and the next (prev
				# in loop) subtree is active and this isn't a probability node then this is not the last subtree
				if i < len(slices) - 1 and subtree_is_active and nextSubtreeActive and not parent_is_prob_node:
					last = False
				
				# check subtree for actions and make subtree_is_active true if trailingList entry for this
				# slice's root node is true and it isn't already
				activity = self.parseSubtreeActivityWithProbabilityNodesToo(subSubtree)
				real_activity = self.parseSubtreeActivity(subSubtree)
				if self.trailingList[slices[i].start]:
					subtree_is_active = ((subtree_is_active and not parent_is_prob_node) or activity)
					active_subtree_this_iteration = ((subtree_is_active and not parent_is_prob_node) or activity)
				
				# if this is the last subtree which could have actions and doesn't have any actions
				if last and not activity and not active_subtree_this_iteration:
					
					# self.printMessage(indent, "last and not active_subtree_this_iteration")
				
					if parent_is_prob_node:
						
						# self.printMessage(indent, "parent_is_prob_node")
						
						for j in reversed(range(slices[i].start, slices[i].stop)):
							
							node = tree[j].name
							# self.printMessage(indent, str(j)+" "+node)
							
							if node in self.conditionNodes:
								
								# don't change condition nodes here because they're covered
								# in the last clause outside the main loop
								
								new_list = []
								for node in tree:
									new_list.append(node.name)
								trailing[j] = True if j < slices[i].start + 2 else False
								
								tree = self.buildNewTreeFromList(trailing, new_list, indent)
							
							elif node in self.sequenceNodes + self.fallbackNodes:
								
								# print(indent+"node in self.sequenceNodes + self.fallbackNodes")
								# print(indent+str(j))
								# print(indent+tree[j].name)
								
								# if a seqm or selm node will be deleted here
								# we need to assign default condition node name
								# to "node" and delete children because we can
								# no longer identify this as a composition node
								
								if not self.anyActivityInSubtree(tree, j, indent):
									
									# print(indent+"not self.anyActivityInSubtree")
									
									new_list = []
									for n in tree:
										new_list.append(n.name)
								
									if int(node[-1]) > 3:
										del trailing[j+4]
										del new_list[j+4]
									if int(node[-1]) > 2:
										del trailing[j+3]
										del new_list[j+3]
									del trailing[j+2]
									del trailing[j+1]
									del new_list[j+2]
									del new_list[j+1]
									
										
									trailing[j] = True
									new_list[j] = self.changeConditionNode(new_list[j])
									
									tree = self.buildNewTreeFromList(trailing, new_list, indent)
										
									removed_node_last_time = True
									
									break
							
							elif node in self.probabilityNodes and not self.anyActivityInSubtree(tree, j):
								
								self.printMessage(indent, "can't find anywhere this is used (probm node and no activity in subtree)")
								# this probm node is nested in another probm node, 
								# keep (at least) the first two conditions
								
								new_list = []
								for n in tree:
									new_list.append(n.name)								
								tree = self.neutraliseProbmChildren(trailing, new_list, j)
								
					elif sub_subtree_parent in self.probabilityNodes:						
						self.printMessage(indent, "can't find anywhere this is used (sub-subtree parent is probm node)")
						for j in reversed(range(slices[i].start, slices[i].stop)):
							if tree[j].name in self.probabilityNodes and not self.anyActivityInSubtree(tree, j):
								new_list = []
								for node in tree:
									new_list.append(node.name)
								tree = self.neutraliseProbmChildren(trailing, new_list, j)
								
				# otherwise descend into this subtree
				if not last or active_subtree_this_iteration or (not parent_is_prob_node and not sub_subtree_parent in self.probabilityNodes):
					
					# self.printMessage(indent, "descend into subtree")
					
					first += 1
					if (first < 10000):
						
						trailingSubtree = last

						old_tree = tree
						tree = self.replaceObsoleteConditionsWithStop(tree, slices[i], trailing, "  "+indent, first, trailingSubtree)
						new_tree = tree

						if old_tree != new_tree:
							removed_node_last_time = True
							self.printMessage(indent, "removed_node_last_time = True")

						if self.terminate(): return
				
				if removed_node_last_time:

					subtree = self.updateSubtree(tree, slices, subtree[0].name)
					slice_ = tree.searchSubtree(slices[0].start - 1)
									
					if not parent_is_prob_node and activity:
						last = False
					break
				
				# if the trailinglist value for the root node of this subtree is False we
				# record that this subtree is active for next time round the loop
				if self.trailingList[slices[i].start]:
					nextSubtreeActive = True
			
			# probably don't want to do this if we've just rearranged the tree but not sure
			if not removed_node_last_time and parent_is_last_subtree and parent_is_prob_node:
				
				# self.printMessage(indent, "not removed_node_last_time and parent_is_last_subtree and parent_is_prob_node")

				prob_subtree_slices = self.getSubtreeSlices(tree, subtree_slice)
				
				tree_index = prob_subtree_slices[-1].start
				slice_index = len(prob_subtree_slices) - 1
				while slice_index >= 0:
					
					new_list = []

					# make a new list of every node in the tree
					for node in tree:
						new_list.append(node.name)				

					# if root of this slice is a condition node change it to ifInNest
					if new_list[tree_index] in self.conditionNodes:
						new_list[tree_index] = self.changeConditionNode(new_list[tree_index])
					
					# rewrite the tree now condition nodes have been changed (trailing param is just for debugging)
					tree = self.buildNewTreeFromList(trailing, new_list, indent)
					
					# also update this subtree to match the updated tree
					subtree = self.updateSubtree(tree, slices, parent)
					
					# proceed to previous subtree for next loop
					slice_index -= 1
					tree_index -= prob_subtree_slices[slice_index].stop - prob_subtree_slices[slice_index].start

			# self.printMessage(indent, "removed last time: "+str(removed_node_last_time)+" and count: "+str(count))

		return tree

	def rebuildTree(self, tree, slice_, trailing, first, last):
		
		lastParam = last
		subtreeSlice = slice_
		subtreeChromosome = tree[slice_]
		subtree = gp.PrimitiveTree(subtreeChromosome)
		
		lenCount = slice_.start + 1
		limit = slice_.stop
		slices = []
		subtrees = []

		# get the slices and strings for each subtree
		while (lenCount < limit):
			slice_ = tree.searchSubtree(lenCount)
			chromosome = tree[slice_]
			subSubtree = gp.PrimitiveTree(chromosome)
			slices.append(slice_)
			subtrees.append(str(subSubtree))
			lenCount += len(subSubtree)
		
		
		activeSubtree = False
		probNodeStatus = False
		nextSubtreeActive = False # from parseSubtree
		removed_node_last_time = False
		
		# going backwards through all slices
		for i in range(len(slices) - 1, -1, -1):
		
			activeSubtreeThisIteration = False
			chromosome = tree[slices[i]]
			subSubtree = gp.PrimitiveTree(chromosome)
			
			# if not first time round loop and a subtree has already been marked as active and the next (prev
			# in loop) subtree is active and this isn't a probability node then this is not the last subtree
			if i < len(slices) - 1 and activeSubtree and nextSubtreeActive and subtree[0].name not in self.probabilityNodes:
				last = False
			
			# check subtree for actions and make activeSubtree true if trailingList entry for this
			# slice's root node is true and it isn't already
			activity = self.parseSubtreeActivityWithProbabilityNodesToo(subSubtree)
			if self.trailingList[slices[i].start]:
				activeSubtree = ((activeSubtree and subtree[0].name not in self.probabilityNodes) or activity)
				activeSubtreeThisIteration = ((activeSubtree and subtree[0].name not in self.probabilityNodes) or activity)
			
			parent_name = subtree[0].name
			
			# if this is the last subtree which could have actions and doesn't have any actions
			if last and not activeSubtreeThisIteration:
				
				# if it isn't a probability node make all associated trailingList entries False
				if subtree[0].name not in self.probabilityNodes:
					parent_name = subtree[0].name[0:-1] + str(int(subtree[0].name[-1]) - 1)
					parent_index = slices[0].start - 1
					# print(subtree[0].name+" to "+parent_name+" (index "+str(parent_index)+")")
					new_list = []
					for node in tree:
						new_list.append(node.name)				
					del new_list[slices[i].start:slices[i].stop]
					
					if parent_name[-1] == "1":
						del new_list[parent_index]
					else:	
						new_list[parent_index] = parent_name
					
					new_chromosome = ""
					for node in new_list:
						new_chromosome += node + " "
					new_chromosome = new_chromosome[0:-1]
					
					new_tree = self.primitivetree.from_string(new_chromosome, self.pset)
					tree = new_tree
					
					slice_start = slices[0].start - 1
					slice_stop = slices[int(subtree[0].name[-1]) - 1].stop
					subtree = new_tree[slice_start:slice_stop]
					
					if parent_name[-1] == "1":
						removed_node_last_time = True
						break
					
				else:
					for j in range(slices[i].start, slices[i].stop):
						if not activity:
							# parent_name = subtree[0].name[0:-1] + str(int(subtree[0].name[-1]) - 1)
							# parent_index = slices[0].start - 1
							# print(subtree[0].name+" to "+parent_name+" (index "+str(parent_index)+")")
							new_list = []
							for node in tree:
								new_list.append(node.name)				
							new_list[j] = "stop"
							trailing[j] = True
							
							# if parent_name[-1] == "1":
								# del new_list[parent_index]
							# else:	
								# new_list[parent_index] = parent_name
							
							new_chromosome = ""
							for node in new_list:
								new_chromosome += node + " "
							new_chromosome = new_chromosome[0:-1]
							
							new_tree = self.primitivetree.from_string(new_chromosome, self.pset)
							tree = new_tree
							slice_start = slices[0].start - 1
							slice_stop = slices[int(subtree[0].name[-1]) - 1].stop
							subtree = new_tree[slice_start:slice_stop]
							
							
							# if parent_name[-1] == "1":
								# removed_node_last_time = True
								# break
								
			# otherwise recursively descend into this subtree
			else:
				if not removed_node_last_time:
					probNodeStatus = True
					trailingSubtree = last
					first += 1
					if (first < 100):
						new_tree = self.rebuildTree(tree, slices[i], trailing, first, trailingSubtree)
						tree = new_tree
						slice_start = slices[0].start - 1
						slice_stop = slices[int(subtree[0].name[-1]) - 1].stop
						subtree = new_tree[slice_start:slice_stop]
			
			# if we didn't set trailinglist for the root node of this subtree to False we
			# record that this subtree is active for next time round the loop
			if self.trailingList[slices[i].start]:
				nextSubtreeActive = True
		
		# if this whole function was called on the (or a) last (sub?)tree and the root is a
		# probability node and the whole subtree is inactive mark the whole thing false in trailinglist
		if lastParam and subtree[0].name in self.probabilityNodes and not probNodeStatus:
			
			for i in range(subtreeSlice.start, subtreeSlice.stop):
					
				parent_name = subtree[0].name[0:-1] + str(int(subtree[0].name[-1]) - 1)
				parent_index = slices[0].start - 1
				# print(subtree[0].name+" to "+parent_name+" (index "+str(parent_index)+")")
				new_list = []
				for node in tree:
					new_list.append(node.name)				
				new_list[i] = "stop"
				trailing[j] = True
				# if parent_name[-1] == "1":
					# del new_list[parent_index]
				# else:	
					# new_list[parent_index] = parent_name
							
				
				new_chromosome = ""
				for node in new_list:
					new_chromosome += node + " "
				new_chromosome = new_chromosome[0:-1]
				
				new_tree = self.primitivetree.from_string(new_chromosome, self.pset)
				tree = new_tree
				
				slice_start = slices[0].start - 1
				slice_stop = slices[int(subtree[0].name[-1]) - 1].stop
				subtree = new_tree[slice_start:slice_stop]
				
				self.trailingList[i] = False
		
		return tree

	def rebuildChromosome2(self, tree):
		
		childrenRemaining = []
		chromosome = ""
		
		for i in range(len(tree)):
			
			node = tree[i]
			
			if node.lower() in self.sequenceNodes + self.fallbackNodes + self.probabilityNodes:
				if len(childrenRemaining) > 0: childrenRemaining[-1] -= 1
				children = int(node[-1])			
				childrenRemaining.append(children)
				chromosome += node +"("
			
			else:	
				if len(childrenRemaining) > 0 and childrenRemaining[-1] > 1: chromosome += node + ", "
				else: chromosome += node
				if len(childrenRemaining) > 0: childrenRemaining[-1] -= 1
				
			if len(childrenRemaining) == 0 or childrenRemaining[-1] == 0:
				for childQty in reversed(childrenRemaining):
					if childQty == 0: 
						childrenRemaining.pop()
						chromosome += ")"
					else: break
				if len(childrenRemaining) > 0 and childrenRemaining[-1] > 0 and i < len(output) - 1:
					chromosome += ", "
			
		for node in childrenRemaining:
			chromosome += ")"
		
		# print chromosome
		return chromosome

	def rebuildChromosome(self, output):
		
		childrenRemaining = []
		chromosome = ""
		
		for i in range(len(output)):
			
			node = output[i]
			
			if node.lower() in self.sequenceNodes + self.fallbackNodes + self.probabilityNodes:
				if len(childrenRemaining) > 0: childrenRemaining[-1] -= 1
				children = int(node[-1])			
				childrenRemaining.append(children)
				chromosome += node +"("
			
			else:	
				if len(childrenRemaining) > 0 and childrenRemaining[-1] > 1: chromosome += node + ", "
				else: chromosome += node
				if len(childrenRemaining) > 0: childrenRemaining[-1] -= 1
				
			if len(childrenRemaining) == 0 or childrenRemaining[-1] == 0:
				for childQty in reversed(childrenRemaining):
					if childQty == 0: 
						childrenRemaining.pop()
						chromosome += ")"
					else: break
				if len(childrenRemaining) > 0 and childrenRemaining[-1] > 0 and i < len(output) - 1:
					chromosome += ", "
			
		for node in childrenRemaining:
			chromosome += ")"
		
		# print chromosome
		return chromosome

	def printTree(self, tree):
		
		string = ""
		stack = []
		for node in tree:
			stack.append((node, []))
			while len(stack[-1][1]) == stack[-1][0].arity:
				prim, args = stack.pop()
				string = prim.format(*args)
				if (string[1:4].find(".") >= 0): string = string[0:5]
				if len(stack) == 0:
					break  # If stack is empty, all nodes should have been seen
				stack[-1][1].append(string)

		return string
		
	def formatChromosome(self, chromosome):
		
		tree = ""
		indent = ""
		lineEnding = "\n"
		
		childrenRemaining = []
		insideComposite = 0
		insideSubtree = True
		
		for i in range(len(chromosome)):
			
			node = chromosome[i].name
			
			# ======= inner nodes =======
			
			if node.lower() in self.sequenceNodes + self.fallbackNodes + self.probabilityNodes:
				
				if len(childrenRemaining) > 0: childrenRemaining[-1] -= 1
				
				childrenRemaining.append(int(node[-1]))
				
				# check if any children are inner nodes
				insideSubtree = False
				composites = 0
				j = i + 1
				limit = j + childrenRemaining[-1]
				while j < limit:
					if chromosome[j].name.lower() in self.sequenceNodes + self.fallbackNodes + self.probabilityNodes:
						insideSubtree = True
						break
					# if chromosome[j].lower() in self.compositeNodes:
						# limit += 2
					j += 1
				
				# if all children are terminals print them on one line
				if insideSubtree:
					tree += indent + node +"(" + lineEnding
					indent += "   "
				else:
					lineEnding = ""
					tree += indent + node +"("
			
			# ==== composite nodes ====
			
			# elif node.lower() in self.compositeNodes:
				# if len(childrenRemaining) > 0: childrenRemaining[-1] -= 1
				# if insideSubtree: tree += indent
				# tree += node + "(" + chromosome[i+1] + ", " + chromosome[i+2] + ")"
				# if len(childrenRemaining) > 0 and childrenRemaining[-1] > 0: tree += ", "
				# tree += lineEnding
				# insideComposite = 2
				
			# elif insideComposite > 0:
				# insideComposite -= 1
				# continue
			
			# ======= terminals =======
			
			else:
				comma = ", " if len(childrenRemaining) > 0 and childrenRemaining[-1] > 1 else ""
				if insideSubtree: tree += indent
				tree += node + comma + lineEnding
				if len(childrenRemaining) > 0: childrenRemaining[-1] -= 1
			
			# ==== closing brackets ====
			
			if len(childrenRemaining) == 0 or childrenRemaining[-1] == 0:
				for i in range(len(childrenRemaining) - 1, -1, -1):
					if childrenRemaining[i] == 0: 
						childrenRemaining.pop()
						if insideSubtree: 
							indent = indent[0:-3]
							tree += indent
						insideSubtree = True
						lineEnding = "\n"
						comma = "" if i == 0 or childrenRemaining[i-1] == 0 else ", "
						tree += ")" + comma + lineEnding
					else: break
		
		return tree

	def evaluateRobot(self, individual, thread_index=1):
		
		# print ("")
		# print ("evaluate")
		# print (individual)
		
		# save number of robots and chromosome to file
		with open('../txt/chromosome'+str(thread_index)+'.txt', 'w') as f:
			f.write(str(self.params.sqrtRobots))
			f.write("\n")
			f.write(str(individual))
		
		totals = []
		# qdpy optimisation
		# for i in range(self.params.features):
		for i in range(self.params.features + 3):
			# end qdpy
			totals.append(0.0)
		
		robots = {}
		seed = 0
		
		for i in self.params.arenaParams:
			
			# get maximum food available with the current gap between the nest and food
			# maxFood = self.calculateMaxFood(i)
			
			# for j in range(self.params.iterations):
			
			# write seed to file
			seed += 1
			with open('../txt/seed'+str(thread_index)+'.txt', 'w') as f:
				f.write(str(seed))
				f.write("\n")
				f.write(str(i))

			# run argos
			subprocess.call(["/bin/bash", "../evaluate"+str(thread_index), "", "./"])
			
			# result from file
			with open("../txt/result"+str(thread_index)+".txt", "r") as f:
				
				# print ("")
				for line in f:
					first = line[0:line.find(" ")]
					if (first == "result"):
						# print (line[0:-1])
						lines = line.split()
						robotId = int(float(lines[1]))
						robots[robotId] = []
						for j in range(self.params.features):
							for k in range(self.params.iterations):
								index = (j * self.params.iterations) + k + 2
								robots[robotId].append(float(lines[index]))
						# qdpy optimisation
						for j in range(3):
							for k in range(self.params.iterations):
								index = (j * self.params.iterations) + (self.params.features * self.params.iterations) + k + 2
								robots[robotId].append(float(lines[index]))
						# end qdpy
						# string = str(robotId)+" "
						# for s in robots[robotId][15:20]:
							# string += str(s)+" "
						# print (string)
			
			# get scores for each robot and add to cumulative total
			# qdpy optimisation
			# for k in range(self.params.features):
			for k in range(self.params.features + 3):
				# end qdpy
				totals[k] += self.collectFitnessScore(robots, k)
				# print (totals[k])
			
			# increment counter and pause to free up CPU
			time.sleep(self.params.trialSleep)
		
		# divide to get average per seed and arena configuration then apply derating factor
		# deratingFactor = self.deratingFactor(individual)
		deratingFactor = 1.0
		features = []
		# qdpy optimisation
		# for i in range(self.params.features):
		for i in range(self.params.features + 3):
			# end qdpy
			features.append(self.getAvgAndDerate(totals[i], individual, deratingFactor))
		
		# pause to free up CPU
		time.sleep(self.params.evalSleep)
		
		# output = ""
		# for f in features:
			# output += str("%.9f" % f) + " \t"
		# print (output)
		
		return (features)

	def collectFitnessScore(self, robots, feature, maxScore = 1.0):

		thisFitness = 0.0
		fitnessString = ""
		
		# get food collected by each robot and add to cumulative total
		for r in (range(len(robots))):
			# print (robots[r])
			for i in range(self.params.iterations):
				index = (feature * self.params.iterations) + i
				thisFitness += float(robots[r][index])
				fitnessString += "," + str(robots[r][index])
		# print (fitnessString)
		# print (thisFitness)
		
		# divide to get average for this iteration, normalise and add to running total
		thisFitness /= self.params.sqrtRobots * self.params.sqrtRobots
		thisFitness /= maxScore
		# print (thisFitness)
		# print ("----")
		return thisFitness
	
	def getAvgAndDerate(self, score, individual, deratingFactor):
		# print (score)
		fitness = score / self.params.iterations
		fitness = fitness / len(self.params.arenaParams)
		# print (fitness)
		fitness /= deratingFactor
		return fitness

		
	def is_number(self, s):
		try:
			float(s)
			return True
		except ValueError:
			return False

