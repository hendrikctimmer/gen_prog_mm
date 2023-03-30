import numpy as np

class Algorithm:

	def __init__(self):
	
		self.mult_algo = {} 		#A dictionary where the keys define h-term (e.g. h123), key defines the actual equation (e.g. a23 * b45)
		self.mult_algo_nums = {}    #Same as mult_algo except the keys contain the numbers instead of variables (e.g. 7 instead of a12)
		
