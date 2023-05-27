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
    if(cell[0] % 10000 == 0):
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
    
        
    
    