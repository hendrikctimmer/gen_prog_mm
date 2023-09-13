import numpy as np
import random
import copy
import time
from Algorithm import Algorithm

class Matmul:

	"""Object is initialized with number of triples as parameter, where the triple is
	a triple of matrices (a,b,c), such that a*b=c. 
	
	"""

	def __init__(self, num_triples, verbose = False, cells_priority = False):


		self.mat_triples = []           		#List of triples of matrices in form [a,b,c] where a * b = c
		self.mat_size = [5,5]
		self.start_terms = self.mat_size[0] * self.mat_size[0] * self.mat_size[1]
		self.num_triples = num_triples
		self.SMALL = 2
		self.MEDIUM = 5
		self.LARGE = 10
		self.num_terms = self.mat_size[0] * self.mat_size[0] * self.mat_size[1]
		self.algo = Algorithm()
		self.verbose = verbose					#Toggle verbose mode for debugging
		self.cells_priority = cells_priority	#Toggle cell priority mode, where cell fitness is prioritized
		self.h_added = 0

		
	def init_mats(self, num_triples):
		
		for x in range(num_triples):
		
			m1 = np.random.randint(low=-10, high=11, size=(self.mat_size[0], self.mat_size[1]))
			m2 = np.random.randint(low=-10, high=11, size=(self.mat_size[0], self.mat_size[1]))
			m3 = np.matmul(m1,m2)
			
			mat = (m1,m2,m3)
			
			self.mat_triples.append(mat)

	def rand_algo(self, term_size, num_terms):			#Method that initiates a random algorithm

		res = Algorithm()

		for x in range(num_terms):

			h_term_list = self.make_h_list(term_size)
			h_term = self.make_h(h_term_list)

			res.h_term_lists[f"h{x+1}"] = h_term_list
			res.mult_algo[f"h{x+1}"] = h_term

		for x in range(self.mat_size[0]):
			for y in range(self.mat_size[1]):

				c_term_list = self.make_c_list(term_size)
				c_term = self.make_c(c_term_list)

				res.c_term_lists[f"c{x+1}{y+1}"] = c_term_list
				res.mult_algo[f"c{x+1}{y+1}"] = c_term

		return res

	def make_ab_term(self, term_size):
		prob = random.uniform(0, 1)
		term_to_add = ""
		if prob > 0.5:
			term_to_add += " - "
		term_to_add += random.choice(["a", "b"])
		term_to_add += f"{random.randint(1,self.mat_size[0])}"
		term_to_add += f"{random.randint(1,self.mat_size[1])}"

		return term_to_add

	def make_h_list(self, term_size):
		
		h_term_list = []

		for x in range(term_size):
			h_term_list.append(self.make_ab_term(term_size))

		if self.one_sided_h(h_term_list):
			h_term_list = self.make_h_list(term_size)

		return h_term_list

	def make_h(self, h_term_list):

		h_term_a = ""
		h_term_b = ""

		for z in h_term_list:
			if "a" in z and "-" not in z:
				h_term_a += " + " + z
		for z in h_term_list:
			if "a" in z and "-" in z:
				h_term_a += z
		for z in h_term_list:
			if "b" in z and "-" not in z:
				h_term_b += " + " + z
		for z in h_term_list:
			if "b" in z and "-" in z:
				h_term_b += z + " "

		# This can all be done in a much cleaner way probably
		h_term_a = h_term_a.strip()
		h_term_b = h_term_b.strip()
		h_term_a = h_term_a.strip("+")
		h_term_b = h_term_b.strip("+")
		h_term_a = h_term_a.strip()
		h_term_b = h_term_b.strip()
		h_term_a = "(" + h_term_a + ")"
		h_term_b = "(" + h_term_b + ")"
		if h_term_a[2] == " ":
			h_term_a = h_term_a.replace(" ", "", 1)
		if h_term_b[2] == " ":
			h_term_b = h_term_b.replace(" ", "", 1)

		h_term = h_term_a + " * " + h_term_b

		return h_term

	def make_c_list(self, term_size):

		c_term_list = []

		for x in range(term_size):
			prob = random.uniform(0, 1)
			term_to_add = ""
			if prob > 0.5:
				term_to_add += " - "
			term_to_add += "h"
			term_to_add += f"{random.randint(1,self.num_terms)}"
			c_term_list.append(term_to_add)

		return c_term_list

	def make_c(self, c_term_list):

		c_term = ""

		for z in c_term_list:
			if "-" not in z:
				c_term += " + " + z
		for z in c_term_list:
			if "-" in z:
				c_term += z
		c_term = c_term.strip()
		c_term = c_term.strip("+")
		c_term = c_term.strip()
		c_term = c_term + " "
		if c_term[1] == " ":
			c_term = c_term.replace(" ", "", 1)

		return c_term


	def one_sided_h(self, h_list):

		#Checks whether an h-term has only a's or only b's

		num_a = 0
		num_b = 0

		for x in h_list:
			if "a" in x:
				num_a +=1
			elif "b" in x:
				num_b +=1

		if num_a == 0 or num_b == 0:
			return True
		else:
			return False

	"""
	def init_pop(self, pop_size):

		for x in range(pop_size):
			self.population.append(self.rand_algo(self.MEDIUM, self.num_terms))
	"""

	def print_algo(self, algo):
		for x in algo.h_term_lists.keys():
			print(x + ": ", algo.mult_algo[x])
			

		print("\n")

		for x in range(self.mat_size[0]):
			for y in range(self.mat_size[1]):
				print(f"c{x+1}{y+1}: ", "(" + algo.mult_algo[f"c{x+1}{y+1}"] + ")")
				
