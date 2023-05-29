# -*- coding: utf-8 -*-
"""
Created on Mon May 22 19:54:51 2023

@author: serge
"""

#dirs_path = "/home/georgelab/Documents/Lieselot/Sergei/Cell_map_ext/drafts_reference/double_dirs.txt"
dirs_path = "/home/georgelab/Documents/Lieselot/Sergei/Cell_map_ext/drafts_reference/double_dirs_over.txt"

dirs = {}

file = open(dirs_path)
i = 0
num = 0
for line in file:
    line = line.rstrip('\n')
    line_list = line.split("_")
    if(i % 2 == 0):
        if(len(line_list[1]) >= 4):
            if(line_list[1][3].isdigit()):
                num = int(line_list[1][2:4])
            else:
                num = int(line_list[1][2])
        else:
            num = int(line_list[1][2])
        if(num == 1):
            dirs[num] = {"dir_brain" : "/media/georgelab/LaCie/Lieselot_double/LC" + str(num) + "R"}
        else:
            dirs[num] = {"dir_brain" : "/media/georgelab/LaCie/Lieselot_double/LC" + str(num)}
        if("green" in line_list[1].lower()):
            dirs[num].update({"dir_auto" : "/" + line + "/" + line_list[2] + "_" + line_list[1] + "_UltraII_C00_xyz-Table Z<Z,4>.ome.tif"})
        else:
            dirs[num].update({"dir_mecp2" : "/" + line + "/" + line_list[2] + "_" + line_list[1] + "_UltraII_C00_xyz-Table Z<Z,4>.ome.tif"})
            dirs[num].update({"dir_foss" : "/" + line + "/" + line_list[2] + "_" + line_list[1] + "_UltraII_C01_xyz-Table Z<Z,4>.ome.tif"})
    else:
        if("green" in line_list[1].lower()):
            dirs[num].update({"dir_auto" : "/" + line + "/" + line_list[2] + "_" + line_list[1] + "_UltraII_C00_xyz-Table Z<Z,4>.ome.tif"})
        else:
            dirs[num].update({"dir_mecp2" : "/" + line + "/" + line_list[2] + "_" + line_list[1] + "_UltraII_C00_xyz-Table Z<Z,4>.ome.tif"})
            dirs[num].update({"dir_foss" : "/" + line + "/" + line_list[2] + "_" + line_list[1] + "_UltraII_C01_xyz-Table Z<Z,4>.ome.tif"})
    i += 1