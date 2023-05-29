# -*- coding: utf-8 -*-
"""
Created on Thu May 25 23:35:33 2023

@author: serge
"""
#%%
# import pandas as pd
# pd.options.mode.chained_assignment = None  # default='warn'

# #index = 9 #???????

# mecp2 = pd.DataFrame([])
# fos = pd.DataFrame([])


# counts = {}

# for cell in fos.iterrows():
#     if(cell[0] % 1000 == 0):
#         print("processing cell", cell[0])
#     cell = cell[1]
#     consider = mecp2[mecp2["name"] == cell["name"]]
#     consider["dist_sq"] = (consider["x"]-cell[0])**2 + (consider["y"]-cell[1])**2 + (consider["z"]-cell[2])**2
#     if(consider["dist_sq"].min() < 225):
#         if(cell["name"] in counts.keys()):
#             counts.update({cell["name"] : counts.get(cell["name"])+1})
#         else:
#             counts.update({cell["name"] : 1})
#         break
    
#fos["min_dist_sq"] =        
    
#%%
#import numpy as np
# cells_mecp2_path = "/media/georgelab/LaCie/Lieselot_double/LC3/C00-mecp2/cells_raw.npy"
# cells_fos_path = "/media/georgelab/LaCie/Lieselot_double/LC3/C01-fos/cells_raw.npy"
# create_plot_path = "/home/georgelab/Documents/Lieselot/Sergei/Cell_map_ext/CellMap/create_plottable.py"

# mecp2 = np.load(cells_mecp2_path)
# print("loaded mecp2")
# fos = np.load(cells_fos_path)
# print("loaded fos")

# exec(open(create_plot_path).read())

# shape = [2160, 2560, 1988]
# mecp2_full = []#create_plottable_cells3(mecp2, shape)
# print("created plottable")

# xy_margin = 4 #16 micron
# z_margin = 5 #15 micron

# overlap = 0

# i = 0
# for cell in fos:
#     if(i % 1000):
#         print("on the cell", i)
#     i += 1
#     consider = mecp2_full[(cell[0]-xy_margin):(cell[0]+xy_margin), (cell[1]-xy_margin):(cell[1]+xy_margin), (cell[2]-z_margin):(cell[2]+z_margin)]
#     if(sum(sum(sum(consider))) > 0):
#         overlap += 1

#%% load the data
import numpy as np
directory = ""
mecp2_path = ""
fos_path = ""
cells_mecp2_path = mecp2_path + "/cells.npy"
cells_fos_path = fos_path + "/cells.npy"
create_plot_path = "/home/georgelab/Documents/Lieselot/Sergei/Cell_map_ext/CellMap/create_plottable.py"

out_path = directory + "count_overlap.csv"

mecp2 = np.load(cells_mecp2_path)
print("loaded mecp2")
fos = np.load(cells_fos_path)
print("loaded fos")

#%% define functions

def create_slice(shape, x, y, z, xy_margin, z_margin):
    nums = [(x-xy_margin), (x+xy_margin), (y-xy_margin), (y+xy_margin), (z-z_margin), (z+z_margin)]
    if(nums[0] < 0):
        nums[0] = 0
    if(nums[2] < 0):
        nums[2] = 0
    if(nums[4] < 0):
        nums[4] = 0
    if(nums[1] >= shape[0]):
        nums[1] = shape[0]
    if(nums[3] >= shape[1]):
        nums[3] = shape[1]
    if(nums[5] >= shape[2]):
        nums[5] = shape[2]
    return nums

def add_to_dict(cell, counts, overlap):
    if(overlap):
        if(cell[index] in counts.keys()):
            data = counts.get(cell[index])
            counts.update({cell[index] : (data[0]+1, data[1]+1)})
        else:
            counts.update({cell[index] : (1, 1)})
    else:
        if(cell[index] in counts.keys()):
            data = counts.get(cell[index])
            counts.update({cell[index] : (data[0], data[1]+1)})
        else:
            counts.update({cell[index] : (0, 1)})
    