#-----------------------------------------------------------------RUSTIFICATION LINE------------------------------------------------------------------------------#

	def mutate(self, algorithm, term_size):

		"""
		1: Add h
		2: Remove h
		3: Add (+/-)a to h
		4: Add (+/-)b to h
		5: Remove a from h
		6: Remove b from h
		7: Add (+/-)h to c
		8: Remove h from c
		 
		"""

		#mutation_type = 8 #for debugging mutations
		mutation_type = np.float64(random.randint(1,8))

		#print("Mutation type: ", mutation_type)

		if mutation_type == 1:

			if self.verbose:
				print("Mutation type: New h")

			h_to_add = f"h{self.num_terms+1}"

			new_h_list = self.make_h_list(term_size)
			new_h = self.make_h(new_h_list)
			
			algorithm.h_term_lists[f"h{self.num_terms+1}"] = new_h_list
			algorithm.mult_algo[f"h{self.num_terms+1}"] = new_h


			#Also add this new h to one of the c's

			c_to_add_to = f"c{random.randint(1,self.mat_size[0])}{random.randint(1,self.mat_size[0])}"

			if random.randint(0,1) == 1:
				h_to_add = " - " + h_to_add

			#print("h to add: ", h_to_add)

			#print("old c list: ", algorithm.c_term_lists[c_to_add_to])
			#print("old c: ", algorithm.mult_algo[c_to_add_to])

			algorithm.c_term_lists[c_to_add_to].append(h_to_add)
			algorithm.mult_algo[c_to_add_to] = self.make_c(algorithm.c_term_lists[c_to_add_to])

			#print("new c list: ", algorithm.c_term_lists[c_to_add_to])
			#print("new c: ", algorithm.mult_algo[c_to_add_to])

			
			self.h_added += 1
			self.num_terms += 1

		elif mutation_type == 2:

			if self.verbose:
				print("Mutation type: Remove h")

			unremovable_h_list = [] #A list of h's that are the only one in a particular c and can therefore not be removed because a c must contain at least 1 term

			go_break = False

			for row in range(self.mat_size[0]):		#This loop checks all c terms to see how many h terms they contain. If it is 1, then the h in that c term is added to the "unremovable" list
				for col in range(self.mat_size[1]):
					if len(algorithm.c_term_lists[f"c{row+1}{col+1}"]) == 1:
						if "-" in algorithm.c_term_lists[f"c{row+1}{col+1}"][0]:
							unremovable_h_list.append(algorithm.c_term_lists[f"c{row+1}{col+1}"][0][3:])
						else:
							unremovable_h_list.append(algorithm.c_term_lists[f"c{row+1}{col+1}"][0])
					else:		#This part checks whether a c term that contains multiple h terms contains only multiple of the same h term, if so, that h is added to the "unremovable" list
						count = 0
						h = algorithm.c_term_lists[f"c{row+1}{col+1}"][0]
						for x in range(len(algorithm.c_term_lists[f"c{row+1}{col+1}"])):
							if algorithm.c_term_lists[f"c{row+1}{col+1}"][x] == h or algorithm.c_term_lists[f"c{row+1}{col+1}"][x] == " - " + h or algorithm.c_term_lists[f"c{row+1}{col+1}"][x] == h[3:]:
								count +=1
						
						if count == len(algorithm.c_term_lists[f"c{row+1}{col+1}"]):
							unremovable_h_list.append(algorithm.c_term_lists[f"c{row+1}{col+1}"][0].replace(" - ",""))



			h_to_remove = f"h{random.randint(1,self.num_terms)}"

			unremovable_h_list = dict.fromkeys(unremovable_h_list)

			while h_to_remove not in algorithm.mult_algo.keys() or h_to_remove in unremovable_h_list:
			
				if len(unremovable_h_list) == len(algorithm.h_term_lists.keys()):
					return algorithm
				h_to_remove = f"h{random.randint(1,self.num_terms)}"

			#print("Removing ", h_to_remove)

			del algorithm.mult_algo[h_to_remove]
			del algorithm.h_term_lists[h_to_remove]
			if h_to_remove in algorithm.solo_h_list_a:
				algorithm.solo_h_list_a.remove(h_to_remove)
			if h_to_remove in algorithm.solo_h_list_b:
				algorithm.solo_h_list_b.remove(h_to_remove)

			#print(unremovable_h_list)
			#print("h to remove: ", h_to_remove)

			for row in range(self.mat_size[0]):
				for col in range(self.mat_size[1]):
					if h_to_remove in algorithm.c_term_lists[f"c{row+1}{col+1}"]:

						while h_to_remove in algorithm.c_term_lists[f"c{row+1}{col+1}"]:
							algorithm.c_term_lists[f"c{row+1}{col+1}"].remove(h_to_remove)
						algorithm.mult_algo[f"c{row+1}{col+1}"] = self.make_c(algorithm.c_term_lists[f"c{row+1}{col+1}"])

					if " - " + h_to_remove in algorithm.c_term_lists[f"c{row+1}{col+1}"]:

						while " - " + h_to_remove in algorithm.c_term_lists[f"c{row+1}{col+1}"]:
							algorithm.c_term_lists[f"c{row+1}{col+1}"].remove(" - " + h_to_remove)
						algorithm.mult_algo[f"c{row+1}{col+1}"] = self.make_c(algorithm.c_term_lists[f"c{row+1}{col+1}"])


		elif mutation_type == 3:

			if self.verbose:
				print("Mutation type: Add a to h")
			
			a_to_add = "a"
			
			if random.randint(0,1) == 1:
				a_to_add = " - " + a_to_add

			a_to_add += f"{random.randint(1,self.mat_size[0])}"
			a_to_add += f"{random.randint(1,self.mat_size[1])}"

			#print("new a: ", a_to_add)

			h_to_add_to = f"h{random.randint(1,self.num_terms)}"

			while h_to_add_to not in algorithm.mult_algo.keys():
				h_to_add_to = f"h{random.randint(1,self.num_terms)}"

			#print("old h list: ", algorithm.h_term_lists[h_to_add_to])
			#print("old h: ", algorithm.mult_algo[h_to_add_to])

			algorithm.h_term_lists[h_to_add_to].append(a_to_add)
			algorithm.mult_algo[h_to_add_to] = self.make_h(algorithm.h_term_lists[h_to_add_to])

			if h_to_add_to in algorithm.solo_h_list_a:
				algorithm.solo_h_list_a.remove(h_to_add_to)

			#print("new h list: ", algorithm.h_term_lists[h_to_add_to])
			#print("new h: ", algorithm.mult_algo[h_to_add_to])
			
		elif mutation_type == 4:

			if self.verbose:
				print("Mutation type: Add b to h")
			
			b_to_add = "b"
			
			if random.randint(0,1) == 1:
				b_to_add = " - " + b_to_add

			b_to_add += f"{random.randint(1,self.mat_size[0])}"
			b_to_add += f"{random.randint(1,self.mat_size[1])}"

			#print("new b: ", b_to_add)

			h_to_add_to = f"h{random.randint(1,self.num_terms)}"

			while h_to_add_to not in algorithm.mult_algo.keys():
				h_to_add_to = f"h{random.randint(1,self.num_terms)}"

			#print("old h list: ", algorithm.h_term_lists[h_to_add_to])
			#print("old h: ", algorithm.mult_algo[h_to_add_to])

			algorithm.h_term_lists[h_to_add_to].append(b_to_add)
			algorithm.mult_algo[h_to_add_to] = self.make_h(algorithm.h_term_lists[h_to_add_to])

			if h_to_add_to in algorithm.solo_h_list_b:
				algorithm.solo_h_list_b.remove(h_to_add_to)

			#print("new h list: ", algorithm.h_term_lists[h_to_add_to])
			#print("new h: ", algorithm.mult_algo[h_to_add_to])

		elif mutation_type == 5:

			if self.verbose:
				print("Mutation type: Remove a from h")
			
			h_to_remove_from = ""
			valid = False

			excess = 0

			while not valid:

				h_to_remove_from = f"h{random.randint(1,self.num_terms)}"

				while h_to_remove_from not in algorithm.h_term_lists.keys():
					h_to_remove_from = f"h{random.randint(1,self.num_terms)}"

				num_a = 0

				for term in algorithm.h_term_lists[h_to_remove_from]:
					if "a" in term:
						num_a +=1
				
				if num_a > 1:
					valid = True
				elif h_to_remove_from not in algorithm.solo_h_list_a:
					algorithm.solo_h_list_a.append(h_to_remove_from)

				if len(algorithm.solo_h_list_a) == len(algorithm.h_term_lists.keys()):
					#print("Ran out of a terms to remove!")
					return algorithm

			terms = []

			for term in algorithm.h_term_lists[h_to_remove_from]:
				
				if "a" in term:
					terms.append(term)
				
			picked_term_i = random.randint(0, len(terms)-1)
			picked_term = terms[picked_term_i]

			#print("a to remove: ", picked_term)

			#print("old h list: ", algorithm.h_term_lists[h_to_remove_from])
			#print("old h: ", algorithm.mult_algo[h_to_remove_from])

			algorithm.h_term_lists[h_to_remove_from].remove(picked_term)
			algorithm.mult_algo[h_to_remove_from] = self.make_h(algorithm.h_term_lists[h_to_remove_from])

			#print("new h list: ", algorithm.h_term_lists[h_to_remove_from])
			#print("new h: ", algorithm.mult_algo[h_to_remove_from])

		elif mutation_type == 6:

			if self.verbose:
				print("Mutation type: Remove b from h")
			
			h_to_remove_from = ""
			valid = False

			excess = 0

			while not valid:

				h_to_remove_from = f"h{random.randint(1,self.num_terms)}"

				while h_to_remove_from not in algorithm.h_term_lists.keys():
					h_to_remove_from = f"h{random.randint(1,self.num_terms)}"

				num_b = 0

				for term in algorithm.h_term_lists[h_to_remove_from]:
					if "b" in term:
						num_b +=1
				
				if num_b > 1:
					valid = True
				elif h_to_remove_from not in algorithm.solo_h_list_b:
					algorithm.solo_h_list_b.append(h_to_remove_from)

				if len(algorithm.solo_h_list_b) == len(algorithm.h_term_lists.keys()):
					#print("Ran out of b terms to remove!")
					return algorithm

			terms = []

			for term in algorithm.h_term_lists[h_to_remove_from]:
				
				if "b" in term:
					terms.append(term)
				
			picked_term_i = random.randint(0, len(terms)-1)
			picked_term = terms[picked_term_i]

			#print("b to remove: ", picked_term)

			#print("old h list: ", algorithm.h_term_lists[h_to_remove_from])
			#print("old h: ", algorithm.mult_algo[h_to_remove_from])

			algorithm.h_term_lists[h_to_remove_from].remove(picked_term)
			algorithm.mult_algo[h_to_remove_from] = self.make_h(algorithm.h_term_lists[h_to_remove_from])

			#print("new h list: ", algorithm.h_term_lists[h_to_remove_from])
			#print("new h: ", algorithm.mult_algo[h_to_remove_from])

		elif mutation_type == 7:

			if self.verbose:
				print("Mutation type: Add h to c")

			h_to_add = f"h{random.randint(1,self.num_terms)}"

			while h_to_add not in algorithm.mult_algo.keys():
				h_to_add = f"h{random.randint(1,self.num_terms)}"

			c_to_add_to = f"c{random.randint(1,self.mat_size[0])}{random.randint(1,self.mat_size[1])}"

			if random.randint(0,1) == 1:
				h_to_add = " - " + h_to_add

			#print("h to add: ", h_to_add)

			#print("old c list: ", algorithm.c_term_lists[c_to_add_to])
			#print("old c: ", algorithm.mult_algo[c_to_add_to])

			algorithm.c_term_lists[c_to_add_to].append(h_to_add)
			algorithm.mult_algo[c_to_add_to] = self.make_c(algorithm.c_term_lists[c_to_add_to])

			#print("new c list: ", algorithm.c_term_lists[c_to_add_to])
			#print("new c: ", algorithm.mult_algo[c_to_add_to])

		elif mutation_type == 8:
			
			if self.verbose:
				print("Mutation type: Remove h from c")

			c_to_remove_from = ""
			valid = False

			while not valid:

				c_to_remove_from = f"c{random.randint(1,self.mat_size[0])}{random.randint(1,self.mat_size[1])}"
				
				if len(algorithm.c_term_lists[c_to_remove_from]) > 2:
					valid = True
				elif c_to_remove_from not in algorithm.solo_c_list:
					algorithm.solo_c_list.append(c_to_remove_from)

				if len(algorithm.solo_c_list) == len(algorithm.c_term_lists.keys()):
					#print("Ran out of h terms to remove from c terms!")
					return algorithm

			picked_term_i = random.randint(0,len(algorithm.c_term_lists[c_to_remove_from])-1)
			picked_term = algorithm.c_term_lists[c_to_remove_from][picked_term_i]

			#print("h to remove: ", picked_term)

			#print("old c list: ", algorithm.c_term_lists[c_to_remove_from])
			#print("old c: ", algorithm.mult_algo[c_to_remove_from])

			algorithm.c_term_lists[c_to_remove_from].remove(picked_term)
			algorithm.mult_algo[c_to_remove_from] = self.make_c(algorithm.c_term_lists[c_to_remove_from])

			#print("new c list: ", algorithm.c_term_lists[c_to_remove_from])
			#print("new c: ", algorithm.mult_algo[c_to_remove_from])

		return algorithm
	
	def main(self, num_mutations, num_generations, term_size, num_runs, random_mutations = False):

		for run in range(num_runs):
			self.init_mats(self.num_triples)

			#self.init_pop(self.pop_size)
			print("MAT A")
			print(self.mat_triples[0][0])
			print("MAT B")
			print(self.mat_triples[0][1])
			print("MAT C")
			print(self.mat_triples[0][2], "\n")

			self.algo = self.rand_algo(term_size, self.num_terms)
			self.print_algo(self.algo)

			self.algo.get_fitness(self.num_triples, self.mat_triples,self.num_terms,term_size,self.mat_size)

			print(self.algo.fitness_difference)

			time_0 = time.time()

			for gen in range(num_generations):
				if gen % 100 == 0 or gen == 0 or gen == num_generations-1:
					if random_mutations:
						f = open(f"./data/LISArmutation{self.num_triples}evalrun{run+1}.txt", "a")
					else:
						f = open(f"./data/LISA{num_mutations}mutation{self.num_triples}evalrun{run+1}.txt", "a")
					f.write(f"{gen},{self.algo.fitness_difference},{self.algo.fitness_cells}\n")
					f.close()
					print("Generation", gen)
				new_algo = copy.deepcopy(self.algo)
				if random_mutations:
					num_mutations = random.randint(1,5)
				for mutation in range(num_mutations):
					new_algo = copy.deepcopy(self.mutate(new_algo, term_size))
				new_algo.get_fitness(self.num_triples, self.mat_triples,self.num_terms,term_size,self.mat_size)
				if self.cells_priority:
					if new_algo.fitness_cells < self.algo.fitness_cells:
						self.algo = new_algo
						self.algo.get_fitness(self.num_triples, self.mat_triples,self.num_terms,term_size,self.mat_size)
						print("New fitness cells: %.2f | Difference: %f" % (self.algo.fitness_cells, self.algo.fitness_difference))
						self.h_added = 0
					else:
						self.num_terms -= self.h_added
						self.h_added = 0
				else:
					if new_algo.fitness_difference < self.algo.fitness_difference:
						self.algo = new_algo
						self.algo.get_fitness(self.num_triples, self.mat_triples,self.num_terms,term_size,self.mat_size)
						print("New fitness difference: %f | Cells: %f" % (self.algo.fitness_difference, self.algo.fitness_cells))
						self.h_added = 0
					else:
						self.num_terms -= self.h_added
						self.h_added = 0


			self.print_algo(self.algo)

			if random_mutations:
				f = open(f"./data/LISArmutation{self.num_triples}evalrun{run+1}.txt", "a")
			else:
				f = open(f"./data/LISA{num_mutations}mutation{self.num_triples}evalrun{run+1}.txt", "a")
			f.write("Final fitness difference: %.3f | Final fitness cells: %.2f \n" % (self.algo.fitness_difference,self.algo.fitness_cells))
			f.write("Time: %.2f \n" % (time.time() - time_0))
			f.write("Final number of h's: %d" % len(self.algo.h_term_lists.keys()))
			for x in self.algo.h_term_lists.keys():
				f.write(x + ": ")
				f.write(self.algo.mult_algo[x] + "\n")

			f.write("\n")

			for x in range(self.mat_size[0]):
				for y in range(self.mat_size[1]):
					f.write(f"c{x+1}{y+1}: ")
					f.write("(" + self.algo.mult_algo[f"c{x+1}{y+1}"] + ")" + "\n")

			f.close()
			print("Final fitness difference: %.3f | Final fitness cells: %.2f" % (self.algo.fitness_difference,self.algo.fitness_cells))
			print("Time: %.2f" % (time.time() - time_0))
			print("Final number of h's: ", len(self.algo.h_term_lists.keys()))
		
			self.num_terms = self.start_terms
		
if __name__ == "__main__":
		
	matmul = Matmul(30, cells_priority = False, verbose = False)
	matmul.main(1, 1000000, term_size=matmul.MEDIUM, num_runs=5, random_mutations=False)
	#matmul.main(2, 1000000, term_size=matmul.MEDIUM, num_runs=5, random_mutations=False)
	#matmul.main(3, 1000000, term_size=matmul.MEDIUM, num_runs=5, random_mutations=False)
	#matmul.main(4, 1000000, term_size=matmul.MEDIUM, num_runs=5, random_mutations=False)
	#matmul.main(5, 1000000, term_size=matmul.MEDIUM, num_runs=5, random_mutations=False)
	#matmul.main(1, 1000000, term_size=matmul.MEDIUM, num_runs=5, random_mutations=True)

