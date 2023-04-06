#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 20:42:13 2023

@author: georgelab
"""

#%%
  #import the up to cell detection spydata before running this script
  
  import sys 
  sys.path.append('/home/georgelab/Documents/ClearMap2')
  
  from ClearMap.Environment import *  #analysis:ignore
  
  #directories and files
  directory = '/media/georgelab/LaCie/Lieselot_Collab/INTOX_Durakilmed/i1'  #1 animal  
  
  expression_raw      = '/220323_i1red_13-23-37/13-23-37_i1red_UltraII_C00_xyz-Table Z<Z,4>.ome.tif'     #neurons      
  expression_auto     = '/220323_i1green_13-01-55/13-01-55_i1green_UltraII_C00_xyz-Table Z<Z,4>.ome.tif'  #structure
  
  ws = wsp.Workspace('CellMap', directory=directory);
  ws.update(raw=expression_raw, autofluorescence=expression_auto)
  ws.info()
  
  ws.debug = False
  
  resources_directory = settings.resources_path
  
  #%% Crop test data 
  
  #select sublice for testing the pipeline
  slicing = (slice(300, 600),slice(1200, 1500),slice(950, 1050));
  ws.create_debug('stitched', slicing=slicing);
  ws.debug = True; 
  
  
  #%% Cell detection:  Aprox 7min
  
  cell_detection_parameter = cells.default_cell_detection_parameter.copy();
  #cell_detection_parameter['iullumination_correction']['flatfield'] = None;
  #cell_detection_parameter['background'] = None;
  cell_detection_parameter['background_correction']['shape'] = (7,7);
  cell_detection_parameter['background_correction']['form'] = 'Disk';
  #cell_detection_parameter['background_correction']['save'] = ws.filename('cells', postfix='bgremove');
  cell_detection_parameter['intensity_detection']['measure'] = ['source'];
  #cell_detection_parameter['shape_detection']['threshold'] = 1200;
  
  io.delete_file(ws.filename('cells', postfix='maxima')) # deletes existing cells maxima file
  cell_detection_parameter['maxima_detection']['shape'] = 3 #5 #size of structural element - should be near typical size of cell
  cell_detection_parameter['maxima_detection']['threshold'] = 700 #only maxima above this intensity are detected
  cell_detection_parameter['maxima_detection']['save'] = ws.filename('cells', postfix='maxima')
 
  #Parameters for block processing   for 128GB RAM  6, 100,50,16, chunkoptTrue, chunkoptsizeall, processparaellel
  processing_parameter = cells.default_cell_detection_processing_parameter.copy();
  processing_parameter.update(
      processes = 12, # 32, 6, 'serial',
      size_max = 100, #100, #35, 20 35     
      size_min = 50,# 30, #30, 11  25
      overlap  = 4, #32, #10, 10  10
      verbose = True
      )
  
  cells.detect_cells(ws.filename('stitched'), ws.filename('cells', postfix='raw'),
                     cell_detection_parameter=cell_detection_parameter, 
                     processing_parameter=processing_parameter)
  
  #%%
  #creating cells raw plottable file
  d_cells_raw_path = '/media/georgelab/LaCie/Lieselot_Collab/INTOX_Durakilmed/i1/debug_cells_raw.npy'
  d_cells_raw_plot_path = '/media/georgelab/LaCie/Lieselot_Collab/INTOX_Durakilmed/i1/debug_cells_raw_plot.npy'
  shape = [300, 300, 100] #manually calculated
  source_path = '/home/georgelab/Documents/Lieselot/Sergei/Cell_map_ext/create_plottable.py'
  
  exec(open(source_path).read())
  
  create_plottable_cells(d_cells_raw_path, d_cells_raw_plot_path, shape)
  
  
  
  
  #%%
  thresholds = { # can filter on any column in the cells table
      'source' : None, #Measured intensity
      'size'   : (20,900) #filter cells based on size range
      }
  
  cells.filter_cells(source = ws.filename('cells', postfix='raw'), 
                     sink = ws.filename('cells', postfix='filtered'), 
                     thresholds=thresholds);
  
  
  source = ws.source('cells', postfix='filtered')