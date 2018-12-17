import sys
import pandas as pd
import numpy as np
from sklearn import cluster, datasets, linear_model
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection  import train_test_split

import seaborn as sns

##data_etudiant=pd.read_csv("..\data\dataSet_NbrEtudiant_sexe.csv", sep=';')
##data_etudiant["Nombre Etudiant Total"]=data_etudiant["Nombre Etudiant Femme"]+data_etudiant["Nombre Etudiant Male"]
##data_etudiant


import matplotlib.pyplot as plt, mpld3
plt.plot([3,1,4,1,5], 'ks-', mec='w', mew=5, ms=20)
##res=mpld3.show()
##fig=mpld3.fig_to_html()
##print("the script is running !")
##print(sys.argv[1])
##print(sys.argv[2])

import io
import base64

def fig_to_base64(fig):
    img = io.BytesIO()
    fig.savefig(img, format='png',
                bbox_inches='tight')
    img.seek(0)

    return base64.b64encode(img.getvalue())


data_etudiant=pd.read_csv("..\..\data\dataSet_NbrEtudiant_sexe.csv", sep=';')
data_etudiant["Nombre Etudiant Total"]=data_etudiant["Nombre Etudiant Femme"]+data_etudiant["Nombre Etudiant Male"]
data_logement=pd.read_csv("..\..\data\\NumberConstructionPerYear.csv", sep=';')
##plt.plot(data_logement['year'], data_logement['NumberConstructionPeerYear'], color='green', linewidth=3)
##plt.legend()




data_etudiant_from_2010=data_etudiant[data_etudiant["rentrée"]>2009]
dataframe=pd.concat((data_etudiant_from_2010["Nombre Etudiant Total"],data_logement["NumberConstructionPeerYear"]),axis=1,keys=["Nombre Etudiant Total","NumberConstructionPeerYear"])
dataframe["Nombre Etudiant Total"]=data_etudiant_from_2010["Nombre Etudiant Total"].reset_index(drop=True)
dataframe["NumberConstructionPeerYear"]=data_logement["NumberConstructionPeerYear"].reset_index(drop=True)
dataframe = dataframe[-np.isnan(dataframe["NumberConstructionPeerYear"])]
####### Nombre etudiant graph

fig, ax = plt.subplots()
ax.plot(data_etudiant_from_2010['rentrée'], data_etudiant_from_2010['Nombre Etudiant Total'], color='grey', linewidth=3)
ax.legend()
ax.set_title("Nombre d'étudiant par Année", fontsize=20)
ax.set_xlabel('Année',fontsize=15)
ax.set_ylabel("Nombre total d'étudiant",fontsize=15)

encoded = fig_to_base64(fig)
my_html = '<img src="data:image/png;base64, {}">'.format(encoded.decode('utf-8'))

print(my_html)
####### logement graph

fig, ax = plt.subplots()
ax.plot(data_logement['year'], data_logement['NumberConstructionPeerYear'], color='green', linewidth=3)
ax.legend()
ax.set_title("Nombre de construction par Année", fontsize=20)
ax.set_xlabel('Année',fontsize=15)
ax.set_ylabel('Nombre de construction',fontsize=15)

encoded = fig_to_base64(fig)
my_html1 = '<img src="data:image/png;base64, {}">'.format(encoded.decode('utf-8'))


############ regression lineaire
npMatrix = np.matrix(dataframe)
x , y = npMatrix[:,0], npMatrix[:,1]
model = linear_model.LinearRegression().fit(x,y)

m = model.coef_
b = model.intercept_

#print("formula : y = {0}x + {1}".format(m, b))

predicted = model.predict(np.array(x[:,0]))

######## graphics
fig, ax = plt.subplots()
ax.scatter(dataframe.iloc[:,:2],data_logement.iloc[:dataframe.size-1,:2],  color='black')
ax.scatter([x[:,0]],predicted,  color='blue')
ax.plot(np.array(x[:,0]),b+m*np.array(x[:,0]) , color='red', linewidth=3)

ax.set_title("Régression linéraire ", fontsize=20)
ax.set_xlabel('Nombre Etudiant Total',fontsize=15)
ax.set_ylabel('Nombre de construction',fontsize=15)

encoded = fig_to_base64(fig)
my_html2 = '<img src="data:image/png;base64, {}">'.format(encoded.decode('utf-8'))


print([x[:,0]],[y[:,0]])

print(dataframe.iloc[:,:])

# write-html-2-windows.py

import webbrowser

f = open('helloworld.html','w')

message = """<html>
<head></head>
<body><p>Hello World!</p>
{0}
{1}
</body>
</html>""".format(my_html1,my_html2)

f.write(message)
f.close()

webbrowser.open_new_tab('helloworld.html')