def merge_res(res_list):
    overlap_dict = {}
    overlap = 0
    total = 0
    for res in res_list:
        cells_dict = res[0]
        for key in cells_dict.keys():
            if key in overlap_dict.keys():
                data_old = overlap_dict.get(key)
                data_add = cells_dict.get(key)
                overlap_dict.update({key : (data_old[0]+data_add[0], data_old[1]+data_add[1])})
            else:
                overlap_dict.update({key : cells_dict.get(key)})
        overlap += res[1]
        total += res[2]
    return (overlap_dict, overlap, total)
    

def count_overlap_slice(cells_slice, full, xy_margin, z_margin, shape, qq):
    print("started processing slice")
    overlap = 0
    total = 0
    counts = {}
    for cell in cells_slice:
        if(total % 500000 == 0):
            print("on the cell", total)
        total += 1
        coords = create_slice(shape, cell[0], cell[1], cell[2], xy_margin, z_margin)
        consider = full[coords[0]:coords[1], coords[2]:coords[3], coords[4]:coords[5]]
        if(type(consider) == int):
            test = consider
        elif(len(consider.shape) == 1):
            test = sum(consider)
        elif(len(consider.shape) == 2):
            test = sum(sum(consider))
        else:
            test = sum(sum(sum(consider)))
        if(test > 0):
            overlap += 1
            add_to_dict(cell, counts, True)
        else:
            add_to_dict(cell, counts, False)
    qq.put((counts, overlap, total))
    print("done processing slice")
            
#%% prepare worksapce
import multiprocessing as mp
import time
shape = [2160, 2560, 1989]
xy_margin = 2 #16 micron
z_margin = 2 #15 micron
num_cores = 8
index = 9
exec(open(create_plot_path).read())

#%% fos in mecp2
mecp2_full = [] #create_plottable_cells3(mecp2, shape)
print("created plottable mecp2")

fos_list = np.array_split(fos, num_cores, axis = 0)
fos_res = []

qq = mp.Queue()
processes = []

start = time.time()
for fos_slice in fos_list:
    p = mp.Process(target = count_overlap_slice, args = (fos_slice, mecp2_full, xy_margin, z_margin, shape, qq))
    processes.append(p)
    p.start()

while 1:
    running = any(p.is_alive() for p in processes)
    while not qq.empty():
        fos_res.append(qq.get())
    if not running:
        break

for p in processes:
    p.join()

fos_data = merge_res(fos_res)
end = time.time()

print("done with fos in mecp2 in", end-start)

#%% mecp2 in fos
fos_full = []#create_plottable_cells3(fos, shape)
print("created plottable fos")

mecp2_list = np.array_split(mecp2, num_cores, axis = 0)
mecp2_res = []

qq = mp.Queue()
processes = []

start = time.time()
for mecp2_slice in mecp2_list:
    p = mp.Process(target = count_overlap_slice, args = (mecp2_slice, fos_full, xy_margin, z_margin, shape, qq))
    processes.append(p)
    p.start()

while 1:
    running = any(p.is_alive() for p in processes)
    while not qq.empty():
        mecp2_res.append(qq.get())
    if not running:
        break

for p in processes:
    p.join()

mecp2_data = merge_res(mecp2_res)
end = time.time()

print("done with mecp2 in fos in", end-start)

#%% Export
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

fos_df = pd.DataFrame(fos_data[0])
fos_df = fos_df.T
fos_df.loc["total_fos"] = [fos_data[1], fos_data[2]]
fos_df.rename(columns={0:"fos_in_mecp2", 1:"total_fos"}, inplace = True)
fos_df["percent_fos"] = fos_df["fos_in_mecp2"]/fos_df["total_fos"]*100

mecp2_df = pd.DataFrame(mecp2_data[0])
mecp2_df = mecp2_df.T
mecp2_df.loc["total_mecp2"] = [mecp2_data[1], mecp2_data[2]]
mecp2_df.rename(columns={0:"mecp2_in_fos", 1:"total_mecp2"}, inplace = True)
mecp2_df["percent_mecp2"] = fos_df["mecp2_in_fos"]/fos_df["total_mecp2"]*100

o_merg = pd.concat([fos_df, mecp2_df], axis=1)

o_merg.to_csv(out_path)


















    