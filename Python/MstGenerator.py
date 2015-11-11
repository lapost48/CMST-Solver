# Nick LaPosta
# Advanced Concepts in Artificial Intelligence Project
#     Genetic MST Generator
import random
import individual
import hall_of_fame

INDEX_RANGE = 10
MINIMIZE = True

# TODO: Fitness functionality. Figure out how it works with your representation
def fitness_evaluation(individuals):
	for ind in individuals:
		ind.set_fitness(random.randrange(0, 2000))

# TODO: Crossover functionality
def crossover(individuals, crossover_pb):


	return individuals
	
# Mutates each chromosome of the entire population based on a mutation probability
# This function runs in O(num_individuals * length of an individual) / O(n*l)
def mutation(individuals, mutation_pb):
	for individual in individuals:
		for value in individual:
			if random.random() > mutation_pb:
				value = random.randrange(0, INDEX_RANGE)
	return individuals
	
# Mutates each individual in the entire population based on a mutation probability
# This function runs in O(num_individuals) / O(n)
def mutation_quick(individuals, mutation_pb):
	for individual in individuals:
		if random.random() > mutation_pb:
			# TODO: This will have to be modified to work with the actual structure of the individuals
			individual[random.random * len(individual)] = random.randrange(0, INDEX_RANGE)
	return individuals

# This function generates a population using the individual generator
def generate_population(num_individuals, ind_size):
	generated_pop = list()
	for i in range(num_individuals):
		generated_pop.append(individual.generate_individual(ind_size, MINIMIZE))
	return generated_pop
	
# This is the main function that executes the genetic algorithm
def main(pop_size, ind_size, cross_pb, mut_pb, num_gen, hof_size):
	# Hall Of Fame is terminology from deap but I like it so I am giving it credit here
	hof = hall_of_fame.hof(hof_size)
	population = generate_population(pop_size, ind_size)
	for _ in range(num_gen):
		fitness_evaluation(population)
		children = crossover(population, cross_pb)
		children = mutation(children, mut_pb)
		hof.update(population)
		
if __name__=="__main__":
# Use this main line when experimenting with values through a command line or something
#	main(args[0], args[1], args[2], args[3], args[4], args[5])
	main(100, 5, .7, .02, 100, 3)