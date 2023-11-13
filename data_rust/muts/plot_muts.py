import matplotlib.pyplot as plt
import numpy as np

final_avg_diff = 0
final_avg_cells = 0

graph, (plot1, plot2) = plt.subplots(1,2)

num_runs = 12

for x in range(5):

	gens = []
	diff = []
	cells = []

	for y in range(num_runs):

		f = open("5matnocappos" + str(x+1) + "mut" + str(y+1), "r")
		lines = f.readlines()

		if y == 0:
		
			for z in range(2001):
				lineparts = lines[z].split(',')
				gens.append(lineparts[0])
				diff.append(float(lineparts[1]))
				cells.append(float(lineparts[2]))
		else: 
		
			for z in range(2001):
				lineparts = lines[z].split(",")
				diff[z] += float(lineparts[1])
				cells[z] += float(lineparts[2])
			
	for y in range(2001):
		diff[y] /= num_runs
		cells[y] /= num_runs
		
	plot1.plot(gens,diff, label = str(x+1) + " mutation")
	plot2.plot(gens,cells)
	
	if x == 0:
		print("1 mutation: " + str(diff[-1]))
	else:
		print(str(x+1) + " mutations: " + str(diff[-1]))



plot1.set_title("Cell difference over generations")


plot2.set_title("Number of incorrect cells over generations")

xticks = [0,400, 800, 1200, 1600, 2000]
#yticks = [0, 20, 40, 60, 80, 100]
yticks = [0,20,40,60,80,100]

plot1.set_xlim([0,200])
plot2.set_xlim([0,200])
plot1.set_ylim([0,100])
plot1.set_xticks(xticks)
plot1.set_yticks(yticks)
plot2.set_xticks(xticks)
plot1.set_xlabel("No. Generations")
plot1.set_ylabel("Average cell difference")
plot2.set_xlabel("No. Generations")
plot2.set_ylabel("Average number of incorrect cells")
plot1.legend()
#plot2.set_yticks(yticks)
#plot1.invert_yaxis()
graph.tight_layout()
#graph.suptitle("1 Mutation")

plt.show()
#print(gens[1])
#print(run1_diff[1])

#print(diff[0])



    

