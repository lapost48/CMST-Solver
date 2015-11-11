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
		while not self.individuals.empty():
			temp.put(self.individuals.get())
		while not self.individuals.full() and not temp.empty():
			self.individuals.put(temp.get())
			
	def update(self, pop):
		pop.sort()
		best_candidates = pop[0:self.size]
#		for ind in best_candidates:
#			print ind.get_fitness(),
#		print ""
		for individual in best_candidates:
			self.add(individual)