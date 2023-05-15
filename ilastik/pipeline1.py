# -*- coding: utf-8 -*-
"""
Created on Fri May 12 00:11:38 2023

@author: serge
"""

#%% Initialize alignment 

annotation_file, reference_file, distance_file=ano.prepare_annotation_files(
      slicing=(slice(None),slice(None),slice(0,228)), orientation=(1,2,3),
      overwrite=False, verbose=True);
  
  #alignment parameter files    
align_channels_affine_file   = io.join(resources_directory, 'Alignment/align_affine.txt')
align_reference_affine_file  = io.join(resources_directory, 'Alignment/align_affine.txt')
align_reference_bspline_file = io.join(resources_directory, 'Alignment/align_bspline.txt')
  
  
  #%%############################################################################
  ### Data conversion
  ############################################################################### 
  
 #%% Convet raw data to npy file 
 # Outputs stitched.npy    
              
source = ws.source('raw');
sink   = ws.filename('stitched')
io.delete_file(sink)
io.convert(source, sink, processes=None, verbose=True);
 
 #%%############################################################################
 ### Resampling and atlas alignment 
 ###############################################################################
       
 #%% Resample 
 #Outputs resampled.tif
            
resample_parameter = {
    "source_resolution" : (4.0625, 4.0625, 3),
    "sink_resolution"   : (25,25,25),
    "processes" : 4,
    "verbose" : True,             
    "orientation":(-1,2,3) 
    };

io.delete_file(ws.filename('resampled'))

res.resample(ws.filename('stitched'), sink=ws.filename('resampled'), **resample_parameter)
 
 #%% Resample autofluorescence
 #Outputs resampled_auto.tif
     
resample_parameter_auto = {
    "source_resolution" : (4.0625,4.0625,3),
    "sink_resolution"   : (25,25,25),
    "processes" : 4,
    "verbose" : True,                
    "orientation":(-1,2,3) 
    };   

res.resample(ws.filename('autofluorescence'), sink=ws.filename('resampled', postfix='autofluorescence'), **resample_parameter_auto)
 
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