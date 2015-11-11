# Nick LaPosta
# Advanced Concepts in Artificial Intelligence Project
#     Genetic MST Generator

# TODO: Actually generate individuals
def generate_individual(num_nodes, min):
	return individual(num_nodes, min) # To be replaced with actual
									  #     individual object

class individual:

	def __init__(self, size, minimize):
		self.fitness = 0
		if minimize:
			self.fit_mod = 1
		else:
			self.fit_mod = -1
			
	def __iter__(self):
		return self
		
	def next(self):
		raise StopIteration
		
	def set_fitness(self, value):
		self.fitness = value * self.fit_mod
		
	# I don't see this being used but it is in place so that if I do
	#     need it I have it
	def get_fitness(self):
		return self.fitness * self.fit_mod

	def __cmp__(self, other):
		return cmp(self.fitness, other.fitness)