# -*- coding: utf-8 -*-
"""
Created on Thu May 25 23:35:33 2023

@author: serge
"""

import math

index = 0 #???????
i = 0

mecp2 = []
fos = []

counts = {}

for cell in fos:
    if(i % 10000 == 0):
        print("processing cell", i)
    neighbours = {}
    for cell2 in mecp2:
        dist = math.sqrt((cell[0]-cell2[0])**2 + (cell[1]-cell2[1])**2 + (cell[2]-cell2[2])**2)
        if(dist < 15):
            neighbours[dist] = cell2
    nearest = neighbours[min(neighbours.keys())]
    if(nearest[index] in counts.keys()):
        counts.update({nearest[index] : counts.get(nearest[index])+1})
    else:
        counts.update({nearest[index] : 1})
        
    
    