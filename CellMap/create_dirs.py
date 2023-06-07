# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 15:30:42 2023

@author: serge
"""

dirs = {}

file = open(set1_path)
i = 0
num = 0
for line in file:
    line = line.rstrip('\n')
    line_list = line.split("_")
    if(i % 2 == 0):
        if(line_list[1][2].isdigit()):
            num = int(line_list[1][1:3])
        else:
            num = int(line_list[1][1:2])
        dirs[num] = {"dir_brain" : "/media/georgelab/Rett1/Lieselot_Collab/R" + str(num)}
        if("red" in line_list[1].lower()):
            dirs[num].update({"dir_raw" : "/" + line + "/" + line_list[2] + "_" + line_list[1] + "_UltraII_C00_xyz-Table Z<Z,4>.ome.tif"})
        else:
            dirs[num].update({"dir_auto" : "/" + line + "/" + line_list[2] + "_" + line_list[1] + "_UltraII_C00_xyz-Table Z<Z,4>.ome.tif"})
    else:
        if("red" in line_list[1].lower()):
            dirs[num].update({"dir_raw" : "/" + line + "/" + line_list[2] + "_" + line_list[1] + "_UltraII_C00_xyz-Table Z<Z,4>.ome.tif"})
        else:
            dirs[num].update({"dir_auto" : "/" + line + "/" + line_list[2] + "_" + line_list[1] + "_UltraII_C00_xyz-Table Z<Z,4>.ome.tif"})
    i += 1

file2 = open(set2_path)
i = 0
num = 0
for line in file2:
    line = line.rstrip('\n')
    line_list = line.split("_")
    if(i % 2 == 0):
        num = int(line_list[1][1:3])
        dirs[num] = {"dir_brain" : "/media/georgelab/Rett1/Lieselot_Collab/R" + str(num)}
        if("red" in line_list[1].lower()):
            dirs[num].update({"dir_raw" : "/" + line + "/" + line_list[2] + "_" + line_list[1] + "_UltraII_C00_xyz-Table Z<Z,4>.ome.tif"})
        else:
            dirs[num].update({"dir_auto" : "/" + line + "/" + line_list[2] + "_" + line_list[1] + "_UltraII_C00_xyz-Table Z<Z,4>.ome.tif"})
    else:
        if("red" in line_list[1].lower()):
            dirs[num].update({"dir_raw" : "/" + line + "/" + line_list[2] + "_" + line_list[1] + "_UltraII_C00_xyz-Table Z<Z,4>.ome.tif"})
        else:
            dirs[num].update({"dir_auto" : "/" + line + "/" + line_list[2] + "_" + line_list[1] + "_UltraII_C00_xyz-Table Z<Z,4>.ome.tif"})
    i += 1    













    