#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 17:25:56 2023

@author: georgelab
"""

  #%%% Original from the parameter file

  cell_detection_parameter = cells.default_cell_detection_parameter.copy();
  # cell_detection_parameter['iullumination_correction'] = dict(flatfield = None, scaling = 'mean');
  # cell_detection_parameter['background_correction'] = dict(shape = (10,10), form = 'Disk', save = False);
  # cell_detection_parameter['dog_filter'] = dict(shape = None, sigma = None, sigma2 = None),;
  # cell_detection_parameter['maxima_detection'] = dict(h_max = None, shape = 5, threshold = 0, valid = True, save = False);
  # cell_detection_parameter['shape_detection'] - dict(threshold = 700, save = False)
  # cell_detection_parameter['intensity_detection']= dict(method = 'max', shape = 3, measure = ['source', 'background'])


  #%% Hammond
  
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


  #%% Alex
  cell_detection_parameter = cells.default_cell_detection_parameter.copy();

  cell_detection_parameter['dog_filter'] = dict(shape = (7,7,7)); #(6,6,11)
  cell_detection_parameter['shape_detection']['threshold'] = 500


