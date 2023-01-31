import numpy as np

class Matmul:

	def __init__(self, num_triples):
		
		self.matrices = []
		self.num_triples = num_triples
		self.mult_algo = {}
		self.mult_algo_nums = {}
		

	def init_mats(self, num_triples):
		
		for x in range(num_triples):
		
			m1 = np.random.randint(10, size=(5, 5))
			m2 = np.random.randint(10, size=(5, 5))
			m3 = np.matmul(m1,m2)
			
			mat = (m1,m2,m3)
			
			self.matrices.append(mat)
			
	def mat_mult(self, m1, m2):
	
		res = np.zeros(shape=(m1.shape[0],m2.shape[1]))
		
		mult_num = 0
		
		for x in range(res.shape[0]):			#TODO: Find out if these vars are correct (x,y,z)
			for y in range(res.shape[1]):
				res_int_list = []							
				for z in range(res.shape[1]):	
					res_int_list.append(m1[x][z]*m2[z][y])
					self.mult_algo["h" + str(mult_num)] = "a" + str(x+1) + str(z+1) + " * " + "b" + str(z+1) + str(y+1)
					self.mult_algo_nums["h" + str(mult_num)] = str(m1[x][z]) + " * " + str(m2[z][y])
					mult_num += 1
				res[x][y] = sum(res_int_list)
		#for x in range(len(self.mult_algo_nums.keys())):
		#	print(self.mult_algo["h"+str(x)])
		#	print(self.mult_algo_nums["h"+str(x)])
		return res
			
	def assess_mult(self, result_mat, answer_mat):
	
		for x in range(result_mat.shape[0]):
			for y in range(result_mat.shape[1]):
				if result_mat[x][y] != answer_mat[x][y]:
					print("Error in position ", x,",", y, "is: ",result_mat[x][y], " should be: ", answer_mat[x][y])
		
	def main(self):

		self.init_mats(self.num_triples)
		print("Number of triples: ", len(self.matrices))
		print(self.matrices[0][0])
		print(self.matrices[0][1])
		print(self.matrices[0][2])
		
		print(self.mat_mult(self.matrices[0][0],self.matrices[0][1]))
		
		
		
matmul = Matmul(20)
matmul.main()

