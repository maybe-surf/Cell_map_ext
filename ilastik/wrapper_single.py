#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 20:22:48 2023

@author: georgelab
"""

#%% Set paths
set1_path = '/home/georgelab/Documents/Lieselot/Sergei/Cell_map_ext/drafts_reference/set1.txt'
set2_path = '/home/georgelab/Documents/Lieselot/Sergei/Cell_map_ext/drafts_reference/set2.txt'

create_dirs_path = '/home/georgelab/Documents/Lieselot/Sergei/Cell_map_ext/CellMap/create_dirs.py'

pipeline1_path = '/home/georgelab/Documents/Lieselot/Sergei/Cell_map_ext/ilastik/pipeline1_single.py'
cell_detection_path = '/home/georgelab/Documents/Lieselot/Sergei/Cell_map_ext/ilastik/detect.py'
pipeline2_path = '/home/georgelab/Documents/Lieselot/Sergei/Cell_map_ext/ilastik/pipeline2.py'

trained_model_path = '/home/georgelab/Documents/Lieselot/Sergei/R1_3d_0.ilp'


#%% create dict of directories
#exec(open(create_dirs_path).read())

#%% run analysis

import sys 
sys.path.append('/home/georgelab/Documents/ClearMap2')
  
from ClearMap.Environment import *  #analysis:ignore
  
#directories and files
directory = '/media/georgelab/LaCie1/Lieselot_Collab/INTOX_Durakilmed/i4' #fill in the directory to a specific brain

print("processing brain at", directory)
  
expression_raw      = '/220324_i4red_13-05-47/13-05-47_i4red_UltraII_C00_xyz-Table Z<Z,4>.ome.tif' #fill in the raw path
expression_auto     = '/220325_i4green_07-46-45/07-46-45_i4green_UltraII_C00_xyz-Table Z<Z,4>.ome.tif' #fill in the auto path  
  
ws = wsp.Workspace('CellMap', directory=directory);
ws.update(raw=expression_raw, autofluorescence=expression_auto)
ws.info()
  
ws.debug = False
  
resources_directory = settings.resources_path

exec(open(pipeline1_path).read()) #runs the CellMap pipeline up to cell_detection

data_path = directory + "/stitched.npy"
output_path = directory + "/cells_detected.npy" #check the file name
cells_raw_path = directory + "/cells_raw_i.npy"

#tester directories
#data_path = directory + "/ilastik/test.npy"
#output_path = directory + "/ilastik/cells_detected.npy"
     
exec(open(cell_detection_path).read())

exec(open(pipeline2_path).read())

