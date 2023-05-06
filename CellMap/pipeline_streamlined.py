# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 11:52:46 2023

@author: serge

This script is used to test different processing and cell_detection parameters for CellMap.
It assumes that a .spydata file is imported so that you don't have to rerun the entire
pipeline every time to test a new set of parameters
"""

#%%
  #import the "up to cell detection spydata" before running this script from Documents/Lieselot/Sergei 
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
  
  #%%
  
  io.delete_file(ws.filename('cells', postfix='maxima')) # deletes existing cells maxima file
  io.delete_file(ws.filename('cells', postfix='bgremove')) # deletes existing cells maxima file
  ws.debug = True

  slicing = (slice(300, 600),slice(1200, 1500),slice(950, 1050));
  
  shape = [300, 300, 100] #manually calculated based of slicing
  
  thresholds = { # can filter on any column in the cells table
      'source' : None, #Measured intensity-
      'size'   : (20,900) #filter cells based on size range
      }
  
  #%% Default - too few detections
  cell_detection_parameter = cells.default_cell_detection_parameter.copy();


  cell_detection_parameter['maxima_detection']['save'] = ws.filename('cells', postfix='maxima')
  
  
  #%% Hammond - too few detections
   cell_detection_parameter = cells.default_cell_detection_parameter.copy();
  #cell_detection_parameter['iullumination_correction']['flatfield'] = None;
  #cell_detection_parameter['dog_filter'] = dict(shape = None, sigma = None, sigma2 = None),;

  cell_detection_parameter['background_correction']['shape'] = (7,7);
  cell_detection_parameter['background_correction']['form'] = 'Disk';
  #cell_detection_parameter['background_correction']['save'] = ws.filename('cells', postfix='bgremove');
    
  cell_detection_parameter['maxima_detection']['shape'] = 3 #5 #size of structural element - should be near typical size of cell
  cell_detection_parameter['maxima_detection']['threshold'] = 700 #only maxima above this intensity are detected
  #cell_detection_parameter['maxima_detection']['save'] = ws.filename('cells', postfix='maxima')

  cell_detection_parameter['shape_detection']['threshold'] = 1200;

  cell_detection_parameter['intensity_detection']['measure'] = ['source']
  
  #%% Alex - most detections are false but close
  cell_detection_parameter = cells.default_cell_detection_parameter.copy();

  cell_detection_parameter['dog_filter'] = dict(shape = (7,7,7)); #(6,6,11)
  cell_detection_parameter['shape_detection']['threshold'] = 500
  
  #%% Sergei 1 - almost as good as Sergei 2
  cell_detection_parameter = cells.default_cell_detection_parameter.copy();
  cell_detection_parameter['background_correction']['shape'] = (7, 7); # 3;
  cell_detection_parameter['background_correction']['form'] = 'Disk';
  cell_detection_parameter['intensity_detection']['measure'] = ['source'];  
  cell_detection_parameter['maxima_detection']['shape'] = 3 #5 #size of structural element - should be near typical size of cell
  cell_detection_parameter['maxima_detection']['threshold'] = 400 #450 #700 #only maxima above this intensity are detected
  cell_detection_parameter['maxima_detection']['save'] = ws.filename('cells', postfix='maxima')
  cell_detection_parameter['shape_detection']['threshold'] = 450
  
  #%% Sergei 2 - optimal as of 04/11/2023 7pm
  cell_detection_parameter = cells.default_cell_detection_parameter.copy();
  cell_detection_parameter['background_correction']['shape'] = (10, 10); # 3;
  cell_detection_parameter['background_correction']['form'] = 'Disk';
  cell_detection_parameter['background_correction']['save'] = ws.filename('cells', postfix='bgremove');
  cell_detection_parameter['intensity_detection']['measure'] = ['source'];
  cell_detection_parameter['maxima_detection']['shape'] = 3 #5 #size of structural element - should be near typical size of cell
  cell_detection_parameter['maxima_detection']['threshold'] = 400 #450 #700 #only maxima above this intensity are detected
  cell_detection_parameter['maxima_detection']['save'] = ws.filename('cells', postfix='maxima')
  cell_detection_parameter['shape_detection']['threshold'] = 450
  
  #%% Sergei 3 - bad, too many false positives
  cell_detection_parameter = cells.default_cell_detection_parameter.copy();
  cell_detection_parameter['background_correction'] = None
  cell_detection_parameter['maxima_detection']['shape'] = 3 #5 #size of structural element - should be near typical size of cell
  cell_detection_parameter['maxima_detection']['threshold'] = 400 #450 #700 #only maxima above this intensity are detected
  cell_detection_parameter['maxima_detection']['save'] = ws.filename('cells', postfix='maxima')
  cell_detection_parameter['shape_detection']['threshold'] = 450
  
  
  #%% Lieselot 1
  cell_detection_parameter = cells.default_cell_detection_parameter.copy();
  #cell_detection_parameter['iullumination_correction']['flatfield'] = None;

  cell_detection_parameter['background_correction']['shape'] = (30, 30);
  cell_detection_parameter['background_correction']['form'] = 'Disk';
  cell_detection_parameter['background_correction']['save'] = ws.filename('cells', postfix='bgremove');
  
  #%% Lieselot 2
  cell_detection_parameter = cells.default_cell_detection_parameter.copy();
  cell_detection_parameter['iullumination_correction']['flatfield'] = None;
  cell_detection_parameter['background_correction'] = None;
  cell_detection_parameter['shape_detection']['threshold'] = 1500
    
  #%% Lieselot 3
  cell_detection_parameter = cells.default_cell_detection_parameter.copy();
  cell_detection_parameter['iullumination_correction'] = None
  #cell_detection_parameter['background_correction'] = None;
  #cell_detection_parameter['shape_detection']['threshold'] = 500;
  
  #cell_detection_parameter['maxima_detection'] = None;
  #cell_detection_parameter['intensity_detection']['measure'] = None;
  #cell_detection_parameter['dog_filter'] = None

  #%% Sergei 4
  cell_detection_parameter = cells.default_cell_detection_parameter.copy();
  cell_detection_parameter['background_correction']['shape'] = (10, 10); # 3;
  cell_detection_parameter['background_correction']['form'] = 'Disk';
  cell_detection_parameter['background_correction']['save'] = ws.filename('cells', postfix='bgremove');
  cell_detection_parameter['intensity_detection']['measure'] = ['source'];
  cell_detection_parameter['maxima_detection']['shape'] = 2 #5 #size of structural element - should be near typical size of cell
  cell_detection_parameter['maxima_detection']['threshold'] = 300 #450 #700 #only maxima above this intensity are detected
  cell_detection_parameter['maxima_detection']['save'] = ws.filename('cells', postfix='maxima')
  cell_detection_parameter['shape_detection']['threshold'] = 300
  
  #%% Sergei 5
  cell_detection_parameter = cells.default_cell_detection_parameter.copy();
  cell_detection_parameter['background_correction']['shape'] = (12, 12); # 3;
  cell_detection_parameter['background_correction']['form'] = 'Disk';
  cell_detection_parameter['background_correction']['save'] = ws.filename('cells', postfix='bgremove');
  cell_detection_parameter['intensity_detection']['measure'] = ['source'];
  cell_detection_parameter['maxima_detection']['shape'] = 3 #5 #size of structural element - should be near typical size of cell
  cell_detection_parameter['maxima_detection']['threshold'] = 400 #450 #700 #only maxima above this intensity are detected
  cell_detection_parameter['maxima_detection']['save'] = ws.filename('cells', postfix='maxima')
  cell_detection_parameter['shape_detection']['threshold'] = 400
#%%

  code_path = '/home/georgelab/Documents/Lieselot/Sergei/Cell_map_ext/CellMap/detect_filter.py'  
  
  exec(open(code_path).read())
 
  