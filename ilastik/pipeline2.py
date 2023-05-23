# -*- coding: utf-8 -*-
"""
Created on Sun May 14 21:38:38 2023

@author: serge
"""

 #%%############################################################################
 ### Cell atlas alignment and annotation
 ###############################################################################
 
#%% Cell alignment

source = ws.source('cells', postfix='raw_i')

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

io.write(ws.filename('cells_i'), cells_data)
 
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
 
source = ws.source('cells_i');
header = ', '.join([h[0] for h in source.dtype.names]);
np.savetxt(ws.filename('cells_i', extension='csv'), source[:], header=header, delimiter=',', fmt='%s')
 
 #%% ClearMap 1.0 export
 
source = ws.source('cells_i');

clearmap1_format = {'points' : ['x', 'y', 'z'], 
                    'points_transformed' : ['xt', 'yt', 'zt'],
                    'intensities' : ['source', 'dog', 'background', 'size']}

for filename, names in clearmap1_format.items():
  sink = ws.filename('cells_i', postfix=['ClearMap1', filename]);
  data = np.array([source[name] if name in source.dtype.names else np.full(source.shape[0], np.nan) for name in names]);
  io.write(sink, data);