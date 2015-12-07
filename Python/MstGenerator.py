# Nick LaPosta
# Advanced Concepts in Artificial Intelligence Project
#     Genetic MST Generator
from __future__ import division
import random
import individual
import hall_of_fame
import progress
import sys
import time

ADJACENCY_MATRIX = []
TOURNAMENT_SIZE = 10
NUM_NODES = 0
INDEX_RANGE = 256
MINIMIZE = True
ROOT = 0
CAPACITY = 0
MAXIMUM_FITNESS = 0

def random_adjacency_matrix():
	global MAXIMUM_FITNESS
	global ADJACENCY_MATRIX
	ADJACENCY_MATRIX = [[0 for x in xrange(NUM_NODES)]
			    for x in xrange(NUM_NODES)]
	for col in xrange(len(ADJACENCY_MATRIX)):
		for row in xrange(col, len(ADJACENCY_MATRIX[col])):
			value = random.randint(0, 100) if col != row else sys.maxint
			ADJACENCY_MATRIX[col][row] = value
			ADJACENCY_MATRIX[row][col] = value
			
			if row != col:
				if value > MAXIMUM_FITNESS:
					MAXIMUM_FITNESS = value
				print ADJACENCY_MATRIX[col][row],
		print ""
	print MAXIMUM_FITNESS
	MAXIMUM_FITNESS *= NUM_NODES

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
					index += NUM_NODES
					matrix[col][row] =  genome[row]
					matrix[col][row] += genome[col]
					matrix[col][row] += genome[int(index)]
		ind.fitness = random.randint(1, 255)

		# Apply Prim's Algorithm to get Tree
		tree = prim(matrix)

		# Depth search starting from ROOT
		over_capacity = False
		for edge in tree:
			b_weight = 0
			if edge[0] == ROOT:
				b_weight = measure_branch(tree, edge[1], ROOT)
			elif edge[1] == ROOT:
				b_weight = measure_branch(tree, edge[0], ROOT)
			if b_weight > CAPACITY:
				ind.tree = tree
				ind.fitness = MAXIMUM_FITNESS
				over_capacity = True

		# Get weight of converted representation if under capacity
		if not over_capacity:
			weight = 0
			for edge in tree:
				(col, row) = edge
				weight += ADJACENCY_MATRIX[col - 1][row - 1]
			ind.tree = tree
			ind.fitness = weight

# This function counts the number of nodes on a branch starting at a node
def measure_branch(tree, parent, prev):
	weight = 0
	for edge in tree:
		if  edge[0] == parent and edge[1] != prev:
			weight += measure_branch(tree, edge[1], parent)
		elif edge[0] != prev and edge[1] == parent:
			weight += measure_branch(tree, edge[0], parent)
	return weight + 1

# Applies Prim's Algorithm to find MSTs
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

# Selects and crosses parent individuals to create new offspring
def crossover(individuals, crossover_pb):
	group_A = list()
	group_B = list()

	# Tournament style mating selection
	mating_group = list()
	while len(mating_group) < len(individuals):
		best = None
		for i in xrange(TOURNAMENT_SIZE):
			ind = individuals[random.randint(0, len(individuals) - 1)]
			if best is None or ind.fitness > best.fitness:
				best = ind
		mating_group.append(best)

	while mating_group:
		group_A.append(mating_group.pop())
		group_B.append(mating_group.pop())
	
	ret = list()
	for i in xrange(len(group_A)):
		ind1 = group_A.pop()
		ind2 = group_B.pop()
		if random.random() < crossover_pb:
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
			individual[int(random.random() * len(individual))] = random.randrange(0, INDEX_RANGE)
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
	global TOURNAMENT_SIZE
	TOURNAMENT_SIZE = 20

	global NUM_NODES
	NUM_NODES = int(graph_file)

	global ROOT
	ROOT = random.randint(1, NUM_NODES)

	global CAPACITY
	CAPACITY = random.randint(3, NUM_NODES)

	random_adjacency_matrix()

	# Hall Of Fame is terminology from deap but
	#     I like it so I am giving it credit here
	hof = hall_of_fame.hof(hof_size)

	population = generate_population(pop_size + (pop_size % 2)
					,int(NUM_NODES * (NUM_NODES + 1) / 2))

	fitness_evaluation(population)
	hof.update(population)

	start = time.clock()

	progress.startProgress("Generation Progress")

	# GA Execution
	# Mutation function can be changed from here
	for cur_gen in range(num_gen):
		children = crossover(population, cross_pb)
		population = mutation(children, mut_pb)
		fitness_evaluation(population)
		hof.update(population)
		progress.progress((cur_gen / num_gen) * 100)

	progress.endProgress()

	print hof
	print "Time: ", time.clock() - start
	print "ROOT: ", ROOT
	print "CAPACITY: ", CAPACITY
#	comp = prim(ADJACENCY_MATRIX)
#	weight = 0
#	for edge in comp:
#		(col, row) = edge
#		weight += ADJACENCY_MATRIX[col - 1][row - 1]
#	print "Weight: ", weight

		
if __name__=="__main__":
	main(150, sys.argv[1], 0.7, 0.02, 200, 3)
#	main(100, 20, .7, .2, 200, 3)
