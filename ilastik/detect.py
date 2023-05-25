# -*- coding: utf-8 -*-
"""
Created on Fri May 12 00:16:03 2023

@author: serge
"""
#%%
import os
#import numpy as np

#trained_model_path = '/home/georgelab/Documents/Lieselot/Sergei/R1_3d_0.ilp'
#data_path = '/media/georgelab/Rett1/Lieselot_Collab/R1/ilastik/test_small.npy'
#output_path = '/media/georgelab/Rett1/Lieselot_Collab/R1/ilastik/results1.npy'

#%%
#os.system('pwd')
os.chdir('/home/georgelab/Downloads') #test it out with absolute path

os.chdir('ilastik-1.4.0-Linux')
#os.system('pwd')


#%%

command = "./run_ilastik.sh --headless --project=" + trained_model_path + " --output_format=numpy --output_filename_format=" + output_path + " --export_dtype=uint8 --export_source=\"Simple Segmentation\" --stack_along=\"t\" \"" + data_path + "\""

os.system(command)

#%%
import numpy as np
import time
import multiprocessing as mp
#import threading as th
verbose = False

#output_path = '/media/georgelab/Rett1/Lieselot_Collab/R1/ilastik/cells_detected.npy'
#stitched_path = '/media/georgelab/Rett1/Lieselot_Collab/R1/ilastik/test.npy'

stitched_path = data_path

output = np.load(output_path)
print("loaded data")
stitched = np.load(stitched_path)
print("loaded stitched")

output3d = output[:, :, :, 0]
#brain = [output3d[270*i:270*(i+1), :, :] for i in range(8)]
#brain_shape = brain.shape
#num_slices = brain_shape[2]
#cells_raw = []

print("here")

def valid(x, y, z, brain_shape):
    if(x >= 0 and x < brain_shape[0]):
        if(y >= 0 and y < brain_shape[1]):
            if(z >= 0 and z < brain_shape[2]):
                return True
    return False


def DFS2d(x, y, z, brain, brain_shape, ones):
    #base case:
    if((x, y, z) in ones):
        return
    ones.append((x, y, z))
    if(len(ones) > 20):
        return
    #recursive cases:
    if(valid(x, y+1, z, brain_shape) and brain[x, y+1, z] == 1):
        DFS2d(x, y+1, z, brain, brain_shape, ones)
    if(valid(x, y-1, z, brain_shape) and brain[x, y-1, z] == 1):
        DFS2d(x, y-1, z, brain, brain_shape, ones)
    if(valid(x+1, y, z, brain_shape) and brain[x+1, y, z] == 1):
        DFS2d(x+1, y, z, brain, brain_shape, ones)
    if(valid(x-1, y, z, brain_shape) and brain[x-1, y, z] == 1):
        DFS2d(x-1, y, z, brain, brain_shape, ones)
    return

def DFS3d(x, y, z, brain, brain_shape, ones):
    #base case:
    if((x, y, z) in ones):
        return
    ones.append((x, y, z))
    if(len(ones) > 2000):
        return
    #recursive cases:
    if(valid(x, y, z+1, brain_shape) and brain[x, y, z+1] == 1):
        DFS3d(x, y, z+1, brain, brain_shape, ones)
    if(valid(x, y+1, z, brain_shape) and brain[x, y+1, z] == 1):
        DFS3d(x, y+1, z, brain, brain_shape, ones)
    if(valid(x, y, z-1, brain_shape) and brain[x, y, z-1] == 1):
        DFS3d(x, y, z-1, brain, brain_shape, ones)
    if(valid(x, y-1, z, brain_shape) and brain[x, y-1, z] == 1):
        DFS3d(x, y-1, z, brain, brain_shape, ones)
    if(valid(x+1, y, z, brain_shape) and brain[x+1, y, z] == 1):
        DFS3d(x+1, y, z, brain, brain_shape, ones)
    if(valid(x-1, y, z, brain_shape) and brain[x-1, y, z] == 1):
        DFS3d(x-1, y, z, brain, brain_shape, ones)
    return


def fix_cell2D(ones, stitched, brain, z, shift):
    for coord in ones:
        brain[coord] = 2
    sum_x = 0
    sum_y = 0
    sum_stit = 0
    for coord in ones:
        sum_x += coord[0]
        sum_y += coord[1]
        sum_stit += stitched[coord]
    x_coord = round(sum_x/len(ones))
    y_coord = round(sum_y/len(ones))
    source = round(sum_stit/len(ones))
    size = len(ones)
    #brain[x_coord, y_coord, z_coord] = 1
    return (x_coord + shift, y_coord, z, size, source)


