import pandas as pd
import sys
import os
import numpy as np
from sklearn import linear_model
from datetime import date
import pickle
import matplotlib
import glob
import io
import base64

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

import seaborn as sns





year = sys.argv[1:2][0].split("_")[1]

criteria=[]
for item in sys.argv[2:]:
    criteria.append(item.split("_"))

print(year)
path='dataFiles/struct_pop/models/'
concat=""



for item in criteria:
    concat+=item[0]+"*"
    

modelFiles=glob.glob(path+'model_*{0}.pkl'.format(concat))




populationCols=["Population / H","Population / F","Nombre de ménage","Couple sans enfants ","Couple avec enfants","Ménage d'une seule personne","Famille monoparentales"]
np.set_printoptions(threshold=np.nan)
# Load from file in directory => "../dataFiles/struct_pop/models/
for idx,val in enumerate(modelFiles):
    with open(val, 'rb') as file:  
        reg_model = pickle.load(file)

        parameters=[int(x[1]) for x in criteria]
        
        parameters=np.array([parameters])
        
            
        print([populationCols[idx],[round(val,2) for val in reg_model.predict(np.array(parameters))]])
           
