# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 00:19:30 2023

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
 
 #%%############################################################################
 ### Cell detection
 ###############################################################################
 
 #%% Cell detection:  Aprox 7min
 
cell_detection_parameter = cells.default_cell_detection_parameter.copy();

io.delete_file(ws.filename('cells', postfix='maxima'))

cell_detection_parameter['background_correction']['shape'] = (10, 10); # 3;
cell_detection_parameter['background_correction']['form'] = 'Disk';
cell_detection_parameter['intensity_detection']['measure'] = ['source'];
cell_detection_parameter['maxima_detection']['shape'] = 3 #5 #size of structural element - should be near typical size of cell
cell_detection_parameter['maxima_detection']['threshold'] = 400 #450 #700 #only maxima above this intensity are detected
cell_detection_parameter['shape_detection']['threshold'] = 450

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
 
 
 #%% Filter cells and plot filtered cell statistics
 
 # thresholds = { # can filter on any column in the cells table
 #     'source' : None, #Measured intensity
 #     'size'   : (20,900) #filter cells based on size range
 #     }
 
 # cells.filter_cells(source = ws.filename('cells', postfix='raw'), 
 #                    sink = ws.filename('cells', postfix='filtered'), 
 #                    thresholds=thresholds);
 

 
 #%%############################################################################
 ### Cell atlas alignment and annotation
 ###############################################################################
 
#%% Cell alignment

source = ws.source('cells', postfix='raw')

def transformation(coordinates):
  coordinates = res.resample_points(
                  coordinates, sink=None, orientation=None, 
                  source_shape=io.shape(ws.filename('stitched')), 
                  sink_shape=io.shape(ws.filename('resampled')));
  
  coordinates = elx.transform_points(
                  coordinates, sink=None, 
                  transform_directory=ws.filename('resampled_to_auto'), 
                  binary=True, indices=False);
  
  coordinates = elx.transform_points(
                  coordinates, sink=None, 
                  transform_directory=ws.filename('auto_to_reference'),
                  binary=True, indices=False);
      
  return coordinates;
  

coordinates = np.array([source[c] for c in 'xyz']).T;

coordinates_transformed = transformation(coordinates);
 
#%% Cell annotation
 # *** by default this script only provides graph order - which may confuse some users after region ID
 # updated to include ID and acronyms
 
label = ano.label_points(coordinates_transformed, key='order');
names = ano.convert_label(label, key='order', value='name');
 
 #ID = ano.convert_label(label, key='order', value='id');
 #acronym = ano.convert_label(label, key='order', value='acronym');
 
 #%% Save results
 
coordinates_transformed.dtype=[(t,float) for t in ('xt','yt','zt')]
label = np.array(label, dtype=[('order', int)]);
names = np.array(names, dtype=[('name' , 'U256')])

import numpy.lib.recfunctions as rfn
cells_data = rfn.merge_arrays([source[:], coordinates_transformed, label, names], flatten=True, usemask=False)

io.write(ws.filename('cells'), cells_data)
 
 #%% Save results
 #adding in ID and acronyms as above
 #IMPORTANT - names should be final column, as comma seperated names create additional columns and 
 #will mix entries in columns to the right of the names column
 # keep in mind, first letter of column name used in output - so "atlas_ID" and "acronym" would be both be save to column "a"
 
 # coordinates_transformed.dtype=[(t,float) for t in ('xt','yt','zt')]
 # label = np.array(label, dtype=[('order', int)]);
 # names = np.array(names, dtype=[('name' , 'U256')])
 # ID = np.array(ID, dtype=[('id' , int)])
 # acronym = np.array(acronym, dtype=[('acronym' , 'U256')])
 
 # import numpy.lib.recfunctions as rfn
 # cells_data = rfn.merge_arrays([source[:], coordinates_transformed, label, ID, acronym, names], flatten=True, usemask=False)
 
 # io.write(ws.filename('cells'), cells_data)
   
 
 
 #%%############################################################################
 ### Cell csv generation for external analysis
 ###############################################################################
 
 #%% CSV export
 
source = ws.source('cells');
header = ', '.join([h[0] for h in source.dtype.names]);
np.savetxt(ws.filename('cells', extension='csv'), source[:], header=header, delimiter=',', fmt='%s')
 
 #%% ClearMap 1.0 export
 
source = ws.source('cells');

clearmap1_format = {'points' : ['x', 'y', 'z'], 
                    'points_transformed' : ['xt', 'yt', 'zt'],
                    'intensities' : ['source', 'dog', 'background', 'size']}

for filename, names in clearmap1_format.items():
  sink = ws.filename('cells', postfix=['ClearMap1', filename]);
  data = np.array([source[name] if name in source.dtype.names else np.full(source.shape[0], np.nan) for name in names]);
  io.write(sink, data);