def fix_cell3D(ones, stitched, brain, shift):
    for coord in ones:
        brain[coord] = 2
    sum_x = 0
    sum_y = 0
    sum_z = 0
    sum_stit = 0
    for coord in ones:
        sum_x += coord[0]
        sum_y += coord[1]
        sum_z += coord[2]
        sum_stit += stitched[coord]
    x_coord = round(sum_x/len(ones))
    y_coord = round(sum_y/len(ones))
    z_coord = round(sum_z/len(ones))
    source = round(sum_stit/len(ones))
    size = len(ones)
    #brain[x_coord, y_coord, z_coord] = 1
    return (x_coord + shift, y_coord, z_coord, size, source)


def process_brain_pool(brain_slice):
    print("started")
    brain_shape = brain_slice.shape
    #num_slices = brain_shape[2]
    cells = []
    for x in range(brain_shape[0]):
        if(x % 100 == 0):
            print("processing slice with x =", x)
        for y in range(brain_shape[1]):
            for z in range(brain_shape[2]):
                if(brain_slice[x, y, z] == 1):
                    ones = []
                    if(verbose):
                        print("start")
                    DFS2d(x, y, z, brain_slice, brain_shape, ones)
                    #check the size of ones and if you need the filtering
                    if(len(ones) > 20):
                        for coord in ones:
                            brain_slice[coord] = 2
                        break
                    if(len(ones) > 1):
                        cell_info = fix_cell2D(ones, stitched, brain_slice, z)
                    else:
                        cell_info = (x, y, z, 1, stitched[x, y, z])
                    cells.append(cell_info)
                    if(verbose):
                        print("done")
    #return cells
    #cells_raw += cells
    cells_np = np.array(cells, dtype = np.uint16)
    print("done slice")
    return cells_np

def mp_brain(brain, func, cores):
    brain_sliced = np.array_split(brain, cores, axis = 0)
    if __name__ == '__main__':
        pool = mp.Pool(cores)
        cells_raw = pool.map(func, brain_sliced)
        pool.close()
        pool.join()
        return np.concatenate(cells_raw, axis = 0)
    

def process_brain(brain_slice, cells_raw):
    print("started")
    brain_shape = brain_slice.shape
    #num_slices = brain_shape[2]
    cells = []
    for x in range(brain_shape[0]):
        for y in range(brain_shape[1]):
            for z in range(brain_shape[2]):
                if(brain_slice[x, y, z] == 1):
                    ones = []
                    if(verbose):
                        print("start")
                    DFS3d(x, y, z, brain_slice, brain_shape, ones)
                    #check the size of ones and if you need the filtering
                    if(len(ones) > 1):
                        cell_info = fix_cell3D(ones, stitched, brain_slice)
                    else:
                        cell_info = (x, y, z, 1, stitched[x, y, z])
                    cells.append(cell_info)
                    if(verbose):
                        print("done")
    #return cells
    cells_raw += cells
    print("done slice")



def process_brain_mp3d(brain_slice, qq, shift): #add an extra argument for a shift and make the multiprocess
#take the tuple of brain_slice and shift as arguments in addition to the queue
    print("started process")
    brain_shape = brain_slice.shape
    #num_slices = brain_shape[2]
    cells = []
    for x in range(brain_shape[0]):
        if(x % 10 == 0):
            print("processing slice with x =", x)
        for y in range(brain_shape[1]):
            for z in range(brain_shape[2]):
                if(brain_slice[x, y, z] == 1):
                    ones = []
                    DFS3d(x, y, z, brain_slice, brain_shape, ones)
                    #check the size of ones and if you need the filtering
                    if(len(ones) > 2000):
                        for coord in ones[:-1]:
                            brain_slice[coord] = 2
                        ones = ones[-2:-1]
                        DFS3d(ones[0][0], ones[0][1], ones[0][2], brain_slice, brain_shape, ones)
                        while(len(ones) > 1):
                            for coord in ones[:-1]:
                                brain_slice[coord] = 2
                            ones = ones[-2:-1]
                            DFS3d(ones[0][0], ones[0][1], ones[0][2], brain_slice, brain_shape, ones)
                        brain_slice[ones[0]] = 2
                        break
                    if(len(ones) > 1):
                        cell_info = fix_cell3D(ones, stitched, brain_slice, shift)
                    else:
                        cell_info = (x + shift, y, z, 1, stitched[x, y, z])
                    cells.append(cell_info)
                    if(verbose):
                        print("done")
    qq.put(cells)
    print("done process")
    
