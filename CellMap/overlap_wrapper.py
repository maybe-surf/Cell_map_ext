# -*- coding: utf-8 -*-
"""
Created on Sun May 28 18:42:11 2023

@author: serge
"""

#%% Paths
create_dirs_path = '/home/georgelab/Documents/Lieselot/Sergei/Cell_map_ext/CellMap/create_dirs_double.py'
overlap_path = '/home/georgelab/Documents/Lieselot/Sergei/Cell_map_ext/CellMap/double_overlap.py'

exec(open(create_dirs_path).read())

zs = [1988, 1986, 1989, 1986, 1980, 1988, 1987, 1987]

#%%
num_brains = 0
limit = 12

for brain in dirs.keys():
    if(num_brains == 0):
        num_brains += 1
        continue
    brain_dirs = dirs.get(brain)
    directory = brain_dirs.get("dir_brain")
    mecp2_path = directory + "/C00-mecp2"
    fos_path = directory + "/C01-fos"
    
    shape = [2160, 2560, zs[num_brains]]

    
    exec(open(overlap_path).read())
    
    num_brains += 1
    if(num_brains == limit):
        break