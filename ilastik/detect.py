# -*- coding: utf-8 -*-
"""
Created on Fri May 12 00:16:03 2023

@author: serge
"""
#%%
import os
import numpy as np

trained_model_path = '/home/georgelab/Documents/Lieselot/Sergei/R1_3d_0.ilp'
data_path = '/media/georgelab/Rett1/Lieselot_Collab/R1/ilastik/test_small.npy'
output_path = '/media/georgelab/Rett1/Lieselot_Collab/R1/ilastik/results1.npy'

#%%
os.system('pwd')
os.chdir('Downloads')

os.chdir('ilastik-1.4.0-Linux')
os.system('pwd')


#%%

command = "./run_ilastik.sh --headless --project=" + trained_model_path + " --output_format=numpy --output_filename_format=" + output_path + " --export_dtype=uint8 --export_source=\"Simple Segmentation\" --stack_along=\"t\" \"" + data_path + "\""

os.system(command)

#%%

output = np.load(output_path)
brain = output[:, :, :, 0]
brain_shape = brain.shape
num_slices = 20

def valid(x, y, z, num_slices):
    if(x >= 0 and x < 2160):
        if(y >= 0 and y < 2560):
            if(z >= 0 and z <= num_slices):
                return True
    return False

def DFS3d(x, y, z, brain):
    # if(x < x_init):
    #     return
    # if(x == x_init and y < y_init):
    #     return
    if((x, y, z) in visited):
        return
    ones.append((x, y, z))
    visited.append((x, y, z))
    if(x == 0 or y == 0): #ok since we are not going to have cells on the edges of slice
        return
    if(x == slice_shape[0] - 1 or y == slice_shape[1] - 1):
        return
    #recursive cases:
    if(brain[x, y, z+1] == 1):
        DFS3d(x, y, z+1, brain)
    if(brain[x, y+1, z] == 1):
        DFS3d(x, y+1, z, brain)
    if(brain[x, y, z-1] == 1):
        DFS3d(x, y, z-1, brain)
    if(brain[x, y-1, z] == 1):
        DFS3d(x, y-1, z, brain)
    if(brain[x+1, y, z] == 1):
        DFS3d(x+1, y, z, brain)
    if(brain[x-1, y, z] == 1):
        DFS3d(x-1, y, z, brain)
    return

for x in range(brain_shape[0]):
    for y in range(brain_shape[1]):
        for z in range(brain_shape[2]):
            if(brain[x, y, z] == 1):
                x_init = x
                y_init = y
                z_init = z
                ones = []
                visited = []
                dfs_cell(x, y, brain_slice)
                #check the size of ones and if you need the filtering
                if(len(ones) > 1):
                    fix_cell(ones)



for z in range(brain_shape[2]):
    brain_slice = brain[:, :, z]
    for x in range(brain_shape[0]):
        for y in range(brain_shape[1]):
            if(brain_slice[x, y] == 1):
                x_init = x
                y_init = y
                ones = []
                visited = []
                dfs_cell(x, y, brain_slice)
                #check the size of ones and if you need the filtering
                if(len(ones) > 1):
                    fix_cell(ones)