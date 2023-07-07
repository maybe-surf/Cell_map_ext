# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 20:43:35 2023

@author: serge
"""

#%% Set paths
set1_path = '/home/georgelab/Documents/Lieselot/Sergei/Cell_map_ext/drafts_reference/set1.txt'
set2_path = '/home/georgelab/Documents/Lieselot/Sergei/Cell_map_ext/drafts_reference/set2.txt'

create_dirs_path = '/home/georgelab/Documents/Lieselot/Sergei/Cell_map_ext/CellMap/create_dirs.py'

#pipeline1_path = '/home/georgelab/Documents/Lieselot/Sergei/Cell_map_ext/ilastik/pipeline1.py'
cell_detection_path = '/home/georgelab/Documents/Lieselot/Sergei/Cell_map_ext/ilastik/detect.py'
pipeline2_path = '/home/georgelab/Documents/Lieselot/Sergei/Cell_map_ext/ilastik/pipeline2.py'

trained_model_path = '/home/georgelab/Documents/Lieselot/Sergei/R1_3d_0.ilp'

#%%
exec(open(create_dirs_path).read())

#%%
def get_counts(directory, folder):
    import pandas as pd
    import os.path
    if(not os.path.isfile(directory + '/cells_i.csv')):
        print("not analyzed with ilastik")
        return
    brain_dir = directory.split('/')
    brain_name = brain_dir[-1]
    df = pd.read_csv (directory + '/cells_i.csv', error_bad_lines=False, index_col=False)
    counts = df[' n'].value_counts()
    counts = counts.to_frame()
    counts.index.name = 'region'
    counts.reset_index(inplace=True)
    counts = counts.rename(columns={" n" : brain_name})
    counts.to_csv(directory + '/counts_i_' + brain_name + '.csv', index = False)
    counts.to_csv(folder + '/counts_' + brain_name + '.csv', index = False) 

#%% run analysis

num_brains = 0
limit = 0

for brain in dirs.keys():
    # if(num_brains < 27):
    #     num_brains += 1
    #     continue
    brain_dirs = dirs.get(brain)

    #directories and files
    directory = brain_dirs.get("dir_brain")  #1 animal 
    print("processing brain at", directory)
    folder = "/media/georgelab/Rett1/Counts_ilastik"
    
    get_counts(directory, folder)
    
    num_brains += 1
#    if(num_brains == limit):
#        break






























