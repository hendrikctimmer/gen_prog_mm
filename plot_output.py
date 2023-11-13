import matplotlib.pyplot as plt
import numpy as np

final_avg_diff = 0
final_avg_cells = 0
gens = []
run1_diff = []
run2_diff = []
run3_diff = []

run1_cells = []
run2_cells = []
run3_cells = []

diff = []
diff_max = []
diff_min = []
cells = []

multiple = True

if (multiple):

    for x in range(3):

        f = open("run" + str(x+1) + "mutation1.txt", "r")
        lines = f.readlines()

        if x == 0:
            for x in range(len(lines)):
                line = lines[x].strip()
                data = line.split(",")
                gens.append(float(data[0]))
                run1_diff.append(float(data[1]))
                run1_cells.append(float(data[2]))
        elif x == 1:
            for x in range(len(lines)):
                line = lines[x].strip()
                data = line.split(",")
                run2_diff.append(float(data[1]))
                run2_cells.append(float(data[2]))
        elif x == 2:
            for x in range(len(lines)):
                line = lines[x].strip()
                data = line.split(",")
                run3_diff.append(float(data[1]))
                run3_cells.append(float(data[2]))

else:

    f = open("LISA1mutation5eval.txt", "r")
    lines = f.readlines()
    for x in range(len(lines)):
        line = lines[x].strip()
        data = line.split(",")
        gens.append(float(data[0]))
        diff_min.append(float(data[1]))
        cells.append(float(data[2]))
        
    f = open("LISA1mutation10eval.txt", "r")
    lines = f.readlines()
    for x in range(len(lines)):
        line = lines[x].strip()
        data = line.split(",")
        diff.append(float(data[1]))


    f = open("LISA1mutation20eval.txt", "r")
    lines = f.readlines()
    for x in range(len(lines)):
        line = lines[x].strip()
        data = line.split(",")
        diff_max.append(float(data[1]))


graph, (plot1, plot2) = plt.subplots(1,2)

xticks = [0,20000,40000,60000,80000,100000]
yticks = [200,150,100,50,0]

#print(type(run1_diff[0]))
if (multiple):
    diff = np.average([run1_diff,run2_diff,run3_diff], axis = 0)
    cells = np.average([run1_cells,run2_cells,run3_cells], axis = 0)

plot1.plot(gens,diff)
plot1.plot(gens,diff)
#plot1.fill_between(gens, diff_min, diff_max, facecolor='#BAD0FF')
plot1.set_title("Cell difference over generations")

plot2.plot(gens,cells)
plot2.set_title("Number of incorrect cells over generations")



plot1.set_xlim([0,100000])
plot2.set_xlim([0,100000])
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


    

