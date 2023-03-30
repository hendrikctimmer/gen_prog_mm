import numpy as np
import random
from Algorithm import Algorithm

class Matmul:

	"""Object is initialized with number of triples as parameter, where the triple is
	a triple of matrices (a,b,c), such that a*b=c. 
	
	mult_algo is a dictionary where the 
	
	"""

	def __init__(self, num_triples):

		self.matrices = []
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
			
			self.matrices.append(mat)

	def rand_algo(self, term_size, num_terms):

		res = Algorithm()

		for x in range(num_terms):
			h_term_a = ""
			h_term_b = ""
			h_term_list = self.make_h(term_size)

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

			#This can all be done in a much cleaner way probably
			h_term_a = h_term_a.strip()
			h_term_b = h_term_b.strip()
			h_term_a = h_term_a.strip("+")
			h_term_b = h_term_b.strip("+")
			h_term_a = h_term_a.strip()
			h_term_b = h_term_b.strip()
			h_term_a = "(" + h_term_a + ")"
			h_term_b = "(" + h_term_b + ")"
			if h_term_a[2] == " ":
				h_term_a = h_term_a.replace(" ","",1)
			if h_term_b[2] == " ":
				h_term_b = h_term_b.replace(" ", "", 1)

			h_term = h_term_a + " * " + h_term_b
			print(h_term)


			#res.mult_algo["h" + str(x+1)] = h_term_list_sorted[0] + " + " + h_term_list_sorted[1] + " + " + h_term_list_sorted[2] + " + " + h_term_list_sorted[3] + " + " + h_term_list_sorted[4]
			#print(res.mult_algo["h" + str(x+1)])
		return res

	def make_term(self):
		prob = random.uniform(0, 1)
		term_to_add = ""
		if prob > 0.5:
			term_to_add += " - "
		term_to_add += random.choice(["a", "b"])
		term_to_add += random.choice(["1", "2", "3", "4", "5"])
		term_to_add += random.choice(["1", "2", "3", "4", "5"])

		return term_to_add

	def make_h(self, term_size):

		h_term_list = []

		for x in range(term_size):
			h_term_list.append(self.make_term())

		if self.one_sided_h(h_term_list):
			h_term_list = self.make_h(term_size)

		return h_term_list


	def one_sided_h(self, h_list):

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

		#self.init_pop(self.pop_size)
		self.rand_algo(self.MEDIUM, self.num_terms)

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

		
		
		
matmul = Matmul(20)
matmul.main()

