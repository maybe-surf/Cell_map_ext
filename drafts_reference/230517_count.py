#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 12:16:48 2021

@author: georgelab
"""


#pip install wheel
#pip install pandas







import time
starttime = time.time()
import numpy as np
  
#Clearmap path
import sys 
sys.path.append('/home/georgelab/Documents/ClearMap2')
#load clearmap modules
from ClearMap.Environment import *  #analysis:ignore
  
directory = '/media/georgelab/LaCie/Lieselot_double/LC1R/C00-mecp2'  
ws = wsp.Workspace('CellMap', directory=directory);
ws.info()
ws.debug = False
resources_directory = settings.resources_path
  

import pandas as pd

os.getcwd()
os.chdir('/media/georgelab/LaCie/Lieselot_double/LC1R/C00-mecp2')
    
df = pd.read_csv ('cells.csv', error_bad_lines=False, index_col=False)
#df['region'] = df[' n'] + (' '+ df['m']).fillna(' ')
counts = df[' n'].value_counts()
counts = counts.to_frame()
counts.index.name = 'region'
counts.reset_index(inplace=True)
counts = counts.rename(columns={" n" : "LC1R"})
counts.to_csv('countsLC1R.csv', index = False)
os.chdir('/media/georgelab/LaCie/Lieselot_double/Counts')
counts.to_csv('counts_mecp2_LC1.csv', index = False)


os.getcwd()
os.chdir('/media/georgelab/LaCie/Lieselot_double/LC1R/C01-fos')
    
df = pd.read_csv ('cells.csv', error_bad_lines=False, index_col=False)
#df['region'] = df[' n'] + (' '+ df['m']).fillna(' ')
counts = df[' n'].value_counts()
counts = counts.to_frame()
counts.index.name = 'region'
counts.reset_index(inplace=True)
counts = counts.rename(columns={" n" : "LC1R"})
counts.to_csv('countsLC1R.csv', index = False)
os.chdir('/media/georgelab/LaCie/Lieselot_double/Counts')
counts.to_csv('counts_fos_LC1.csv', index = False)
