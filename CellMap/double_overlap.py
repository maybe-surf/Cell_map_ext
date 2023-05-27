# -*- coding: utf-8 -*-
"""
Created on Thu May 25 23:35:33 2023

@author: serge
"""
#%%
import math
import pandas as pd

#index = 9 #???????

mecp2 = pd.DataFrame([])
fos = pd.DataFrame([])


counts = {}

for cell in fos.iterrows():
    if(cell[0] % 10000 == 0):
        print("processing cell", cell[0])
    cell = cell[1]
    consider = mecp2[mecp2["name"] == cell["name"]]
    for cell2 in consider.iterrows():
        cell2 = cell2[1]
        dist = math.sqrt((cell[0]-cell2[0])**2 + (cell[1]-cell2[1])**2 + (cell[2]-cell2[2])**2)
        if(dist < 15):
            if(cell2["name"] in counts.keys()):
                counts.update({cell2["name"] : counts.get(cell2["name"])+1})
            else:
                counts.update({cell2["name"] : 1})
            break
    
        
    
    