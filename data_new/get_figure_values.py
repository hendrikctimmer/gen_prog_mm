import matplotlib.pyplot as plt
import numpy as np
import statistics

num_mats = 6
num_muts = 5
num_runs = 10
num_modes = 4

mode_1 = "cappos"
mode_2 = "nocappos"
mode_3 = "capnopos"
mode_4 = "nocapnopos"

cell_diff_first_avgs = []
incorrect_cells_first_avgs = []
cell_diff_last_avgs = []
incorrect_cells_last_avgs = []

for m in range(num_modes):
    for x in range(num_mats):
        for y in range(num_muts):
            first_cell_diffs = []
            last_cell_diffs = []
            first_incorrect_cells = []
            last_incorrect_cells = []
            for z in range(num_runs):
                #f = open("5matcappos1mut1", "r")
                mode = ""
                match m:
                    case 0:
                        f = open(str((x+1) * 5) + "mat" + str(mode_1) + str(y+1) + "mut" + str(z+1), "r")
                        mode = mode_1
                    case 1:
                        f = open(str((x+1) * 5) + "mat" + str(mode_2) + str(y+1) + "mut" + str(z+1), "r")
                        mode = mode_2
                    case 2:
                        f = open(str((x+1) * 5) + "mat" + str(mode_3) + str(y+1) + "mut" + str(z+1), "r")
                        mode = mode_3
                    case 3:
                        f = open(str((x+1) * 5) + "mat" + str(mode_4) + str(y+1) + "mut" + str(z+1), "r")
                        mode = mode_4
                lines = f.readlines()
                first_line = lines[0].strip().split(",")
                
                if x == 4 and y == 4 and z == 9 and mode == mode_4:
                    last_line = lines[8420].strip().split(",")
                else:
                    last_line = lines[10000].strip().split(",")
                first_cell_diffs.append(float(first_line[1]))
                last_cell_diffs.append(float(last_line[1]))
                first_incorrect_cells.append(float(first_line[2]))
                last_incorrect_cells.append(float(last_line[2]))
            first_cell_diff_avg = statistics.mean(first_cell_diffs)
            last_cell_diff_avg = statistics.mean(last_cell_diffs)
            first_incorrect_cell_avg = statistics.mean(first_incorrect_cells)
            last_incorrect_cell_avg = statistics.mean(last_incorrect_cells)
            print(str((x+1) * 5) + "mat" + str(mode) + str(y+1) + "mut:\n")
            print("First cell diff: " + str(first_cell_diff_avg))
            print("Last cell diff: " + str(last_cell_diff_avg) + "\n")
            print("First incorrect cells: " + str(first_incorrect_cell_avg))
            print("Last incorrect cells: " + str(last_incorrect_cell_avg) + "\n")


f = open("5mat" + "cappos4mut" + str(y+1), "r")
	