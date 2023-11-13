import matplotlib.pyplot as plt
import numpy as np
import statistics

final_avg_diff = 0
final_avg_cells = 0
gens = []

diff = []
cells = []

diff_avg = []
diff_min = []
diff_max = []

for y in range(10):

	f = open("2mat" + "cappos" + str(y+1), "r")
	lines = f.readlines()
		
	if y == 0:
		for z in range(len(lines)):
			if lines[z][0] not in ['s','', ' ', 'S', 'h', 'c'] and len(lines[z]) > 1:
				line = lines[z].strip()
				data = line.split(",")
			
				gens.append(float(data[0]))
				cells.append(float(data[2]))
	
				nl = []
				diff.append(nl)
			
	for z in range(len(lines)):
		if lines[z][0] not in ['s','', ' ', 'S', 'h', 'c'] and len(lines[z]) > 1:
			line = lines[z].strip()
			data = line.split(",")
				
			diff[z].append(float(data[1]))
		
for x in range(len(diff)):
	
	diff_avg.append(statistics.mean(diff[x]))
	diff_min.append(min(diff[x]))
	diff_max.append(max(diff[x]))
	
plt.plot(gens,diff_avg, label = "CapPos")
plt.fill_between(gens, diff_min, diff_max, facecolor='#BAD0FF')
	
gens = []

diff = []
cells = []

diff_avg = []
diff_min = []
diff_max = []
	
for y in range(10):

	f = open("2mat" + "nocappos" + str(y+1), "r")
	lines = f.readlines()
		
	if y == 0:
		for z in range(len(lines)):
			if lines[z][0] not in ['s','', ' ', 'S', 'h', 'c'] and len(lines[z]) > 1:
				line = lines[z].strip()
				data = line.split(",")
			
				gens.append(float(data[0]))
				cells.append(float(data[2]))
	
				nl = []
				diff.append(nl)
			
	for z in range(len(lines)):
		if lines[z][0] not in ['s','', ' ', 'S', 'h', 'c'] and len(lines[z]) > 1:
			line = lines[z].strip()
			data = line.split(",")
				
			diff[z].append(float(data[1]))
		
for x in range(len(diff)):
	
	diff_avg.append(statistics.mean(diff[x]))
	diff_min.append(min(diff[x]))
	diff_max.append(max(diff[x]))
	
plt.plot(gens,diff_avg, label = "NocapPos")
plt.fill_between(gens, diff_min, diff_max, facecolor='#FFEFBA')

gens = []

diff = []
cells = []

diff_avg = []
diff_min = []
diff_max = []
	
for y in range(10):

	f = open("2mat" + "capnopos" + str(y+1), "r")
	lines = f.readlines()
		
	if y == 0:
		for z in range(len(lines)):
			if lines[z][0] not in ['s','', ' ', 'S', 'h', 'c'] and len(lines[z]) > 1:
				line = lines[z].strip()
				data = line.split(",")
			
				gens.append(float(data[0]))
				cells.append(float(data[2]))
	
				nl = []
				diff.append(nl)
			
	for z in range(len(lines)):
		if lines[z][0] not in ['s','', ' ', 'S', 'h', 'c'] and len(lines[z]) > 1:
			line = lines[z].strip()
			data = line.split(",")
				
			diff[z].append(float(data[1]))
		
for x in range(len(diff)):
	
	diff_avg.append(statistics.mean(diff[x]))
	diff_min.append(min(diff[x]))
	diff_max.append(max(diff[x]))
	
plt.plot(gens,diff_avg, label = "CapNopos")
plt.fill_between(gens, diff_min, diff_max, facecolor='#BFFFC0')

gens = []

diff = []
cells = []

diff_avg = []
diff_min = []
diff_max = []
	
for y in range(10):

	f = open("2mat" + "nocapnopos" + str(y+1), "r")
	print("2matnocapnopos" + str(y+1))
	lines = f.readlines()
		
	if y == 0:
		for z in range(len(lines)):
			if lines[z][0] not in ['s','', ' ', 'S', 'h', 'c'] and len(lines[z]) > 1:
				line = lines[z].strip()
				data = line.split(",")
			
				gens.append(float(data[0]))
				cells.append(float(data[2]))
	
				nl = []
				diff.append(nl)
			
	for z in range(len(lines)):
		if lines[z][0] not in ['s','', ' ', 'S', 'h', 'c'] and len(lines[z]) > 1:
			line = lines[z].strip()
			data = line.split(",")

			diff[z].append(float(data[1]))
		
for x in range(len(diff)):
	
	if diff[x]:
		diff_avg.append(statistics.mean(diff[x]))
		diff_min.append(min(diff[x]))
		diff_max.append(max(diff[x]))
	
plt.plot(gens,diff_avg, label = "NocapNopos")
plt.fill_between(gens, diff_min, diff_max, facecolor='#FFBFBF')



#graph, (plot1, plot2) = plt.subplots(1,2)

xticks = [0,200000,400000,600000,800000,1000000]
yticks = [10,8,6,4,2,0]


plt.title("Cell difference over generations, 2 matrix triples")

#plot2.plot(gens,cells)
#plot2.set_title("Number of incorrect cells over generations")



plt.xlim([0,1000000])
#plot2.set_xlim([0,1000000])
plt.ylim([0,10])
plt.xticks(xticks)
plt.yticks(yticks)
#plot2.set_xticks(xticks)
plt.xlabel("No. Generations")
plt.ylabel("Average cell difference")
plt.legend()
#plot2.set_xlabel("No. Generations")
#plot2.set_ylabel("Average number of incorrect cells")
#plot2.set_yticks(yticks)
#plot1.invert_yaxis()
#graph.tight_layout()
#graph.suptitle("1 Mutation")

plt.show()
#print(gens[1])
#print(run1_diff[1])

#print(diff[0])


    

