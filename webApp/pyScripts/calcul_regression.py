import pandas as pd
import sys
import os
import numpy as np
from sklearn import linear_model
from datetime import date
import pickle
import matplotlib

import io
import base64

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

import seaborn as sns


#samples call :         python calcul_regression.py Logement_nettoye.csv_2 Logement_nettoye.csv_4 Emploi_nettoye.csv_3

#recupérer tous les arguments sous forme fichier.csv_indexColumn ou fichier.txt_indexColumn **
arguments=sys.argv[1:]
listFiles=[]

for value in arguments:
    l = value.split("_")
    fileName='_'.join(l[:-1])
    listFiles.append(fileName)

#list contenant les noms des fichiers reçus en args sans redondance sous forme fichier.csv ou fichier.txt
listFiles=list(set(listFiles))

#list qui contiendrait nos nom de fichier.csv ou fichier.txt avec les index columns regroupé, exemple comme suit :[ [ fichier.csv,[1,2] ] , [ fichier.txt,[5] ] ]
file_col=[]


for idx,val in enumerate(arguments):
    l = val.split("_")
    fileName='_'.join(l[:-1])
    if idx == 0:
        file_col.append([fileName,[l[-1]]])
    else:
        for i, value in enumerate(file_col):          
            if fileName == file_col[i][0]:
                list_to=file_col[i][1]
                list_to.append(l[-1])
                list_to.sort()
                break;
        else:
            file_col.append([fileName,[l[-1]]])


def calcul_regression_avec_temps(dataFile,usingColumn):
    ## retourne modele de l'equation sous forme y(column) = a * temps + b
    usingColumn.append(0)
    data=pd.read_csv(dataFile,sep=";",usecols=usingColumn)

    #print(data.columns[usingColumn[0]].lower())
    #if data.columns[usingColumn[0]].lower() == "année":
    #    print("continue")
    #else:
    #    print("pas de column année")
    #    exit(0)
    #data=data.reset_index()
    today = date.today()
    df = pd.DataFrame(np.array([x for x in range(today.year,today.year+21)]).reshape(-1, 1), columns=[data.columns[0]])
    for index in range(1,len(data.columns)):
        reg = linear_model.LinearRegression()
        features=data[[data.columns[0]]]
        target=data.iloc[:,index]
        reg.fit(features,target)
        #print("regression de {0}".format(dataFile))
        #print("{0}  =  {1} * {2} + {3}".format(data.columns[index],reg.coef_[0],data.columns[0],reg.intercept_))
        #avoir l'année d'aujourdhui et faire les prédictions dans 20 ans 

        
        predictions = reg.predict(np.array([x for x in range(today.year,today.year+21)]).reshape(-1, 1))
        #print(predictions)
        #print(data.columns[index])
        
        df[data.columns[index]]=predictions.astype(int)
        
        
   

        pkl_filename = "dataFiles/struct_pop/models/modelyear_{0}.pkl".format(data.columns[index].replace(" ","-").replace("/","-"))
        with open(pkl_filename, 'wb') as file:  
            pickle.dump(reg, file)

    df = pd.concat([data,df], ignore_index=True,sort=False)

    return [reg,df]



path="dataFiles/"
result=[]
for value in file_col:
    value[1] = list(map(int, value[1]))  #convert columns indexes all to int
    name=path+value[0]

    reg,df=calcul_regression_avec_temps(name,value[1])
    result.append([reg,df])
    
#result contient liste de : [ modele, dataframe Prediction dans 20 ans ]

#maintenant on faire la régression entre criteres et population

#print(result)



################ Pour la création d'image
def fig_to_base64(fig):
    img = io.BytesIO()
    fig.savefig(img, format='png',
                bbox_inches='tight')
    img.seek(0)

    return base64.b64encode(img.getvalue())


