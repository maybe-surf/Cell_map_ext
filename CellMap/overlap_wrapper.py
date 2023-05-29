# -*- coding: utf-8 -*-
"""
Created on Sun May 28 18:42:11 2023

@author: serge
"""

#%% Paths
create_dirs_path = '/home/georgelab/Documents/Lieselot/Sergei/Cell_map_ext/CellMap/create_dirs_double.py'
overlap_path = ''

exec(open(create_dirs_path).read())

#%%
num_brains = 0
limit = 1

for brain in dirs.keys():
    brain_dirs = dirs.get(brain)
    directory = brain_dirs.get("dir_brain")
    mecp2_path = directory + "/C00-mecp2"
    fos_path = directory + "/C01-fos"
    
    exec(open(overlap_path).read())
    
    num_brains += 1
    if(num_brains == limit):
        break