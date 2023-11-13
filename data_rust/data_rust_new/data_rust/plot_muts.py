import matplotlib.pyplot as plt
import numpy as np

final_avg_diff = 0
final_avg_cells = 0

graph, (plot1, plot2) = plt.subplots(1,2)

for x in range(5):

	gens = []
	diff = []
	cells = []

	for y in range(100):

		f = open("5matnocapnopos" + str(x+1) + "mut" + str(y+1), "r")
		lines = f.readlines()

		if y == 0:
		
			for z in range(1001):
				lineparts = lines[z].split(',')
				gens.append(lineparts[0])
				diff.append(float(lineparts[1]))
				cells.append(float(lineparts[2]))
		else: 
		
			for z in range(1001):
				lineparts = lines[z].split(",")
				diff[z] += float(lineparts[1])
				cells[z] += float(lineparts[2])
			
	for y in range(1001):
		diff[y] /= 100
		cells[y] /= 100
		
	plot1.plot(gens,diff, label = str(x+1))
	plot2.plot(gens,cells)




plot1.set_title("Cell difference over generations")


plot2.set_title("Number of incorrect cells over generations")

xticks = [0,200,400,600,800,1001]
yticks = [20, 30]

plot1.set_xlim([0,1001])
plot2.set_xlim([0,1001])
plot1.set_ylim([20,30])
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



    