def process_brain_mp2D(brain_slice, qq, shift): #add an extra argument for a shift and make the multiprocess
#take the tuple of brain_slice and shift as arguments in addition to the queue
    print("started process")
    brain_shape = brain_slice.shape
    #num_slices = brain_shape[2]
    cells = []
    for x in range(brain_shape[0]):
        if(x % 10 == 0):
            print("processing slice with x =", x)
        for y in range(brain_shape[1]):
            for z in range(brain_shape[2]):
                if(brain_slice[x, y, z] == 1):
                    ones = []
                    DFS2d(x, y, z, brain_slice, brain_shape, ones)
                    #check the size of ones and if you need the filtering
                    if(len(ones) > 20): #the following allows to avoid stack overflow and 
                        for coord in ones[:-1]:
                            brain_slice[coord] = 2
                        ones = ones[-1]
                        DFS2d(ones[0], brain, brain_shape, ones)
                        while(len(ones) > 1):
                            for coord in ones[:-1]:
                                brain_slice[coord] = 2
                            ones = ones[-1]
                            DFS2d(ones[0], brain, brain_shape, ones)
                        brain_slice[ones[0]] = 2
                        break
                    if(len(ones) > 1):
                        cell_info = fix_cell2D(ones, stitched, brain_slice, z, shift)
                    else:
                        cell_info = (x + shift, y, z, 1, stitched[x, y, z])
                    cells.append(cell_info)
    qq.put(cells)
    print("done process")



cells_raw = []
num_cores = 10
brain = np.array_split(output3d, num_cores, axis = 0)
x_slice = brain[0].shape[0]
shifts = [x_slice * i for i in range(num_cores)]

#brain = [output3d[216*i:216*(i+1), :, :] for i in range(10)]

#threads = []
#for brain_slice in brain:
#    t = th.Thread(target = process_brain_thread, args = (brain_slice, cells_raw))
#    threads.append(t)
#    t.start()
#for t in threads:
#    t.join()

#for brain_slice in brain:
#     print("slice")
#     new = process_brain(brain_slice, cells_raw)
#     print("done")
#     #cells_raw += new
#%%
start = time.time()
qq = mp.Queue()
processes = []
i = -1
for brain_slice in brain:
    i += 1
    p = mp.Process(target = process_brain_mp3d, args = (brain_slice, qq, shifts[i]))
    processes.append(p)
    p.start()

while 1:
    running = any(p.is_alive() for p in processes)
    while not qq.empty():
        cells_raw += qq.get()
    if not running:
        break


for p in processes:
    p.join()



end = time.time()
print("Total time is:", end - start)

#%%Formatting

import pandas as pd
cellsdf = pd.DataFrame(cells_raw, columns = ["x", "y", "z", "size", "source"])
cellsrec = cellsdf.to_records(index = False)
np.save(cells_raw_path, cellsrec)
                    
#%%
# def test_brain(brain):
#     for x in range(brain_shape[0]):
#         for y in range(brain_shape[1]):
#             for z in range(brain_shape[2]):
#                 if(brain[x, y, z] == 1):
#                     if(valid(x, y, z+1, num_slices) and brain[x, y, z+1] == 1):
#                         return False
#                     if(valid(x, y+1, z, num_slices) and brain[x, y+1, z] == 1):
#                         return False
#                     if(valid(x, y, z-1, num_slices) and brain[x, y, z-1] == 1):
#                         return False
#                     if(valid(x, y-1, z, num_slices) and brain[x, y-1, z] == 1):
#                         return False
#                     if(valid(x+1, y, z, num_slices) and brain[x+1, y, z] == 1):
#                         return False
#                     if(valid(x-1, y, z, num_slices) and brain[x-1, y, z] == 1):
#                         return False
#     return True

#%%
# import pandas as pd
# coords = []

# for row in cells_raw:
#     coords.append((row[0], row[1], row[2]))

# coordsDF = pd.DataFrame(coords)
# dups = coordsDF[0].duplicated()

