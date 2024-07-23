import matplotlib.pyplot as plt
import numpy as np
import statistics
from scipy.optimize import curve_fit

final_avg_diff = 0
final_avg_cells = 0
gens = []

no_muts = 5

diff = []
cells = []

diff_avg = []
diff_min = []
diff_max = []

final_curve_params = []

def func(x,b):
	return -np.log(x) + b

for y in range(10):

	f = open("5mat" + "cappos" + str(no_muts) + "mut" + str(y+1), "r")
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
		if lines[z][0] not in ['', ' ', 'S', 'h', 'c'] and len(lines[z]) > 1:
			line = lines[z].strip()
			data = line.split(",")
				
			diff[z].append(float(data[2]))
		
for x in range(len(diff)):
	
	diff_avg.append(statistics.mean(diff[x]))
	diff_min.append(min(diff[x]))
	diff_max.append(max(diff[x]))

print("30mat: " + str(diff_avg[-1]))
	
plt.plot(gens,diff_avg, label = "5 Problem Instances")
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
	
for y in range(10):

	f = open("10mat" + "cappos" + str(no_muts) + "mut" + str(y+1), "r")
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
		if lines[z][0] not in ['', ' ', 'S', 'h', 'c'] and len(lines[z]) > 1:
			line = lines[z].strip()
			data = line.split(",")
				
			diff[z].append(float(data[2]))
		
for x in range(len(diff)):
	
	diff_avg.append(statistics.mean(diff[x]))
	diff_min.append(min(diff[x]))
	diff_max.append(max(diff[x]))

print("30mat: " + str(diff_avg[-1]))
	
plt.plot(gens,diff_avg, label = "10 Problem Instances")
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
	
for y in range(10):

	f = open("15mat" + "cappos" + str(no_muts) + "mut" + str(y+1), "r")
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
		if lines[z][0] not in ['', ' ', 'S', 'h', 'c'] and len(lines[z]) > 1:
			line = lines[z].strip()
			data = line.split(",")
				
			diff[z].append(float(data[2]))
		
for x in range(len(diff)):
	
	diff_avg.append(statistics.mean(diff[x]))
	diff_min.append(min(diff[x]))
	diff_max.append(max(diff[x]))

print("30mat: " + str(diff_avg[-1]))
	
plt.plot(gens,diff_avg, label = "15 Problem Instances")
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
	
for y in range(10):

	f = open("20mat" + "cappos" + str(no_muts) + "mut" + str(y+1), "r")
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
		if lines[z][0] not in ['', ' ', 'S', 'h', 'c'] and len(lines[z]) > 1:
			line = lines[z].strip()
			data = line.split(",")
				
			diff[z].append(float(data[2]))
		
for x in range(len(diff)):
	
	diff_avg.append(statistics.mean(diff[x]))
	diff_min.append(min(diff[x]))
	diff_max.append(max(diff[x]))

print("30mat: " + str(diff_avg[-1]))
	
plt.plot(gens,diff_avg, label = "20 Problem Instances")
#plt.fill_between(gens, diff_min, diff_max, facecolor='#FFBFBF')

gens[0] = 1

params, params_cov = curve_fit(func, gens, diff_avg)
final_curve_params.append(params[0])

gens = []

diff = []
cells = []

diff_avg = []
diff_min = []
diff_max = []
	
for y in range(10):

	f = open("25mat" + "cappos" + str(no_muts) + "mut" + str(y+1), "r")
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
		if lines[z][0] not in ['', ' ', 'S', 'h', 'c'] and len(lines[z]) > 1:
			line = lines[z].strip()
			data = line.split(",")
				
			diff[z].append(float(data[2]))
		
for x in range(len(diff)):
	
	diff_avg.append(statistics.mean(diff[x]))
	diff_min.append(min(diff[x]))
	diff_max.append(max(diff[x]))

print("30mat: " + str(diff_avg[-1]))
	
plt.plot(gens,diff_avg, label = "25 Problem Instances")
#plt.fill_between(gens, diff_min, diff_max, facecolor='#D1BFFF')

gens[0] = 1

params, params_cov = curve_fit(func, gens, diff_avg)
final_curve_params.append(params[0])

gens = []

diff = []
cells = []

diff_avg = []
diff_min = []
diff_max = []
	
for y in range(10):

	f = open("30mat" + "cappos" + str(no_muts) + "mut" + str(y+1), "r")
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
		if lines[z][0] not in ['', ' ', 'S', 'h', 'c'] and len(lines[z]) > 1:
			line = lines[z].strip()
			data = line.split(",")
				
			diff[z].append(float(data[2]))
		
for x in range(len(diff)):
	
	diff_avg.append(statistics.mean(diff[x]))
	diff_min.append(min(diff[x]))
	diff_max.append(max(diff[x]))
	
print("30mat: " + str(diff_avg[-1]))
	
plt.plot(gens,diff_avg, label = "30 Problem Instances")
#plt.fill_between(gens, diff_min, diff_max, facecolor='#DABDAD')

gens[0] = 1

params, params_cov = curve_fit(func, gens, diff_avg)
final_curve_params.append(params[0])

#graph, (plot1, plot2) = plt.subplots(1,2)

xticks = [0,200000,400000,600000,800000,1000000]
yticks = [100,80,60,40,20,0]


#plt.title("Cell difference over generations, CapGreedy")

#plot2.plot(gens,cells)
#plot2.set_title("Number of incorrect cells over generations")



plt.xlim([0,1000000])
#plot2.set_xlim([0,1000000])
plt.ylim([20,25])
plt.xticks(xticks)
#plt.yticks(yticks)
#plot2.set_xticks(xticks)
#plt.xlabel("No. Generations")
#plt.ylabel("Average cell difference")
plt.text(40000,20.2, "CapNoEQ", fontsize=12,bbox=dict(facecolor='none', alpha=0.5))
plt.subplots_adjust(right = 0.57, top = 0.98, bottom = 0.09)
plt.tick_params(labelleft=False)
#plt.legend()
#plot2.set_xlabel("No. Generations")
#plot2.set_ylabel("Average number of incorrect cells")
#plot2.set_yticks(yticks)
#plot1.invert_yaxis()
#graph.tight_layout()
#graph.suptitle("1 Mutation")

plt.show()

matrices = [5,10,15,20,25,30]

def final_func(x,a,b,c):
	return a * np.log(x+b) + c
	
params, params_cov = curve_fit(final_func, matrices, final_curve_params)

plt.scatter(matrices, final_curve_params, marker="x", color="red", label = "Vertical Axis Shift")

matrices = np.linspace(-50,50, 101)

plt.plot(matrices, final_func(matrices, params[0], params[1], params[2]), ls='--', label = "Fitted curve")
plt.xlim([0,40])
plt.ylim([0,100])
plt.tick_params(labelbottom=False, labelleft=False)
plt.title("Vertical axis shift vs. problem instances CapGreedy")
plt.legend()
print(params)
#plt.show()
#print(gens[1])
#print(run1_diff[1])

#print(diff[0])


    

