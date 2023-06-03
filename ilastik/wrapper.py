# -*- coding: utf-8 -*-
"""
Created on Thu May 11 23:16:34 2023

@author: serge
"""

#%% Set paths
set1_path = '/home/georgelab/Documents/Lieselot/Sergei/Cell_map_ext/drafts_reference/set1.txt'
set2_path = '/home/georgelab/Documents/Lieselot/Sergei/Cell_map_ext/drafts_reference/set2.txt'

create_dirs_path = '/home/georgelab/Documents/Lieselot/Sergei/Cell_map_ext/CellMap/create_dirs.py'

#pipeline1_path = '/home/georgelab/Documents/Lieselot/Sergei/Cell_map_ext/ilastik/pipeline1.py'
cell_detection_path = '/home/georgelab/Documents/Lieselot/Sergei/Cell_map_ext/ilastik/detect.py'
pipeline2_path = '/home/georgelab/Documents/Lieselot/Sergei/Cell_map_ext/ilastik/pipeline2.py'

trained_model_path = '/home/georgelab/Documents/Lieselot/Sergei/R1_3d_0.ilp'


#%% create dict of directories
exec(open(create_dirs_path).read())

#%% run analysis

num_brains = 0
limit = 0

for brain in dirs.keys():
    if(num_brains < 5):
        num_brains += 1
        continue
    brain_dirs = dirs.get(brain)
    
    import sys 
    sys.path.append('/home/georgelab/Documents/ClearMap2')
  
    from ClearMap.Environment import *  #analysis:ignore
  
    #directories and files
    directory = brain_dirs.get("dir_brain")  #1 animal 
    
    print("processing brain at", directory)
  
    expression_raw      = brain_dirs.get("dir_raw")     #neurons      
    expression_auto     = brain_dirs.get("dir_auto")  #structure    
  
    ws = wsp.Workspace('CellMap', directory=directory);
    ws.update(raw=expression_raw, autofluorescence=expression_auto)
    ws.info()
  
    ws.debug = False
  
    resources_directory = settings.resources_path
    
    #exec(open(pipeline1_path).read()) #runs the CellMap pipeline up to cell_detection
    
    data_path = directory + "/stitched.npy"
    output_path = directory + "/cells_detected.npy" #check the file name
    
    #tester directories
    #data_path = directory + "/ilastik/test.npy"
    #output_path = directory + "/ilastik/cells_detected.npy"
    
    exec(open(cell_detection_path).read())
    
    exec(open(pipeline2_path).read())
    
    num_brains += 1
#    if(num_brains == limit):
#        break