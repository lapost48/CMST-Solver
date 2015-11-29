# Nick LaPosta
# Advanced Concepts in Artificial Intelligence Project
#     Genetic MST Generator
import random

class individual:

	def __init__(self, size, min, range):
		self.fitness = 0
		self.genome = [random.randint(0, range) for i in xrange(size)]
		if min:
			self.fit_mod = 1
		else:
			self.fit_mod = -1
			
	def __iter__(self):
		return iter(self.genome)

	def set_fitness(self, value):
		self.fitness = value * self.fit_mod
		
	# I don't see this being used but it is in place so that if I do
	#     need it I have it
	def get_fitness(self):
		return self.fitness * self.fit_mod

	def __getitem__(self, index):
		return self.genome[index]

	def __setitem__(self, index, value):
		self.genome[index] = value

	def __cmp__(self, other):
		return cmp(self.fitness, other.fitness)

	def __len__(self):
		return len(self.genome)

	def __str__(self):
		ret = ''
		for i in self.genome:
			ret += str(i) + " "
		return ret
