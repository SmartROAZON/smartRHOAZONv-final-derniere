"# smartROAZHON" 
"# smartROAZHON.v2" 
"# smartRHOAZONv-final" 
"# smartRHOAZONv-final-derniere" 

Ceci est pour une version de Python 3.7

Ce projet est un version portable d'un environnement virtuel c'est à dire, pour lancer le projet vous aller avoir besoin de virtualenv, qui peut être installer avec la commande :
#### pip install virtualenv
Ensuite mettez vous à la racine du projet (repository), et lancer la commande :
#### Scripts\activate
Après, entre dans le dossier webApp
#### cd webApp
Et ensuite :
#### python app.py






Si cela ne suffie pas, créer votre propre environnement, et lancer l'app.py
### Pour Créer l'environnement de l'application
Commencer par :
#### pip install virtualenv
Apres :
#### Scripts\activate
Ensuite, Installer les différentes dépendances qui se trouve dans le dossier "dependencies", à l'intérieur de se dossier se trouve un fichier requirment.txt et un dossier wheels
Vous pouvez installer ces dépendances à partir des fichiers whl par la commande suivante à la racine du projet :
#### pip install -r dependencies/requirements.txt --find-links dependencies/wheelsdependencies/
sinon vous pouvez faire, mais les dépendances serait installer d'internet, risque d'incohérence de version
#### pip install -r dependencies/requirements.txt

Après, entre dans le dossier webApp une fois l'installation est finie :
#### cd webApp
Et ensuite :
#### python app.py
