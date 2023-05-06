# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 11:58:12 2023

@author: serge

This file is a part of pipeline_streamline.py. It carries out the cell detection
and filtering as well as creates plottable versions of output arrays

"""

import os

#Parameters for block processing   for 128GB RAM  6, 100,50,16, chunkoptTrue, chunkoptsizeall, processparaellel
processing_parameter = cells.default_cell_detection_processing_parameter.copy();
processing_parameter.update(
      processes = 12, # 32, 6, 'serial',
      size_max = 100, #100, #35, 20 35     
      size_min = 50,# 30, #30, 11  25
      overlap  = 4, #32, #10, 10  10
      verbose = True
      )

#Initialize paths
d_cells_raw_path = '/media/georgelab/LaCie/Lieselot_Collab/INTOX_Durakilmed/i1/debug_cells_raw.npy'
d_cells_raw_plot_path = '/media/georgelab/LaCie/Lieselot_Collab/INTOX_Durakilmed/i1/debug_cells_raw_plot.npy'
d_cells_filt_path = '/media/georgelab/LaCie/Lieselot_Collab/INTOX_Durakilmed/i1/debug_cells_filtered.npy'
d_cells_filt_plot_path = '/media/georgelab/LaCie/Lieselot_Collab/INTOX_Durakilmed/i1/debug_cells_filtered_plot.npy'

source_path = '/home/georgelab/Documents/Lieselot/Sergei/Cell_map_ext/CellMap/create_plottable.py'
  
#Prepare workspace
ws.create_debug('stitched', slicing=slicing);

io.delete_file(ws.filename('cells', postfix='maxima')) # deletes existing cells maxima file

if(os.path.isfile(d_cells_raw_plot_path)):
    os.remove(d_cells_raw_plot_path)
    print("deletion one successful")
if(os.path.isfile(d_cells_filt_plot_path)):
    os.remove(d_cells_filt_plot_path)
    print("deletion two successful")

#Detect and filter
cells.detect_cells(ws.filename('stitched'), ws.filename('cells', postfix='raw'),
                     cell_detection_parameter=cell_detection_parameter, 
                     processing_parameter=processing_parameter)
  
cells.filter_cells(source = ws.filename('cells', postfix='raw'), 
                     sink = ws.filename('cells', postfix='filtered'), 
                     thresholds=thresholds);
  
#Creat plottable .npy arrays to plat against stitched  
exec(open(source_path).read()) 

create_plottable_cells(d_cells_raw_path, d_cells_raw_plot_path, shape)  
create_plottable_cells(d_cells_filt_path, d_cells_filt_plot_path, shape)