import numpy as np
import random
from Algorithm import Algorithm

class Matmul:

	"""Object is initialized with number of triples as parameter, where the triple is
	a triple of matrices (a,b,c), such that a*b=c. 
	
	"""

	def __init__(self, num_triples):

		self.mat_triples = []
		self.mat_size = [5,5]
		self.num_triples = num_triples
		self.pop_size = 100
		self.SMALL = 2
		self.MEDIUM = 5
		self.LARGE = 10
		self.num_terms = 125
		self.population = []

		#Should be able to remove this after initializing population
		self.mult_algo = {}
		self.mult_algo_nums = {}
		
	def init_mats(self, num_triples):
		
		for x in range(num_triples):
		
			m1 = np.random.randint(10, size=(5, 5))
			m2 = np.random.randint(10, size=(5, 5))
			m3 = np.matmul(m1,m2)
			
			mat = (m1,m2,m3)
			
			self.mat_triples.append(mat)

	def rand_algo(self, term_size, num_terms):

		res = Algorithm()

		for x in range(num_terms):

			h_term_list, h_term = self.make_h(term_size)

			res.h_term_lists["h" + str(x+1)] = h_term_list
			res.mult_algo["h" + str(x+1)] = h_term

		for x in range(self.mat_size[0]):
			for y in range(self.mat_size[1]):

				c_term_list, c_term = self.make_c(term_size)

				res.c_term_lists["c" + str(x+1) + str(y+1)] = c_term_list
				res.mult_algo["c" + str(x+1) + str(y+1)] = c_term

		return res

	def make_ab_term(self):
		prob = random.uniform(0, 1)
		term_to_add = ""
		if prob > 0.5:
			term_to_add += " - "
		term_to_add += random.choice(["a", "b"])
		term_to_add += str(random.randint(1,5))
		term_to_add += str(random.randint(1,5))

		return term_to_add

	def make_h(self, term_size):

		h_term_list = []

		for x in range(term_size):
			h_term_list.append(self.make_ab_term())

		if self.one_sided_h(h_term_list):
			h_term_list, h_term = self.make_h(term_size)

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

		for y in range(len(h_term_list)):
			if "-" in h_term_list[y]:
				h_term_list[y] = h_term_list[y].replace("-", "")
				h_term_list[y] = h_term_list[y].strip()

		return h_term_list, h_term

	def make_c(self, term_size):

		c_term_list = []

		for x in range(term_size):
			prob = random.uniform(0, 1)
			term_to_add = ""
			if prob > 0.5:
				term_to_add += " - "
			term_to_add += "h"
			term_to_add += str(random.randint(1,125))
			c_term_list.append(term_to_add)

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
		if c_term[1] == " ":
			c_term = c_term.replace(" ", "", 1)
		for y in range(len(c_term_list)):
			if "-" in c_term_list[y]:
				c_term_list[y] = c_term_list[y].replace("-", "")
				c_term_list[y] = c_term_list[y].strip()

		return c_term_list, c_term


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

	def init_pop(self, pop_size):

		for x in range(pop_size):
			self.population.append(self.rand_algo(self.MEDIUM, self.num_terms))

	def print_algo(self, algo):
		for x in range(self.num_terms):
			print("h" + str(x+1) + ": ", algo.mult_algo["h" + str(x+1)])

		print("\n")

		for x in range(self.mat_size[0]):
			for y in range(self.mat_size[1]):
				print("c" + str(x+1) + str(y+1) + ": ", algo.mult_algo["c" + str(x+1) + str(y+1)])


	#############################################_____OLD_____##############################################################

	def mat_mult(self, m1, m2):
	
		res = np.zeros(shape=(m1.shape[0],m2.shape[1]))
		
		mult_num = 0
		
		for x in range(res.shape[0]):			#TODO: Find out if these vars are correct (x,y,z)
			for y in range(res.shape[1]):
				res_int_list = []							
				for z in range(res.shape[1]):	
					res_int_list.append(m1[x][z]*m2[z][y])
					self.mult_algo["h" + str(mult_num+1)] = "a" + str(x+1) + str(z+1) + " * " + "b" + str(z+1) + str(y+1)
					self.mult_algo_nums["h" + str(mult_num+1)] = str(m1[x][z]) + " * " + str(m2[z][y])
					mult_num += 1
				res[x][y] = sum(res_int_list)
		return res
			
	def assess_mult(self, result_mat, answer_mat):
	
		for x in range(result_mat.shape[0]):
			for y in range(result_mat.shape[1]):
				if result_mat[x][y] != answer_mat[x][y]:
					print("Error in position ", x,",", y, "is: ",result_mat[x][y], " should be: ", answer_mat[x][y])
		
	def main(self):

		self.init_mats(self.num_triples)

		#self.init_pop(self.pop_size)
		print("MAT A")
		print(self.mat_triples[0][0])
		print("MAT B")
		print(self.mat_triples[0][1])

		for x in range(self.pop_size):
			self.population.append(self.rand_algo(self.MEDIUM, self.num_terms))
		self.print_algo(self.population[0])

		self.population[0].eval_h_c(self.mat_triples[0],self.num_terms,self.MEDIUM,self.mat_size)

		#This was all debugging to see if the representation works, it does.
		"""self.init_mats(self.num_triples)
		print("Number of triples: ", len(self.matrices))
		print(self.matrices[0][0])
		print(self.matrices[0][1])
		print(self.matrices[0][2])
		
		print(self.mat_mult(self.matrices[0][0],self.matrices[0][1]))
		
		for x, y, z  in zip(self.mult_algo_nums.values(), self.mult_algo.keys(), self.mult_algo.values()):
			print(y) #y is mult_algo.key
			print(z) #z is mult_algo.value
			print(x + " = " + str(eval(x)) + "\n") #x is mult_algo_nums.value
		"""

		
if __name__ == "__main__":
		
	matmul = Matmul(20)
	matmul.main()

