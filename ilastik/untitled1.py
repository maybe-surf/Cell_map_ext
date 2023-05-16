# -*- coding: utf-8 -*-
"""
Created on Mon May 15 14:12:02 2023

@author: serge
"""

#%%
import numpy as np
import time
import multiprocessing as mp
import threading as th
verbose = False

output_path = "D:/R1_new/results1.npy"
stitched_path = "D:/R1_new/test_small.npy"

output = np.load(output_path)
print("loaded data")
stitched = np.load(stitched_path)
print("loaded stitched")

output3d = output[:, :, 4:16, 0]
#brain = [output3d[270*i:270*(i+1), :, :] for i in range(8)]
#brain_shape = brain.shape
#num_slices = brain_shape[2]
#cells_raw = []

print("here")

def valid(x, y, z, brain_shape):
    if(x >= 0 and x < brain_shape[0]):
        if(y >= 0 and y < brain_shape[1]):
            if(z >= 0 and z < brain_shape[2]):
                return True
    return False

def DFS3d(x, y, z, brain, brain_shape, ones):
    # if(x < x_init):
    #     return
    # if(x == x_init and y < y_init):
    #     return
    #base case:
    if((x, y, z) in ones):
        return
    ones.append((x, y, z))
    #see if not neccessary
    # if(x == 0 or y == 0): #ok since we are not going to have cells on the edges of slice
    #     return
    # if(x == slice_shape[0] - 1 or y == slice_shape[1] - 1):
    #     return
    #recursive cases:
    if(valid(x, y, z+1, brain_shape) and brain[x, y, z+1] == 1):
        DFS3d(x, y, z+1, brain, brain_shape, ones)
    if(valid(x, y+1, z, brain_shape) and brain[x, y+1, z] == 1):
        DFS3d(x, y+1, z, brain, brain_shape, ones)
    if(valid(x, y, z-1, brain_shape) and brain[x, y, z-1] == 1):
        DFS3d(x, y, z-1, brain, brain_shape, ones)
    if(valid(x, y-1, z, brain_shape) and brain[x, y-1, z] == 1):
        DFS3d(x, y-1, z, brain, brain_shape, ones)
    if(valid(x+1, y, z, brain_shape) and brain[x+1, y, z] == 1):
        DFS3d(x+1, y, z, brain, brain_shape, ones)
    if(valid(x-1, y, z, brain_shape) and brain[x-1, y, z] == 1):
        DFS3d(x-1, y, z, brain, brain_shape, ones)
    return

def fix_cell(ones, stitched, brain):
    for coord in ones:
        brain[coord] = 2
    sum_x = 0
    sum_y = 0
    sum_z = 0
    sum_stit = 0
    for coord in ones:
        sum_x += coord[0]
        sum_y += coord[1]
        sum_z += coord[2]
        sum_stit += stitched[coord]
    x_coord = round(sum_x/len(ones))
    y_coord = round(sum_y/len(ones))
    z_coord = round(sum_z/len(ones))
    source = round(sum_stit/len(ones))
    size = len(ones)
    #brain[x_coord, y_coord, z_coord] = 1
    return (x_coord, y_coord, z_coord, size, source)

print("here 2")

def process_brain(brain_slice, cells_raw):
    print("started")
    brain_shape = brain_slice.shape
    #num_slices = brain_shape[2]
    cells = []
    for x in range(brain_shape[0]):
        for y in range(brain_shape[1]):
            for z in range(brain_shape[2]):
                if(brain_slice[x, y, z] == 1):
                    ones = []
                    if(verbose):
                        print("start")
                    DFS3d(x, y, z, brain_slice, brain_shape, ones)
                    #check the size of ones and if you need the filtering
                    if(len(ones) > 1):
                        cell_info = fix_cell(ones, stitched, brain_slice)
                    else:
                        cell_info = (x, y, z, 1, stitched[x, y, z])
                    cells.append(cell_info)
                    if(verbose):
                        print("done")
    #return cells
    cells_raw += cells
    print("done slice")


cells_raw = []

brain = [output3d[270*i:270*(i+1), :, :] for i in range(8)]
start = time.time()
threads = []
for brain_slice in brain:
    t = th.Thread(target = process_brain, args = (brain_slice, cells_raw))
    threads.append(t)
    t.start()
# for process in processes:
#     process.join()
for t in threads:
    t.join()
    
# for brain_slice in brain:
#     print("slice")
#     new = process_brain(brain_slice, cells_raw)
#     print("done")
#     #cells_raw += new



end = time.time()
print("Total time is:", end - start)






