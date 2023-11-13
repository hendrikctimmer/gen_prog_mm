import matplotlib.pyplot as plt
import numpy as np
import statistics
from scipy.optimize import curve_fit

final_avg_diff = 0
final_avg_cells = 0
gens = []

diff = []
cells = []

diff_avg = []
diff_min = []
diff_max = []

final_curve_params = []

def func(x,b):
	return -np.log(x) + b

for y in range(5):

	f = open("10mat" + "nocappos" + str(y+1), "r")
	lines = f.readlines()
		
	if y == 0:
		for z in range(len(lines)):
			if lines[z][0] not in ['', ' ', 'S', 'h', 'c'] and len(lines[z]) > 1:
				line = lines[z].strip()
				data = line.split(",")
			
				gens.append(float(data[0]))
				cells.append(float(data[2]))
	
				nl = []
				diff.append(nl)
			
	for z in range(len(lines)):
		if lines[z][0] not in ['', ' ', 'S', 'h', 'c'] and len(lines[z]) > 1 and lines[z][4] != '9' :
			line = lines[z].strip()
			data = line.split(",")
				
			diff[z].append(float(data[1]))
		
for x in range(len(diff)):
	
	diff_avg.append(statistics.mean(diff[x]))
	diff_min.append(min(diff[x]))
	diff_max.append(max(diff[x]))
	
plt.plot(gens,diff_avg, label = "Nocappos")
#plt.fill_between(gens, diff_min, diff_max, facecolor='#BAD0FF')

gens[0] = 1

params, params_cov = curve_fit(func, gens, diff_avg)
final_curve_params.append(params[0])
	
gens = []

diff = []
cells = []

diff_avg = []
diff_min = []
diff_max = []
	
for y in range(5):

	f = open("10mat" + "cappos" + str(y+1), "r")
	lines = f.readlines()
		
	if y == 0:
		for z in range(len(lines)):
			if lines[z][0] not in ['', ' ', 'S', 'h', 'c'] and len(lines[z]) > 1:
				line = lines[z].strip()
				data = line.split(",")
			
				gens.append(float(data[0]))
				cells.append(float(data[2]))
	
				nl = []
				diff.append(nl)
			
	for z in range(len(lines)):
		if lines[z][0] not in ['', ' ', 'S', 'h', 'c'] and len(lines[z]) > 1 and lines[z][4] != '9' :
			line = lines[z].strip()
			data = line.split(",")
				
			diff[z].append(float(data[1]))
		
for x in range(len(diff)):
	
	diff_avg.append(statistics.mean(diff[x]))
	diff_min.append(min(diff[x]))
	diff_max.append(max(diff[x]))
	
plt.plot(gens,diff_avg, label = "Cappos")
#plt.fill_between(gens, diff_min, diff_max, facecolor='#FFEFBA')

gens[0] = 1

params, params_cov = curve_fit(func, gens, diff_avg)
final_curve_params.append(params[0])

gens = []

diff = []
cells = []

diff_avg = []
diff_min = []
diff_max = []
	
for y in range(5):

	f = open("10mat" + "capnopos" + str(y+1), "r")
	lines = f.readlines()
		
	if y == 0:
		for z in range(len(lines)):
			if lines[z][0] not in ['', ' ', 'S', 'h', 'c'] and len(lines[z]) > 1:
				line = lines[z].strip()
				data = line.split(",")
			
				gens.append(float(data[0]))
				cells.append(float(data[2]))
	
				nl = []
				diff.append(nl)
			
	for z in range(len(lines)):
		if lines[z][0] not in ['', ' ', 'S', 'h', 'c'] and len(lines[z]) > 1 and lines[z][4] != '9' :
			line = lines[z].strip()
			data = line.split(",")
				
			diff[z].append(float(data[1]))
		
for x in range(len(diff)):
	
	diff_avg.append(statistics.mean(diff[x]))
	diff_min.append(min(diff[x]))
	diff_max.append(max(diff[x]))
	
plt.plot(gens,diff_avg, label = "Capnopos")
#plt.fill_between(gens, diff_min, diff_max, facecolor='#BFFFC0')

gens[0] = 1

params, params_cov = curve_fit(func, gens, diff_avg)
final_curve_params.append(params[0])

gens = []

diff = []
cells = []

diff_avg = []
diff_min = []
diff_max = []
	
for y in range(5):

	f = open("10mat" + "nocapnopos" + str(y+1), "r")
	lines = f.readlines()
		
	if y == 0:
		for z in range(len(lines)):
			if lines[z][0] not in ['', ' ', 'S', 'h', 'c'] and len(lines[z]) > 1:
				line = lines[z].strip()
				data = line.split(",")
			
				gens.append(float(data[0]))
				cells.append(float(data[2]))
	
				nl = []
				diff.append(nl)
			
	for z in range(len(lines)):
		if lines[z][0] not in ['', ' ', 'S', 'h', 'c'] and len(lines[z]) > 1 and lines[z][4] != '9' :
			line = lines[z].strip()
			data = line.split(",")
				
			diff[z].append(float(data[1]))
		
for x in range(len(diff)):
	
	diff_avg.append(statistics.mean(diff[x]))
	diff_min.append(min(diff[x]))
	diff_max.append(max(diff[x]))
	
plt.plot(gens,diff_avg, label = "Nocapnopos")
#plt.fill_between(gens, diff_min, diff_max, facecolor='#FFBFBF')

gens[0] = 1

params, params_cov = curve_fit(func, gens, diff_avg)
final_curve_params.append(params[0])


#graph, (plot1, plot2) = plt.subplots(1,2)

xticks = [0,200000,400000,600000,800000,1000000]
yticks = [0, 20, 40, 60, 80, 100]


plt.title("Cell difference over generations, 10 problem instances")

#plot2.plot(gens,cells)
#plot2.set_title("Number of incorrect cells over generations")



plt.xlim([0,1000000])
#plot2.set_xlim([0,1000000])
plt.ylim([0,100])
#plt.xticks([0,1000000])
#plt.yticks([0,100])
plt.tick_params(labelleft=False, labelbottom=False)
#plot2.set_xticks(xticks)
#plt.xlabel("No. Generations")
#plt.ylabel("Average cell difference")
plt.legend()
#plot2.set_xlabel("No. Generations")
#plot2.set_ylabel("Average number of incorrect cells")
#plot2.set_yticks(yticks)
#plot1.invert_yaxis()
#graph.tight_layout()
#graph.suptitle("1 Mutation")

plt.show()

"""

matrices = [5,10,15,20,25,30]

def final_func(x,a,b,c):
	return a * np.log(x+b) + c
	
params, params_cov = curve_fit(final_func, matrices, final_curve_params)

plt.scatter(matrices, final_curve_params, marker="x", color="red", label = "Data Point")

matrices = np.linspace(-50,50, 101)

plt.plot(matrices, final_func(matrices, params[0], params[1], params[2]), ls='--', label = "Fitted curve")
plt.xlim([0,40])
plt.ylim([20,80])
plt.xlabel("Number of problem instances evaluated on per generation")
plt.ylabel("Vertical shift")
plt.title("Vertical axis shift vs. number of problem instances")
print(params)
plt.show()
#print(gens[1])
#print(run1_diff[1])

#print(diff[0])
"""

    

