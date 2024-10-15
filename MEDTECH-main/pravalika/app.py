from flask import Flask,render_template,request
import numpy as np
import pickle
import pandas as pd
import numpy as np
import difflib
import requests
from bs4 import BeautifulSoup
import os, io
from google.cloud import vision
from google.cloud.vision_v1 import types
from matplotlib import pyplot as plt
import requests
from bs4 import BeautifulSoup

url_def = "https://www.apollopharmacy.in/search-medicines/"
rf_clf = pickle.load(open("model2.pkl", "rb"))
df = pd.read_csv('data/clean/Training.csv')
dt=pd.read_csv('data/clean/medicines_list.csv')
pres_=pd.read_csv('data/clean/precaution998.csv')
des=pd.read_csv('data/clean/description778.csv')
X = df.iloc[:, :-1]
y = df['prognosis']
sym={}
sym_a=[]
for i,j in enumerate(X):
    sym[j]=i
    sym_a.append(j)
d1=[]
h=[]
a=[]
l=''
dt['Disease']=dt['Disease'].str.lower()

app = Flask(__name__,template_folder='Template')
@app.route('/',methods=['GET','POST'])
def main():
    return render_template('home.html')
@app.route('/login',methods=['GET','POST'])
def login():
    return render_template('login.html')
@app.route('/about',methods=['GET','POST'])
def about():
    return render_template('about.html')
@app.route('/pres',methods=['GET','POST'])
def pres():
    return render_template('prescriptionpage.html')
@app.route('/getur',methods=['GET','POST'])
def getur():
    return render_template('geturmedicine.html')
@app.route('/medic',methods=['GET','POST'])
def medi():
    return render_template('medicinedetection.html')
@app.route('/diseasepredict',methods=['GET','POST'])

def dispre():
    return render_template('diseaseprediction.html')

@app.route('/dise',methods=['GET','POST'])
def disp():
    return render_template('diseasedetect.html')
@app.route('/disease', methods=['GET','POST'])
def disprediction():
    d= request.form['ll']
    d1=list(d.split(" "))
    for i in d1:
        h.append(difflib.get_close_matches(i,sym_a,4,0.6))
    for i in h:
        if(len(i)!=0):
            a.append(i[0])
    input_vector = np.zeros(len(sym))
    for i in a:
        input_vector[[sym[i]]] = 1
    m=rf_clf.predict([input_vector])
    dt['Disease']=dt['Disease'].str.lower()
    pres_['Disease']=pres_['Disease'].str.lower()
    des['Disease']=des['Disease'].str.lower()
    k1=''
    l=''
    dis=m[0]
    for i in range(len(dt['Disease'])):
        if(dt['Disease'][i]==np.str.lower(m[0])):
            k1+=pres_['Precaution_1'][i]+' '+pres_['Precaution_2'][i]+' '+pres_['Precaution_3'][i]+' '+pres_['Precaution_4'][i]
            l+=des['Description'][i]
            die=des['Diet'][i]
            fit=des['fitness'][i]
    return render_template('diseasedetect2.html',dis=dis,k1=k1,des=l,die=die,fit=fit)
@app.route('/med2',methods=['GET','POST'])
def med2():
    return render_template('meddect1.html')


@app.route('/medicine', methods=['GET','POST'])
def medprediction():
    p1=[]
    p2=[]
    p3=[]
    k=[]
    dis=request.form['medicine']
    for i in range(len(dt['Disease'])):
        if(dt['Disease'][i]==str(dis)):
            k=list(dt['Medicines'][i].split(','))
    # p1=medinf(str(k[0]))
    # p2=medinf(str(k[1]))
    # p3=medinf(str(k[2]))
    return render_template('MEDDECT2.html',dis=dis,med1=k[0],med2=k[1],med3=k[2])


@app.route('/presz',methods=['GET','POST'])
def presz():
    return render_template('prescription1.html')

@app.route('/prescription',methods=['POST'])
def prescription():
    pres=request.form['prescription']
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'hedapi-c8de5a32fd12.json'
    client = vision.ImageAnnotatorClient()
    FILE_PATH =pres
    with io.open(FILE_PATH, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)
    docText = response.full_text_annotation.text
    return render_template('prescription2.html',txt=docText)
@app.route('/getmed1',methods=['GET','POST'])
def getmed_():
    return render_template('getmed1.html')
@app.route('/aboutmed',methods=['POST'])
def aboutmed():
    search=request.form['name']
    k=medinf(search)
    return render_template('getmed2.html',d=k[0],url=k[2],h=search)

def medinf(search):
    if " " in search:
        search = search.replace(' ','')
    url1 = url_def + search
    response1 = requests.get(url1)
    soup1 = BeautifulSoup(response1.content, "html.parser")
    links = soup1.find_all("a",class_="ProductCard_proDesMain__LWq_f")
    a=[]

    for link in links:
        if link.get("href"):
            res_links=link.get("href")
            a.append(res_links)
    b=[]
    c=[]
    k=[]
    for i in a:
        b.append(i.split('?')[0])
    #c=difflib.get_close_matches(search,b,4,0.5)
    url_def2 = "https://www.apollopharmacy.in"
    url_inp = str(b[0])

    url2 = url_def2 + url_inp
    response2 = requests.get(url2)

    # Parse the HTML content
    soup2 = BeautifulSoup(response2.content, "html.parser")


    elements = soup2.find_all(class_="PdpWeb_productDetailed__cgtqy")
    elements3 = soup2.find_all(class_="text-align-justify")
    d=[]
    for element in elements3:
        d.append(element.text)
    k.append(d[0])
    k.append(d[4])
    k.append(url2)
    return k


    
    
      
    

if __name__ == "__main__":
    app.run(debug=True)


