# -*- coding: utf-8 -*-
"""
Created on Fri May 12 00:11:38 2023

@author: serge
"""

 
 #%% Aignment - resampled to autofluorescence (>2min - update elastix to v5 for improved speed?)
 #33 sec
 ## returns the directory elastix_resampled_to_auto
 
 # align the two channels
align_channels_parameter = {            
    #moving and reference images
    "moving_image" : ws.filename('resampled', postfix='autofluorescence'),
    "fixed_image"  : ws.filename('resampled'),
    
    #elastix parameter files for alignment
    "affine_parameter_file"  : align_channels_affine_file,
    "bspline_parameter_file" : None,
    
    #directory of the alig'/home/nicolas.renier/Documents/ClearMap_Ressources/Par0000affine.txt',nment result
    "result_directory" :  ws.filename('resampled_to_auto')
    }; 

elx.align(**align_channels_parameter);
 
 #%% Alignment - autoflourescence to reference - 7-9min (update elastix to v5 for improved speed)
 #4 minutes
 #returns the directory elastix_auto_to_reference
 
 # align autofluorescence to reference
align_reference_parameter = {            
    #moving and reference images
    "moving_image" : reference_file,
    "fixed_image"  : ws.filename('resampled', postfix='autofluorescence'),
    
    #elastix parameter files for alignment
    "affine_parameter_file"  :  align_reference_affine_file,
    "bspline_parameter_file" :  align_reference_bspline_file,
    #directory of the alignment result
    "result_directory" :  ws.filename('auto_to_reference')
    };

elx.align(**align_reference_parameter);