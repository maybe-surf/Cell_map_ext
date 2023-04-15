# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 00:02:42 2023

@author: serge
"""

#%% Set paths
set1_path = '/home/georgelab/Documents/Lieselot/Sergei/Cell_map_ext/set1.txt'
set2_path = '/home/georgelab/Documents/Lieselot/Sergei/Cell_map_ext/set2.txt'

create_dirs_path = '/home/georgelab/Documents/Lieselot/Sergei/Cell_map_ext/create_dirs.py'

pipeline_path = '/home/georgelab/Documents/Lieselot/Sergei/Cell_map_ext/analysis.py'


#%% create dict of directories
exec(open(create_dirs_path).read())

#%% run analysis

num_brains = 0
limit = 5

for brain in dirs.keys():
    brain_dirs = dirs.get(brain)
    
    import sys 
    sys.path.append('/home/georgelab/Documents/ClearMap2')
  
    from ClearMap.Environment import *  #analysis:ignore
  
    #directories and files
    directory = brain_dirs.get("dir_brain")  #1 animal  
  
    expression_raw      = brain_dirs.get("dir_raw")     #neurons      
    expression_auto     = brain_dirs.get("brain.auto")  #structure
  
    ws = wsp.Workspace('CellMap', directory=directory);
    ws.update(raw=expression_raw, autofluorescence=expression_auto)
    ws.info()
  
    ws.debug = False
  
    resources_directory = settings.resources_path
    
    exec(open(pipeline_path).read())
    
    num_brains += 1
    if(num_brains == limit):
        break

    
    