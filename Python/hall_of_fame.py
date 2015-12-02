# Nick LaPosta
# Advanced Concepts in Artificial Intelligence Project
#     Genetic MST Generator
import Queue as q

class hof:
	
	def __init__(self, size):
		self.individuals = q.Queue(size)
		self.size = size

	def add(self, individual):
		temp = q.PriorityQueue()
		in_queue = False
		while not self.individuals.empty():
			old_ind = self.individuals.get()
			if individual == old_ind:
				in_queue = True
			temp.put(old_ind)

		if not in_queue:
			temp.put(individual)

		while not self.individuals.full() and not temp.empty():
			self.individuals.put(temp.get())
			
	def update(self, pop):
		pop.sort()
		best_candidates = pop[0:self.size]
		for individual in best_candidates:
			self.add(individual)

	def __str__(self):
		ret = ''
		while not self.individuals.empty():
			ind = self.individuals.get()
#			ret += "Individual: " + str(ind) + "\n"
			ret += "Fitness: " + str(ind.get_fitness()) + "\n"
			ret += "Tree: " + str(ind.tree)
			ret += "\n\n"
		return ret
