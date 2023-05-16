# -*- coding: utf-8 -*-
"""
Created on Fri May 12 00:16:03 2023

@author: serge
"""
#%%
import os
#import numpy as np

#trained_model_path = '/home/georgelab/Documents/Lieselot/Sergei/R1_3d_0.ilp'
#data_path = '/media/georgelab/Rett1/Lieselot_Collab/R1/ilastik/test_small.npy'
#output_path = '/media/georgelab/Rett1/Lieselot_Collab/R1/ilastik/results1.npy'

#%%
#os.system('pwd')
os.chdir('/home/georgelab/Downloads') #test it out with absolute path

os.chdir('ilastik-1.4.0-Linux')
#os.system('pwd')


#%%

command = "./run_ilastik.sh --headless --project=" + trained_model_path + " --output_format=numpy --output_filename_format=" + output_path + " --export_dtype=uint8 --export_source=\"Simple Segmentation\" --stack_along=\"t\" \"" + data_path + "\""

os.system(command)

#%%
import numpy as np
verbose = False

#output_path = "D:/R1_new/results1.npy"
stitched_path = data_path

print("begin loading data")
output = np.load(output_path)
print("loaded data")
stitched = np.load(stitched_path)
print("loaded stitched")

brain = output[:, :, :, 0]
brain_shape = brain.shape
num_slices = brain_shape[2]
cells_raw = []

print("here")

def valid(x, y, z, num_slices):
    if(x >= 0 and x < 2160):
        if(y >= 0 and y < 2560):
            if(z >= 0 and z < num_slices):
                return True
    return False

def DFS3d(x, y, z, brain):
    # if(x < x_init):
    #     return
    # if(x == x_init and y < y_init):
    #     return
    #base case:
    if((x, y, z) in visited):
        return
    ones.append((x, y, z))
    visited.append((x, y, z)) #see if not neccessary
    # if(x == 0 or y == 0): #ok since we are not going to have cells on the edges of slice
    #     return
    # if(x == slice_shape[0] - 1 or y == slice_shape[1] - 1):
    #     return
    #recursive cases:
    if(valid(x, y, z+1, num_slices) and brain[x, y, z+1] == 1):
        DFS3d(x, y, z+1, brain)
    if(valid(x, y+1, z, num_slices) and brain[x, y+1, z] == 1):
        DFS3d(x, y+1, z, brain)
    if(valid(x, y, z-1, num_slices) and brain[x, y, z-1] == 1):
        DFS3d(x, y, z-1, brain)
    if(valid(x, y-1, z, num_slices) and brain[x, y-1, z] == 1):
        DFS3d(x, y-1, z, brain)
    if(valid(x+1, y, z, num_slices) and brain[x+1, y, z] == 1):
        DFS3d(x+1, y, z, brain)
    if(valid(x-1, y, z, num_slices) and brain[x-1, y, z] == 1):
        DFS3d(x-1, y, z, brain)
    return

def fix_cell(ones, stitched):
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

for x in range(brain_shape[0]):
    print("filtering slice")
    for y in range(brain_shape[1]):
        for z in range(brain_shape[2]):
            if(brain[x, y, z] == 1):
                x_init = x
                y_init = y
                z_init = z
                ones = []
                visited = []
                if(verbose):
                    print("start")
                DFS3d(x, y, z, brain)
                #check the size of ones and if you need the filtering
                if(len(ones) > 1):
                    cell_info = fix_cell(ones, stitched)
                else:
                    cell_info = (x, y, z, 1, stitched[x, y, z])
                cells_raw.append(cell_info)
                if(verbose):
                    print("done")
np.save(directory + '/cells_raw.npy', cells_raw)
                    
#%%
def test_brain(brain):
    for x in range(brain_shape[0]):
        for y in range(brain_shape[1]):
            for z in range(brain_shape[2]):
                if(brain[x, y, z] == 1):
                    if(valid(x, y, z+1, num_slices) and brain[x, y, z+1] == 1):
                        return False
                    if(valid(x, y+1, z, num_slices) and brain[x, y+1, z] == 1):
                        return False
                    if(valid(x, y, z-1, num_slices) and brain[x, y, z-1] == 1):
                        return False
                    if(valid(x, y-1, z, num_slices) and brain[x, y-1, z] == 1):
                        return False
                    if(valid(x+1, y, z, num_slices) and brain[x+1, y, z] == 1):
                        return False
                    if(valid(x-1, y, z, num_slices) and brain[x-1, y, z] == 1):
                        return False
    return True

#%%
# import pandas as pd
# coords = []

# for row in cells_raw:
#     coords.append((row[0], row[1], row[2]))

# coordsDF = pd.DataFrame(coords)
# dups = coordsDF[0].duplicated()

