import matplotlib.pyplot as plt
import numpy as np
import statistics
import pandas as pd
from scipy.optimize import curve_fit

column_names = ["Setting","Average_h", "Max_h", "Min_h", "Stdev_h", "Final_h", "Original_h", "New_h", "Avg_c", "Max_c", "Min_c", "Stdev_c"]
h_data = pd.DataFrame(columns=column_names)

for mode in range(4):

	for mat in range(6):

		for mut in range(5):

			stats = []
			num_h_list = []			#A list of the number of h's in each of the runs of a setting
			final_h_list = []		#A list of the h number of the final h in each run of a setting
			num_original_h = []		#A list of the number of original h's in the each run of a setting
			num_new_h = []			#A list of the number of new h's in the each run of a setting
			avg_len_c_list = []         #A list of the avg length of c's in each of the runs of a setting
			all_len_c_list = []			#A list of all lengths of c's in each run of a setting

			for run in range(10):

				if mode == 0:
					filename = str((mat+1)*5) + "mat" + "capnopos" + str(mut+1) + "mut" + str(run+1)
				elif mode == 1:
					filename = str((mat+1)*5) + "mat" + "cappos" + str(mut+1) + "mut" + str(run+1)
				elif mode == 2:
					filename = str((mat+1)*5) + "mat" + "nocapnopos" + str(mut+1) + "mut" + str(run+1)
				elif mode == 3:
					filename = str((mat+1)*5) + "mat" + "nocappos" + str(mut+1) + "mut" + str(run+1)

				if filename == "25matnocapnopos5mut10":
					filename = "25matnocapnopos5mut9"
				f = open(filename, "r")
				lines = f.readlines()

				number_of_h_terms = 0
				line_number = 10003 #10003 is the first line of the algorithm

				h_list = []

				while(lines[line_number][0] == 'h'):
					line_number += 1
					number_of_h_terms +=1
					h_list.append(lines[line_number].split(":")[0][1:])

				num_original = 0
				num_new = 0

				for h in h_list:
					if int(h) < 126:
						num_original +=1
					else:
						num_new +=1

				#print("Num original: " + str(num_original))
				#print("Num new: " + str(num_new))
				#print(filename)
				c_list = []
				num_c = []

				while(line_number < len(lines)):
					c_list.append(lines[line_number].split(":")[1])
					line_number +=1

				for c in c_list:
					num_c.append(c.count('h'))
					all_len_c_list.append(c.count('h'))

				line_number-=1
				h_term = lines[line_number].split(":")
				last_h = h_term[0][1:] #Save just the number so I can convert to int
				final_h_list.append(int(last_h))
				num_h_list.append(number_of_h_terms)
				num_new_h.append(num_new)
				num_original_h.append(num_original)
				avg_len_c_list.append(statistics.mean(num_c))
				#print("final h: " + last_h)
				#print("num h's: " + str(number_of_h_terms))

			
			if "nocapnopos" in filename:
				stats.append("NoCapEQ" + str((mat+1)*5) + "mat" + str(mut+1) + "mut")
			elif "capnopos" in filename:
				stats.append("CapEQ" + str((mat+1)*5) + "mat" + str(mut+1) + "mut")
			elif "nocappos" in filename:
				stats.append("NoCapNoEQ" + str((mat+1)*5) + "mat" + str(mut+1) + "mut")
			elif "cappos" in filename: 
				stats.append("CapNoEQ" + str((mat+1)*5) + "mat" + str(mut+1) + "mut")
			stats.append(statistics.mean(num_h_list)) 		#Average number of h's
			stats.append(max(num_h_list))			  		#Max number of h's
			stats.append(min(num_h_list))  			  		#Min number of h's
			stats.append(statistics.stdev(num_h_list))		#Stdev of number of h's
			stats.append(statistics.mean(final_h_list)) 	#Average final h no.
			stats.append(statistics.mean(num_original_h))	#Average num original h's
			stats.append(statistics.mean(num_new_h))		#Average num new h's
			stats.append(statistics.mean(avg_len_c_list))	#Average len c equations
			stats.append(max(all_len_c_list))				#Max length of a c equation
			stats.append(min(all_len_c_list))				#Min length of a c equation
			stats.append(statistics.stdev(avg_len_c_list))		#Stdev of len c equations
			stats = [stats]
			h_data = h_data.append(pd.DataFrame(stats, columns = column_names), ignore_index = True)
h_data.set_index(["Setting"],inplace = True)

h_data.to_csv('h_data.csv')
print(h_data)
