import numpy as np

#detected_cells_path = "" #raw or filtered

#plottable_cells_path = "" #sink where we save the file

#shape = []

#testing git_commit

def create_plottable_cells(detected_cells_path, plottable_cells_path, shape):
    detected_cells = np.load(detected_cells_path)
    plottable_cells = np.zeros((shape[0], shape[1], shape[2]))
    
    for line in detected_cells:
        x = line[0]
        y = line[1]
        z = line[2]
        plottable_cells[x][y][z] = 1.
    
    np.save(plottable_cells_path, plottable_cells)