################
# size of target different de size of features (features contains predicted values also need to fix)
def calcul_regression_avec_population(populationFile,resRegAevcTemps):

    data=pd.read_csv(populationFile,sep=";")
    result=[]
    resultGlobal=[]
    fig, ax = plt.subplots(figsize=(10,5))

    figBars, axBars = plt.subplots(figsize=(10,5))

 
    features=pd.DataFrame()
    #print(resRegAevcTemps)
    for val in resRegAevcTemps:
        #print(val[1][val[1].columns[len(val[1].columns)-1]])
        #val[1] => feature dataframe
        #data_logement[[data_logement.columns[len(data_logement.columns)-1]]]
        for idx in range(1,val[1].columns.size):
            features=pd.concat([features,val[1][val[1].columns[idx]]],axis=1)
    #print(features)
    for index in range(2,len(data.columns)):
        reg = linear_model.LinearRegression()

        #features=features[[val for val in features.columns]]
        target=data.iloc[:,index]

        #print(features[:target.size])
        #print(target)

        #print(data.iloc[:,:])
        reg.fit(features[:target.size],target)
        #print(reg.coef_)

        #print(data.columns[index])
        #print([print("{0} * {1} ".format(val,features.columns[idx]), sep=' ', end='+ ', flush=True) for idx,val in enumerate(reg.coef_)])
        featureString=[]
        for idx,val in enumerate(reg.coef_):
            #print("{0} * {1} ".format(val,features.columns[idx]), sep=' ', end='+ ', flush=True)
            featureString.append(features.columns[idx])

        # Save to file in the current working directory
        columnName=data.columns[index].replace(" ","_").replace("/","-")
        #result [RegressionOfcolumnName,[columns]]

        ######## graphics
        #npMatrixFeatures = np.matrix(features)
        #npMatrixTarget = np.matrix(data.iloc[:,index])
        #for val in range(1,features.columns.size):
        #    ax.scatter(data.iloc[:,0],features.iloc[:target.size,val])
        
        #ax.scatter(data.iloc[:,0],target)
        #sns.set_context("paper")
        #sns.set_style("darkgrid", {"axes.facecolor": ".9"}) #change plot background to seaborn
        ax.plot(data.iloc[:,0],target,linewidth=4,linestyle=":")

        regEq=0
        for idx, val in enumerate(reg.coef_):
            calc=reg.coef_[idx]*features.iloc[:target.size,idx]
            regEq=regEq+calc

        regEq=regEq+reg.intercept_
        ax.plot(data.iloc[:,0],regEq,linewidth=1, color="black",marker='+')

        
        #axBars.bar(data.iloc[:,0],height=target,align='center',width=0.35)
        #axBars = data.plot.bar(rot=0)
        
        #ax.scatter([x[:,0]],predicted)
        #ax.plot(np.array(x[:,0]),b+m*np.array(x[:,0]) , color='red', linewidth=3)
        
        #result.append([["Régression_"+columnName,"model_{0}.pkl".format(columnName)],featureString])
        oneStringFeatures=""
        for val in featureString:
            oneStringFeatures+="{0}---".format(val.rstrip().replace(" ","--").replace("/","--"))
        #print("{0}".format(oneStringFeatures))
        pkl_filename = "dataFiles/struct_pop/models/model_{0}---{1}.pkl".format(columnName,oneStringFeatures)
        with open(pkl_filename, 'wb') as file:  
            pickle.dump(reg, file)

        regle_filename = "dataFiles/struct_pop/models/regle.txt"
        with open(regle_filename, 'a') as file:  
            file.write(data.columns[index])
            for val in featureString:
                file.write(";"+val)
            file.write("\n")

    ax.set_title("Donnée population avec les équations de régression", fontsize=20)
    chartBox = ax.get_position()
    ax.set_position([chartBox.x0, chartBox.y0, chartBox.width, chartBox.height])
    ax.legend(loc='upper center', bbox_to_anchor=(1.2, 0.8), shadow=True, ncol=1,scatterpoints=1)
    data.plot(kind='bar',x=data.columns[0],y=[data.columns[val] for val in range(2,data.columns.size)], rot=0,ax=axBars)


    chartsList=[]
    #### pie charts pour les années
    data_col =[data.columns[val] for val in range(2,data.columns.size)]
        
    for index, row in data.iterrows():
        fig1, ax1= plt.subplots()
        series = pd.Series(row[2:].values, index=data_col,name="")
        series.plot(kind='pie',ax=ax1,figsize=(7, 5),autopct='%1.1f%%')
        encoded = fig_to_base64(fig1)
        my_html = '<img src="data:image/png;base64, {0}" >'.format(encoded.decode('utf-8'))
        chartsList.append([row[0],my_html])

        
    #data.plot(kind='pie',x=data.columns[0],y=[data.columns[val] for val in range(1,data.columns.size)], rot=0,ax=axBars)
    #ax.set_xlabel('Nombre Etudiant Total',fontsize=15)
    #ax.set_ylabel('Nombre de construction',fontsize=15)
    
    #axBars.legend()
    encoded = fig_to_base64(fig)

    axBars.set_title("Donnée population en histograme", fontsize=20)
    chartBox = axBars.get_position()
    axBars.set_position([chartBox.x0, chartBox.y0, chartBox.width, chartBox.height])
    axBars.legend(loc='upper center', bbox_to_anchor=(1.2, 0.8), shadow=True, ncol=1)
    encodedBars = fig_to_base64(figBars)
    my_html = '<img src="data:image/png;base64, {0}" id="{1}" >'.format(encoded.decode('utf-8'),"ligne")
    my_htmlBars = '<img src="data:image/png;base64, {0}" id={1} >'.format(encodedBars.decode('utf-8'),"bar")
    #print(my_html)
    #print(my_htmlBars)
    #################
    resultGlobal.append([chartsList,my_html,my_htmlBars,featureString,result])
    return resultGlobal





print(calcul_regression_avec_population(path+"struct_pop/Population.csv",result))
#calcul_regression_avec_population(path+"struct_pop/Population.csv",result)


 
# Load from file in directory => "../dataFiles/struct_pop/models/
##directory="dataFiles/struct_pop/models/"
##for pkl_filename in os.listdir(directory):
##    with open(directory+pkl_filename, 'rb') as file:  
##        pickle_model = pickle.load(file)
##        print(pickle_model)


