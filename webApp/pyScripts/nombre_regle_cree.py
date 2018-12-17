import pandas as pd
import sys
import os
import numpy as np
from sklearn import linear_model
from datetime import date
import pickle




# Load from file in directory => "../dataFiles/struct_pop/models/
regle_filename = "dataFiles/struct_pop/models/regle.txt"
listRegle=[]
with open(regle_filename, 'r') as file:  
    for val in file.readlines():
        line=val.rstrip().split(";")

        listRegle.append('-avec-'.join(line[1:]))
            
listRegle=list(set(listRegle))
print(listRegle)
