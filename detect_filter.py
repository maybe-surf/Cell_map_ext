# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 11:58:12 2023

@author: serge
"""

#%% 
    #Parameters for block processing   for 128GB RAM  6, 100,50,16, chunkoptTrue, chunkoptsizeall, processparaellel
  processing_parameter = cells.default_cell_detection_processing_parameter.copy();
  processing_parameter.update(
      processes = 12, # 32, 6, 'serial',
      size_max = 100, #100, #35, 20 35     
      size_min = 50,# 30, #30, 11  25
      overlap  = 4, #32, #10, 10  10
      verbose = True
      )
  
#%%
  ws.create_debug('stitched', slicing=slicing);
  ws.debug = True;

  io.delete_file(ws.filename('cells', postfix='maxima')) # deletes existing cells maxima file
  
  cells.detect_cells(ws.filename('stitched'), ws.filename('cells', postfix='raw'),
                     cell_detection_parameter=cell_detection_parameter, 
                     processing_parameter=processing_parameter)
  
  d_cells_raw_path = '/media/georgelab/LaCie/Lieselot_Collab/INTOX_Durakilmed/i1/debug_cells_raw.npy'
  d_cells_raw_plot_path = '/media/georgelab/LaCie/Lieselot_Collab/INTOX_Durakilmed/i1/debug_cells_raw_plot.npy'
  
  source_path = '/home/georgelab/Documents/Lieselot/Sergei/Cell_map_ext/create_plottable.py'
  
  exec(open(source_path).read())
  
  create_plottable_cells(d_cells_raw_path, d_cells_raw_plot_path, shape)
  
  d_cells_filt_path = '/media/georgelab/LaCie/Lieselot_Collab/INTOX_Durakilmed/i1/debug_cells_filtered.npy'
  d_cells_filt_plot_path = '/media/georgelab/LaCie/Lieselot_Collab/INTOX_Durakilmed/i1/debug_cells_filtered_plot.npy'
  
  create_plottable_cells(d_cells_filt_path, d_cells_filt_plot_path, shape)