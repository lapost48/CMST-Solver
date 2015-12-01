# Nick LaPosta
# Advanced Concepts in Artificial Intelligence Project
#     Genetic MST Generator
from __future__ import division
import random
import individual
import hall_of_fame
import sys

ADJACENCY_MATRIX = []
NUM_NODES = 0
INDEX_RANGE = 255
MINIMIZE = True

# TODO: Make adjacency matrix from input graph

def random_adjacency_matrix():
	print "Make Matrix"
	global ADJACENCY_MATRIX
	ADJACENCY_MATRIX = [[0 for x in xrange(NUM_NODES)]
			    for x in xrange(NUM_NODES)]
	print "Fill Matrix: Not done"
	for col in xrange(len(ADJACENCY_MATRIX)):
		for row in xrange(len(ADJACENCY_MATRIX[col])):
			ADJACENCY_MATRIX[col][row] = random.randint(0, 100) if col != row else sys.maxint
#			print ADJACENCY_MATRIX[col][row],
#		print ""

def fitness_evaluation(individuals):
	global NUM_NODES
	for ind in individuals:
		# Create Cost Matrix for Representation
		genome = ind.genome
		matrix = [[sys.maxint for x in xrange(NUM_NODES)]
			  for x in xrange(NUM_NODES)]
		for col in xrange(len(matrix)):
			for row in xrange(len(matrix[col])):
				if row != col:
					L = max(row, col)
					S = min(row, col)
					index = L * (L - 1) / 2
					index += S - 1
					index -= L
					matrix[col][row] =  genome[row]
					matrix[col][row] += genome[col]
					matrix[col][row] += genome[int(index)]
#				print matrix[col][row],
#			print ""
#		print ""
		ind.fitness = random.randint(1, 255)
		# Apply Prim's Algorithm to get Tree
		tree = prim(matrix)
		# TODO: Get Validity of Tree

		# Get weight of converted representation
		weight = 0
		for edge in tree:
			(col, row) = edge
			weight += ADJACENCY_MATRIX[col - 1][row - 1]
		ind.tree = tree
		ind.fitness = weight

def prim(matrix):
	nodes = [1]
	tree = []
	while len(tree) < NUM_NODES - 1:
		# Get all edges connected to the current tree
		poss_edges = {}
		minimum = sys.maxint
		for col in nodes:
			for row in xrange(len(matrix[col - 1])):
				if not row + 1 in nodes:
					poss_edges[(col, row + 1)] = matrix[col - 1][row]
		# Choose smallest edge
		smallest = ((0, 0), sys.maxint)
		for edge, weight in poss_edges.iteritems():
			if weight < smallest[1]:
				smallest = (edge, weight)
		# Add edge to tree
		tree.append(smallest[0])
		nodes.append(smallest[0][1])
	return tree

def crossover(individuals, crossover_pb):
	group_A = list()
	group_B = list()

	# TODO: Make roulette mating work
	# Math consultation from Winston Cheong
#	summation = 0
#	for ind in individuals:
#		summation += 1 / ind.fitness
#	choices = {(1 / ind.fitness) for ind in individuals}
#	pick = random.uniform(0, summation)
	

	while individuals:
		group_A.append(individuals.pop())
		group_B.append(individuals.pop())
	
	ret = list()
	for i in xrange(len(group_A)):
		ind1 = group_A.pop()
		ind2 = group_B.pop()
		for i in xrange(random.randint(1, len(ind1))):
			temp = ind1[i]
			ind1[i] = ind2[i]
			ind2[i] = temp
		ret.append(ind1)
		ret.append(ind2)
	return ret

# Mutates each chromosome of the entire population
#     based on a mutation probability
# This function runs in O(num_individuals * length of an individual) / O(n*l)
def mutation(individuals, mutation_pb):
	for individual in individuals:
		for value in individual:
			if random.random() < mutation_pb:
				value = random.randrange(0, INDEX_RANGE)
	return individuals
	
# Mutates each individual in the entire population
#     based on a mutation probability
# This function runs in O(num_individuals) / O(n)
def mutation_quick(individuals, mutation_pb):
	for individual in individuals:
		if random.random() < mutation_pb:
			individual[random.random * len(individual)] = random.randrange(0, INDEX_RANGE)
	return individuals

# This function generates a population using the individual generator
def generate_population(num_individuals, ind_size):
	generated_pop = list()
	for _ in xrange(num_individuals):
		generated_pop.append(
			individual.individual(ind_size, MINIMIZE, INDEX_RANGE))
	return generated_pop
	
# This is the main function that executes the genetic algorithm
def main(pop_size, graph_file, cross_pb, mut_pb, num_gen, hof_size):
	global NUM_NODES
	NUM_NODES = num_nodes
	# TODO: Graph input
	random_adjacency_matrix()
	# Hall Of Fame is terminology from deap but
	#     I like it so I am giving it credit here
	hof = hall_of_fame.hof(hof_size)
	population = generate_population(pop_size + (pop_size % 2)
					,int(num_nodes * (num_nodes + 1) / 2))
	fitness_evaluation(population)
	hof.update(population)
	for _ in range(num_gen):
		children = crossover(population, cross_pb)
		population = mutation(children, mut_pb)
		fitness_evaluation(population)
		hof.update(population)
	print hof
		
if __name__=="__main__":
#	main(100, sys.argv[1], 0.7, 0.2, 200, 3))
	main(100, 5, .7, .2, 200, 3)
