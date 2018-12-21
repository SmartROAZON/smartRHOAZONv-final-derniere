import os
import sys
from flask import Flask,flash, request, redirect, url_for, session
from flask import render_template
from werkzeug.utils import secure_filename
from flask_cache import Cache
import subprocess
import importlib
import json

app = Flask(__name__)

############ upload section
UPLOAD_DIRECTORY = 'dataFiles'
ALLOWED_EXTENSIONS = set(['txt', 'csv'])



################ app conf
#cache = Cache(app,config={'CACHE_TYPE': 'simple'})

app.config.update(
    ENV='development',
    TEMPLATES_AUTO_RELOAD=True,
    DEBUG=True,
    UPLOAD_FOLDER=UPLOAD_DIRECTORY
)
with app.test_request_context():
    print(url_for('static', filename='css/style.css'))
    print(url_for('static', filename='css/bootstrap.min.css'))
    print(url_for('static', filename='js/poper1.14.3.min.js'))
    print(url_for('static', filename='js/bootstrap.min.js'))
    print(url_for('static', filename='js/searchUI.js'))
    print(url_for('static', filename='js/jquery_v3.3.1.min.js'))
    print(url_for('static', filename='img/plus.png'))
    print(url_for('static', filename='img/moins.png'))
    print(url_for('static', filename='img/equal.jpg'))
    print(url_for('static', filename='img/Rennes_Métropole.png'))
    print(url_for('static', filename='img/istic.png'))
    print(url_for('static', filename='img/irisa.png'))
    print(url_for('static', filename='img/druid.png'))
    print(url_for('static', filename='img/patientez.gif'))
    print(url_for('static', filename='img/searchicon.png'))
    print(url_for('static', filename='img/fusee.png'))
    print(url_for('static', filename='img/rennes_bg.jpg'))
    
################## Affichage résultat de calcul prediction
@app.route('/getResult', methods=['POST'])
def predictionFutureResult():
    if request.method == "POST":
        data = request.get_json(force=True)
        listElements=[]
        for element in data:
            listElements.append([element,data[element]])

        for val in listElements:
            val[0]=val[0].replace(" ","--").replace("\\","--").replace("/","--")

        st=""
        for val in listElements:
            st+=" "+val[0]+"_"+val[1]
            
        print(st)    
        
        
                    
        
        command="python pyScripts/calcul_prediction.py{0}".format(st)

        res=[]
        for line in os.popen(command).readlines():
            res.append(eval(line))
        
        
        return render_template('resultCalculPrediction.html',result=res)
################## Calcul Prediction
@app.route('/criteriaForm')
def criteriaForm():
    command="python pyScripts/nombre_regle_cree.py"

    res=[]
    for line in os.popen(command).readlines():
        res.append(eval(line))

    newRes=[]
    for item in res[0]:
        newRes.append([','.join(item.split("-avec-"))])

    print(newRes)
    return render_template('criteria_specification.html',my_string=newRes)


################## calcul de la régression, et redirection vers affichage de résultat
@app.route('/calculRegle', methods=['POST'])
def calculRegle():
    if request.method == 'POST':
        #print(request.form.get('nbrDiv'))
        st=[]
        files=[]
        for i in range(1,int(request.form.get('nbrDiv'))+1):
            #print(request.form.get('crit_{0}'.format(i)))
            #print(request.form.get('file_{0}'.format(i)))
            files.append(request.form.get('file_{0}'.format(i)))
            st.append(request.form.get('file_{0}'.format(i))+"_"+request.form.get('crit_{0}'.format(i)))

        argu=""+' '.join((str(e) for e in st))
        print(argu)
        command="python pyScripts/calcul_regression.py {0}".format(argu)

        res=[]
        for line in os.popen(command).readlines():
            res.append(eval(line))

        

    #return redirect('generationRegle')
    return render_template("resultCalculRegression.html",my_string=res)
    #return redirect(url_for(resultatCalculRegression,regResult=res))



################## générateur de règle
@app.route('/generationRegle')
def generationRegle():
    res=[]
    for line in os.popen("python pyScripts/list_critere.py").readlines():
        res.append(eval(line))
        #print(eval(line))
    return render_template('generateur_regle.html', listFiles=res)

################## générer le fichier à partir des champs
@app.route('/generateFile', methods=['POST'])
def generate_file():
    if request.method == 'POST':
        #print(request.form["1"])
        col=[val.rstrip().replace(" ","_") for val in request.form.getlist("chk")]
        #print(col, type(col))
        #print(' '.join(col))
        st=""+' '.join((str(e) for e in col))
        #print(st)
        command="python pyScripts/generate_file.py {0} {1}".format(request.form["fileName"].rstrip(),st)
        res = subprocess.check_output(command.split(), shell=True)
        #print(res)
        #print(request.form["fileName"].rstrip(),type(request.form["fileName"].rstrip()))
    return redirect('fileForm')


############## controle et list de fichier de donnée
@app.route('/fileForm')
def ajoutDeFichierDonnee():
    res=[]
    #importlib.reload(os)
    #res=os.popen("python pyScripts/ajout_fichier.py").readlines()
    for line in os.popen("python pyScripts/ajout_fichier.py").readlines():
        res.append(eval(line))
        print(eval(line))
        
    
    #res=subprocess.check_call("python pyScripts/ajout_fichier.py", shell=True)
    #p = subprocess.Popen("python pyScripts/ajout_fichier.py".split(),stdout=subprocess.PIPE)
    #res, _ = p.communicate()
    #res=os.system("python pyScripts/ajout_fichier.py")
    #res=subprocess.check_output(["python", "pyScripts/ajout_fichier.py"]).decode("utf-8") 
    print("list files")
    #res=res.decode("utf-8")
    #print(res)
    return render_template('ajout_fichier.html',listFiles=res)#.encode("utf-16")
	

################# page par défaut
@app.route('/')
def home(name=None):
    return render_template('home.html', name=name)
	


#################### file upload
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/fileUpload', methods=['POST'])
def upload_file():

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(file)
            print(filename)
            #os.fsync(file.fileno())

            path=app.config['UPLOAD_FOLDER']+"/"+filename
            print(path)
            #f = open(path, "r")
            #print(f.read())


            
            #flash("uploaded {0}.".format(filename))
            #return redirect(url_for('upload_file',
            #                        filename=filename))
            #file.fsync()


    return redirect('fileForm')


#################################################
@app.route('/executeScript/<firstCrt>/<secondCrt>')
def executeScript(firstCrt,secondCrt):
	#os.system("python hello.py {0} {1}".format(firstCrt,secondCrt))
	#res=os.popen("python hello.py {0} {1}".format(firstCrt,secondCrt)).readlines()
	res=os.popen("python pyScripts/hello.py {0} {1}".format(firstCrt,secondCrt)).readlines()
	print(res)
	return render_template('results.html',my_string=res)


@app.route('/drag')
def dragANDdrop(name=None):
    return render_template('drag_n_drop.html', name=name)




if __name__ == '__main__':
    app.run(host="0.0.0.0",port="5000")
