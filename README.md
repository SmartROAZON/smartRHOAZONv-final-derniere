## smartRHOAZONv-final-derniere

#### Ceci est pour une version de Python 3.7

Ce projet est un version portable d'un environnement virtuel c'est à dire, pour lancer le projet vous aller avoir besoin de virtualenv, qui peut être installer avec la commande :
```
pip install virtualenv

```
Ensuite mettez vous à la racine du projet (repository), et lancer la commande :
```
Scripts\activate
```

Ensuite, Installer les différentes dépendances qui se trouve dans le dossier "dependencies", grace au fichier requirment.txt 
qui se trouve un fichier à l'intérieur :
```
pip install -r dependencies/requirement.txt
```
Après, entre dans le dossier webApp

```
cd webApp 
```
Et ensuite :
```diff
-  vous devez absolument être dans le dossier webApp pour lancer app.py, python webApp/app.py ne marchera pas !
```
```
python app.py
```
Ensuite lancer votre navigateur et connecter vous à l'adresse :
* http://127.0.0.1:5000/

### Bonus (risque de ne pas marcher):
Pour une version windows x86, vous pouvez essayer d'installer directement les dependances dans le dossier des wheels (dependencies/wheelsdependencies) avec la commande :
```
for %x in (dir dependencies/wheelsdependencies/*.whl) do python -m pip install %x
```
