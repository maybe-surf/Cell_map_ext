# -*- coding: utf-8 -*-
"""
Created on Wed May 24 21:25:26 2023

@author: maybe_surf
"""

#%% Set paths
create_dirs_path = '/home/georgelab/Documents/Lieselot/Sergei/Cell_map_ext/CellMap/create_dirs_double.py'

cell_detection_path = '/home/georgelab/Documents/Lieselot/Sergei/Cell_map_ext/ilastik/detect.py'
pipeline1_path = '/home/georgelab/Documents/Lieselot/Sergei/Cell_map_ext/ilastik/pipeline1.py'
pipeline2_path = '/home/georgelab/Documents/Lieselot/Sergei/Cell_map_ext/ilastik/pipeline2.py'

trained_model_path = '/home/georgelab/Documents/Lieselot/Sergei/R1_3d_0.ilp'


#%% create dict of directories
exec(open(create_dirs_path).read())

#%% run analysis

num_brains = 0
limit = 7

for brain in dirs.keys():
    brain_dirs = dirs.get(brain)
    
    #mecp2
#    import sys 
#    sys.path.append('/home/georgelab/Documents/ClearMap2')
#  
#    from ClearMap.Environment import *  #analysis:ignore
  
    #directories and files
    directory = brain_dirs.get("dir_brain") + "/C00-mecp2"  #1 animal  
  
#    expression_raw      = brain_dirs.get("dir_mecp2")     #neurons      
#    expression_auto     = brain_dirs.get("dir_auto")  #structure    
#  
#    ws = wsp.Workspace('CellMap', directory=directory);
#    ws.update(raw=expression_raw, autofluorescence=expression_auto)
#    ws.info()
#  
#    ws.debug = False
#  
#    resources_directory = settings.resources_path
    
    #exec(open(pipeline1_path).read()) #runs the CellMap pipeline up to cell_detection
    
    data_path = directory + "/stitched.npy"
    output_path = directory + "/cells_detected.npy" #check the file name
    cells_raw_path = directory + "/cells_raw_i.npy"
    
    #exec(open(pipeline1_path).read())
    exec(open(cell_detection_path).read())
    
    #exec(open(pipeline2_path).read())
    
    #foss
  
    #directories and files
    directory = brain_dirs.get("dir_brain") + "/C00-fos"  #1 animal  
  
#    expression_raw      = brain_dirs.get("dir_foss")     #neurons      
#    expression_auto     = brain_dirs.get("dir_auto")  #structure    
#  
#    ws = wsp.Workspace('CellMap', directory=directory);
#    ws.update(raw=expression_raw, autofluorescence=expression_auto)
#    ws.info()
#  
#    ws.debug = False
#  
#    resources_directory = settings.resources_path
    
    #exec(open(pipeline1_path).read()) #runs the CellMap pipeline up to cell_detection
    
    data_path = directory + "/stitched.npy"
    output_path = directory + "/cells_detected.npy" #check the file name
    cells_raw_path = directory + "/cells_raw_i.npy"
    
    #exec(open(pipeline1_path).read())
    
    exec(open(cell_detection_path).read())
    
   # exec(open(pipeline2_path).read())
    
    num_brains += 1
    if(num_brains == limit):
        break