import matplotlib.pyplot as plt
import numpy as np
import statistics

final_avg_diff = 0
final_avg_cells = 0
gens = []

diff = []

diff_avg = []
diff_min = []
diff_max = []

multiple = False

for y in range(10):

	f = open("5mat" + "cappos" + str(y+1), "r")
	lines = f.readlines()
		
	if y == 0:
		for z in range(len(lines)):
			line = lines[z].strip()
			data = line.split(",")
			
			gens.append(float(data[0]))
	
			diff[z] = []
			
	for z in range(len(lines)):
		line = lines[z].strip()
		data = line.split(",")
				
		diff[z].append(float(data[1]))
		
for x in range(len(diff)):
	
	diff_avg[x] = statistics.mean(diff[x])
	diff_min[x] = min(diff[x])
	diff_max[x] = max(diff[x])
	

graph, (plot1, plot2) = plt.subplots(1,2)

xticks = [0,200000,400000,600000,800000,1000000]
yticks = [200,150,100,50,0]

#print(type(run1_diff[0]))
if (multiple):
    diff = np.average([run1_diff,run2_diff,run3_diff], axis = 0)
    cells = np.average([run1_cells,run2_cells,run3_cells], axis = 0)

plot1.plot(gens,diff)
plot1.plot(gens,diff_max)
plot1.plot(gens,diff_min)
#plot1.fill_between(gens, diff_min, diff_max, facecolor='#BAD0FF')
plot1.set_title("Cell difference over generations")

plot2.plot(gens,cells)
plot2.set_title("Number of incorrect cells over generations")



plot1.set_xlim([0,1000000])
plot2.set_xlim([0,1000000])
plot1.set_ylim([0,200])
plot1.set_xticks(xticks)
plot1.set_yticks(yticks)
plot2.set_xticks(xticks)
plot1.set_xlabel("No. Generations")
plot1.set_ylabel("Average cell difference")
plot2.set_xlabel("No. Generations")
plot2.set_ylabel("Average number of incorrect cells")
#plot2.set_yticks(yticks)
#plot1.invert_yaxis()
graph.tight_layout()
#graph.suptitle("1 Mutation")

plt.show()
#print(gens[1])
#print(run1_diff[1])

#print(diff[0])


    

