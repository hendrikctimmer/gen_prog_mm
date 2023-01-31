import numpy as np

class Matmul{

	def __init__(self, num_triples):
		
		self.matrices = []
		self.num_triples = num_triples
		

	def init_mats(self, num_triples):
		
		for x in range(num_triples):
		
			m1 = np.random.randint(10, size=(5, 5))
			m2 = np.random.randint(10, size=(5, 5))
			m3 = np.matmul(m1,m2)
			
			
			
		
		
	def mat_mult(self, m1, m2):

	
	def main(self):

		self.init_mats(self.num_triples)
		print(mat)
		

}



