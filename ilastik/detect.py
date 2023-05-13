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

def DFS3d(x, y, z):
    if(x < x_init):
        return
    if(x == x_init and y < y_init):
        return
    if((x, y) in visited):
        return
    ones.append((x, y))
    visited.append((x, y))
    if(x == 0 or y == 0):
        return
    if(x == slice_shape[0] - 1 or y == slice_shape[1] - 1):
        return
    if(image[x, y+1] == 1):
        dfs_cell(x, y+1, image)
    if(image[x+1, y] == 1):
        dfs_cell(x+1, y, image)
    if(image[x, y-1] == 1):
        dfs_cell(x, y-1, image)
    if(image[x-1, y] == 1):
        dfs_cell(x-1, y, image)
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