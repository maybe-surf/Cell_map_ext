# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 11:52:46 2023

@author: serge
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
  ws.debug = True

  slicing = (slice(300, 600),slice(1200, 1500),slice(950, 1050));
  
  shape = [300, 300, 100] #manually calculated based of slicing
  
  cell_detection_parameter = cells.default_cell_detection_parameter.copy();
  #cell_detection_parameter['iullumination_correction']['flatfield'] = None;
  #cell_detection_parameter['background'] = None;
  cell_detection_parameter['background_correction']['shape'] = (7,7);
  cell_detection_parameter['background_correction']['form'] = 'Disk';
  #cell_detection_parameter['background_correction']['save'] = ws.filename('cells', postfix='bgremove');
  cell_detection_parameter['intensity_detection']['measure'] = ['source'];
  #cell_detection_parameter['shape_detection']['threshold'] = 1200;
  
  cell_detection_parameter['maxima_detection']['shape'] = 3 #5 #size of structural element - should be near typical size of cell
  cell_detection_parameter['maxima_detection']['threshold'] = 700 #only maxima above this intensity are detected
  cell_detection_parameter['maxima_detection']['save'] = ws.filename('cells', postfix='maxima')
  
  thresholds = { # can filter on any column in the cells table
      'source' : None, #Measured intensity-
      'size'   : (20,900) #filter cells based on size range
      }
  
#%%

  code_path = '/home/georgelab/Documents/Lieselot/Sergei/Cell_map_ext/detect_filter.py'  
  
  exec(open(code_path).read())
 
  