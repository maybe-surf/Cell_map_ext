# -*- coding: utf-8 -*-
"""
Created on Thu May 25 23:35:33 2023

@author: serge
"""
#%%
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

#index = 9 #???????

mecp2 = pd.DataFrame([])
fos = pd.DataFrame([])


counts = {}

for cell in fos.iterrows():
    if(cell[0] % 1000 == 0):
        print("processing cell", cell[0])
    cell = cell[1]
    consider = mecp2[mecp2["name"] == cell["name"]]
    consider["dist_sq"] = (consider["x"]-cell[0])**2 + (consider["y"]-cell[1])**2 + (consider["z"]-cell[2])**2
    if(consider["dist_sq"].min() < 225):
        if(cell["name"] in counts.keys()):
            counts.update({cell["name"] : counts.get(cell["name"])+1})
        else:
            counts.update({cell["name"] : 1})
        break
    
#fos["min_dist_sq"] =        
    
#%%
import numpy as np
cells_mecp2_path = "/media/georgelab/LaCie/Lieselot_double/LC3/C00-mecp2/cells_raw.npy"
cells_fos_path = "/media/georgelab/LaCie/Lieselot_double/LC3/C01-fos/cells_raw.npy"
create_plot_path = "/home/georgelab/Documents/Lieselot/Sergei/Cell_map_ext/CellMap/create_plottable.py"

mecp2 = np.load(cells_mecp2_path)
print("loaded mecp2")
fos = np.load(cells_fos_path)
print("loaded fos")

exec(open(create_plot_path).read())

shape = [2160, 2560, 1988]
mecp2_full = create_plottable_cells3(mecp2, shape)
print("created plottable")

xy_margin = 4 #16 micron
z_margin = 5 #15 micron

overlap = 0

i = 0
for cell in fos:
    if(i % 1000):
        print("on the cell", i)
    i += 1
    consider = mecp2_full[(cell[0]-xy_margin):(cell[0]+xy_margin), (cell[1]-xy_margin):(cell[1]+xy_margin), (cell[2]-z_margin):(cell[2]+z_margin)]
    if(sum(sum(sum(consider))) > 0):
        overlap += 1




























    