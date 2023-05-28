'''
The file is used to create a plottable version of cells_raw or cells_filtered
arrays for visulizations purposes to be used with clearmap's plotting interface
'''

#import numpy as np
#
##detected_cells_path = "" #raw or filtered
#
##plottable_cells_path = "" #sink where we save the file
#
##shape = []
#
#def create_plottable_cells(detected_cells_path, plottable_cells_path, shape):
#    detected_cells = np.load(detected_cells_path)
#    plottable_cells = np.zeros((shape[0], shape[1], shape[2]))
#    
#    for line in detected_cells:
#        x = line[0]
#        y = line[1]
#        z = line[2]
#        plottable_cells[x][y][z] = 1.
#    
#    np.save(plottable_cells_path, plottable_cells)


import numpy as np

#detected_cells_path = "/media/georgelab/Rett1/Lieselot_Collab/R1/cells_raw.npy"

#plottable_cells_path = "/media/georgelab/Rett1/Lieselot_Collab/R1/plot_cells.npy"

#raw = np.load(detected_cells_path)

#shape = [2160, 2560, 1973]

def create_plottable_cells(detected_cells_path, plottable_cells_path, shape):
    detected_cells = np.load(detected_cells_path)
    plottable_cells = np.zeros((shape[0], shape[1], shape[2]), dtype = np.uint8)
    
    i = 0
    for line in detected_cells:
        if(i % 500 == 0):
            print("on the line", i)
        x = line[0]
        y = line[1]
        z = line[2]
        plottable_cells[x][y][z] = 1
        i += 1
    
    np.save(plottable_cells_path, plottable_cells)


#create_plottable_cells(detected_cells_path, plottable_cells_path, shape)


#%%
def create_plottable_cells2(detected_cells, plottable_cells_path, shape):    
    plottable_cells = np.zeros((shape[0], shape[1], shape[2]), dtype = np.uint8)    
    i = 0
    for line in detected_cells:
        if(i % 300 == 0):
            print("on the line", i)
        x = line[0]
        y = line[1]
        z = line[2]
        plottable_cells[(x, y, z)] = 1
        i += 1   
    np.save(plottable_cells_path, plottable_cells)
    #return plottable_cells

#%%
    
def create_plottable_cells3(cells, shape):    
    plottable_cells = np.zeros((shape[0], shape[1], shape[2]), dtype = np.uint8)    
    i = 0
    for line in cells:
        if(i % 10000 == 0):
            print("on the line", i)
        x = line[0]
        y = line[1]
        z = line[2]
        plottable_cells[(x, y, z)] = 1
        i += 1   
    #np.save(plottable_cells_path, plottable_cells)
    return plottable_cells









