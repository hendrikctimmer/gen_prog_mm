import numpy as np
import copy

class Algorithm:

	def __init__(self):

		self.mult_algo = {} 			#A dictionary where the keys define h-term/c-term (e.g. h123, c43), key defines the actual equation (e.g. a23 * b45)
		self.h_term_lists = {}  		#Keys same as above, values are a list of the terms
		self.c_term_lists = {}			#Keys are index of result matrix (e.g. c23), values are sums of h-terms (e.g. h12 + h43 - h51)

		self.fitness_cells = 1000		#Fitness function: number of incorrect cells
		self.fitness_difference = 1000	#Fitness function: average incorrectness over all cells

		self.solo_h_list_a = []			#A list of the h terms that have 1 a term
		self.solo_h_list_b = []			#A list of the h terms that have 1 b term
		self.solo_c_list = []			#A list of the c terms that have 1 h term

	def eval_h(self, mat_triple, num_terms, term_size, mat_size):

		res = {}

		for x in range(num_terms):

			current_h = "h" + str(x+1)

			if current_h in self.mult_algo.keys():

				h_int = self.mult_algo[current_h]

				for term in range(len(self.h_term_lists[current_h])):

					mat = 0
					current_term = self.h_term_lists[current_h][term].replace(" - ","")

					if "b" in current_term:
						mat = 1
				
					num = mat_triple[mat][int(current_term[1])-1][int(current_term[2])-1] 

					h_int = h_int.replace(current_term, str(num))

				res[current_h] = h_int

				answer = eval(h_int)

		return res


	def eval_h_c(self, mat_triple, num_terms, term_size, mat_size):

		h_ints = self.eval_h(mat_triple, num_terms, term_size, mat_size)

		res_mat = np.zeros(mat_size)

		for row in range(mat_size[0]):
			for col in range(mat_size[1]):
				current_c = "c" + str(row+1) + str(col+1)

				c_int = self.mult_algo[current_c]

				for term in range(len(self.c_term_lists[current_c])):

					current_term = self.c_term_lists[current_c][term].replace(" - ", "")

					if current_term in self.mult_algo.keys():
						c_int = c_int.replace(current_term + " ", str(eval(h_ints[current_term]))+ " ")

				c_int = c_int.replace("+ -", "- ")
				c_int = c_int.replace("- -", "+ ")

				result = eval(c_int)
				res_mat[row][col] = result

				#print("c" + str(row+1) + str(col+1) +": ",c_int + " = " + str(result))
		return res_mat



	def get_fitness(self, num_triples, mat_triples, num_terms, term_size, mat_size):

		self.fitness_difference = 0
		self.fitness_cells = 0

		cells = 0

		for triple in range(num_triples):

			difference = 0
			result = self.eval_h_c(mat_triples[triple], num_terms, term_size, mat_size)
			correct_result = mat_triples[triple][2]

			for row in range(mat_size[0]):
				for col in range(mat_size[1]):
					if result[row][col] != correct_result[row][col]:
						cells +=1
						difference += abs(result[row][col] - correct_result[row][col])

			difference /= mat_size[0]*mat_size[1]
			self.fitness_difference += difference

		self.fitness_cells = cells / num_triples
		self.fitness_difference /= num_triples

		#print("Fitness cells: ", self.fitness_cells)
		#print("Fitness difference: ", self.fitness_difference / (mat_size[0]*mat_size[1]))

		pass



