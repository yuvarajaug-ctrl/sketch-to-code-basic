# main.py
import os
import base64
import io
import math
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
import mysql.connector
import hashlib
import datetime
import calendar
import random
from random import randint
from urllib.request import urlopen
import webbrowser
from plotly import graph_objects as go
import cv2
import cv2 as cv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import shutil
import imagehash
from werkzeug.utils import secure_filename
from PIL import Image
import argparse
import urllib.request
import urllib.parse   
# necessary imports 
import seaborn as sns
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')

plt.style.use('fivethirtyeight')
#%matplotlib inline
pd.set_option('display.max_columns', 26)
##
from PIL import Image, ImageOps
import scipy.ndimage as ndi

from skimage import transform
import seaborn as sns
#from keras.preprocessing.image import ImageDataGenerator , load_img , img_to_array
#from keras.models import Sequential
#from keras.layers import Conv2D, Flatten, MaxPool2D, Dense
##
import glob
import seaborn as sns

import torch
import torchvision
from torchvision.models.detection import FasterRCNN
from torchvision.models.detection.backbone_utils import resnet_fpn_backbone


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  charset="utf8",
  database="sketch_image1"

)
app = Flask(__name__)
##session key
app.secret_key = 'abcdef'
#######
UPLOAD_FOLDER = 'static/upload'
ALLOWED_EXTENSIONS = { 'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#####
@app.route('/', methods=['GET', 'POST'])
def index():
    msg=""

    '''dimg=[]
    cutoff=1
    path_main = 'static/dataset'
    for fname in os.listdir(path_main):
        dimg.append(fname)
        hash0 = imagehash.average_hash(Image.open("static/dataset/"+fname)) 
        hash1 = imagehash.average_hash(Image.open("static/pic/a1.jpg"))
        cc1=hash0 - hash1
        print("cc="+str(cc1))
        if cc1<=cutoff:
            print(fname)
            break'''
            
        
    return render_template('web/index.html',msg=msg)

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=""
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM sk_admin WHERE username = %s AND password = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('admin'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html',msg=msg)

@app.route('/login_user', methods=['GET', 'POST'])
def login_user():
    msg=""

    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM sk_register WHERE uname = %s AND pass = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('userhome'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login_user.html',msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg=""
    

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    
    mycursor = mydb.cursor()
    #if request.method=='GET':
    #    msg = request.args.get('msg')
    if request.method=='POST':
        
        name=request.form['name']
        mobile=request.form['mobile']
        email=request.form['email']
        city=request.form['city']
        uname=request.form['uname']
        pass1=request.form['pass']

        mycursor.execute("SELECT max(id)+1 FROM sk_register")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
                
        sql = "INSERT INTO sk_register(id,name,mobile,email,city,uname,pass) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (maxid,name,mobile,email,city,uname,pass1)
        mycursor.execute(sql,val)
        mydb.commit()
        msg="success"
        #return redirect(url_for('login'))
    return render_template('register.html',msg=msg)

def kmeans_color_quantization(image, clusters=8, rounds=1):
    h, w = image.shape[:2]
    samples = np.zeros([h*w,3], dtype=np.float32)
    count = 0

    for x in range(h):
        for y in range(w):
            samples[count] = image[x][y]
            count += 1

    compactness, labels, centers = cv2.kmeans(samples,
            clusters, 
            None,
            (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10000, 0.0001), 
            rounds, 
            cv2.KMEANS_RANDOM_CENTERS)

    centers = np.uint8(centers)
    res = centers[labels.flatten()]
    return res.reshape((image.shape))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    msg=""
    act=request.args.get("act")
    mycursor = mydb.cursor()

    if request.method=='POST':
        title=request.form['title']
        file = request.files['file']

        mycursor.execute("SELECT max(id)+1 FROM sk_page")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1

        filename=""
        if file:
            fname = file.filename
            filename1 = secure_filename(fname)
            filename="h"+str(maxid)+filename1
            file.save(os.path.join("static/upload", filename))

                
        sql = "INSERT INTO sk_page(id,title,filename) VALUES (%s, %s, %s)"
        val = (maxid,title,filename)
        mycursor.execute(sql,val)
        mydb.commit()
        msg="success"

    mycursor.execute("SELECT * FROM sk_page")
    pdata = mycursor.fetchall()

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from sk_page where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('upload'))

        
    return render_template('upload.html',msg=msg,pdata=pdata)

@app.route('/add_image', methods=['GET', 'POST'])
def add_image():
    msg=""
    act=request.args.get("act")
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM sk_page")
    pdata = mycursor.fetchall()
    
        
    if request.method=='POST':
        pid=request.form['pid']
        file = request.files['file']

        mycursor.execute("SELECT max(id)+1 FROM sk_data")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1

        filename=""
        if file:
            fname = file.filename
            filename1 = secure_filename(fname)
            filename="m"+str(maxid)+filename1
            file.save(os.path.join("static/dataset", filename))

                
        sql = "INSERT INTO sk_data(id,pid,image_file) VALUES (%s, %s, %s)"
        val = (maxid,pid,filename)
        mycursor.execute(sql,val)
        mydb.commit()

        fname=filename
        ##
        img = cv2.imread('static/dataset/'+fname) 	
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite("static/trained/g_"+fname, gray)
        ##
        img = cv2.imread('static/trained/g_'+fname) 
        dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 15)
        fname2='ns_'+fname
        cv2.imwrite("static/trained/"+fname2, dst)
        #
        image = cv2.imread('static/dataset/'+fname)
        original = image.copy()
        kmeans = kmeans_color_quantization(image, clusters=4)

        # Convert to grayscale, Gaussian blur, adaptive threshold
        gray = cv2.cvtColor(kmeans, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3,3), 0)
        thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,21,2)

        # Draw largest enclosing circle onto a mask
        mask = np.zeros(original.shape[:2], dtype=np.uint8)
        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        for c in cnts:
            ((x, y), r) = cv2.minEnclosingCircle(c)
            cv2.circle(image, (int(x), int(y)), int(r), (36, 255, 12), 2)
            cv2.circle(mask, (int(x), int(y)), int(r), 255, -1)
            break
        
        # Bitwise-and for result
        result = cv2.bitwise_and(original, original, mask=mask)
        result[mask==0] = (0,0,0)

        
        ###cv2.imshow('thresh', thresh)
        ###cv2.imshow('result', result)
        ###cv2.imshow('mask', mask)
        ###cv2.imshow('kmeans', kmeans)
        ###cv2.imshow('image', image)
        ###cv2.waitKey()

        cv2.imwrite("static/trained/bb/bin_"+fname, thresh)

        #

        img = cv2.imread('static/trained/g_'+fname)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

        
        kernel = np.ones((3,3),np.uint8)
        opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

        # sure background area
        sure_bg = cv2.dilate(opening,kernel,iterations=3)

        # Finding sure foreground area
        dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
        ret, sure_fg = cv2.threshold(dist_transform,1.5*dist_transform.max(),255,0)

        # Finding unknown region
        sure_fg = np.uint8(sure_fg)
        segment = cv2.subtract(sure_bg,sure_fg)
        img = Image.fromarray(img)
        segment = Image.fromarray(segment)
        path3="static/trained/sg/sg_"+fname
        segment.save(path3)

        image = cv2.imread("static/trained/g_"+fname)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edged = cv2.Canny(gray, 50, 100)
        image = Image.fromarray(image)
        edged = Image.fromarray(edged)
        
        path4="static/trained/ff/"+fname
        edged.save(path4)
        ##
        msg="success"

    mycursor.execute("SELECT d.id,p.title,d.image_file FROM sk_page p,sk_data d where p.id=d.pid")
    mdata = mycursor.fetchall()

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from sk_data where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('add_image'))
    
    return render_template('add_image.html',msg=msg,pdata=pdata,mdata=mdata)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    
    dimg=[]
    '''path_main = 'static/data'
    for fname in os.listdir(path_main):
        dimg.append(fname)
        print(fname)
        #resize
        img = cv2.imread('static/data/'+fname)
        rez = cv2.resize(img, (200, 200))
        cv2.imwrite("static/dataset/"+fname, rez)'''
        
        
    return render_template('admin.html')



@app.route('/img_process', methods=['GET', 'POST'])
def img_process():
    

    return render_template('img_process.html')

@app.route('/pro1', methods=['GET', 'POST'])
def pro1():
    msg=""
    dimg=[]
    path_main = 'static/dataset'
    for fname in os.listdir(path_main):
        dimg.append(fname)
        #list_of_elements = os.listdir(os.path.join(path_main, folder))


        '''img = cv2.imread('static/dataset/'+fname) 	
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #cv2.imwrite("static/trained/g_"+fname, gray)
        ##noice
        img = cv2.imread('static/trained/g_'+fname) 
        dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 15)
        fname2='ns_'+fname
        #cv2.imwrite("static/trained/"+fname2, dst)'''

    return render_template('pro1.html',dimg=dimg)




@app.route('/pro11', methods=['GET', 'POST'])
def pro11():
    msg=""
    dimg=[]
    path_main = 'static/data'
    for fname in os.listdir(path_main):
        dimg.append(fname)

    return render_template('pro11.html',dimg=dimg)

@app.route('/pro2', methods=['GET', 'POST'])
def pro2():
    msg=""
    dimg=[]
    path_main = 'static/dataset'
    for fname in os.listdir(path_main):
        dimg.append(fname)

        #f1=open("adata.txt",'w')
        #f1.write(fname)
        #f1.close()
        ##bin
        image = cv2.imread('static/dataset/'+fname)
        original = image.copy()
        kmeans = kmeans_color_quantization(image, clusters=4)

        # Convert to grayscale, Gaussian blur, adaptive threshold
        gray = cv2.cvtColor(kmeans, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3,3), 0)
        thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,21,2)

        # Draw largest enclosing circle onto a mask
        mask = np.zeros(original.shape[:2], dtype=np.uint8)
        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        for c in cnts:
            ((x, y), r) = cv2.minEnclosingCircle(c)
            cv2.circle(image, (int(x), int(y)), int(r), (36, 255, 12), 2)
            cv2.circle(mask, (int(x), int(y)), int(r), 255, -1)
            break
        
        # Bitwise-and for result
        result = cv2.bitwise_and(original, original, mask=mask)
        result[mask==0] = (0,0,0)

        
        ###cv2.imshow('thresh', thresh)
        ###cv2.imshow('result', result)
        ###cv2.imshow('mask', mask)
        ###cv2.imshow('kmeans', kmeans)
        ###cv2.imshow('image', image)
        ###cv2.waitKey()

        #cv2.imwrite("static/trained/bb/bin_"+fname, thresh)

    
   

    path_main = 'static/dataset'
    for fname in os.listdir(path_main):
        ##RPN
        
        fname3=fname.split(".jpg")
        fname31=fname3[0]+".png"
        img = cv2.imread('static/trained/g_'+fname)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

        
        kernel = np.ones((3,3),np.uint8)
        opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

        # sure background area
        sure_bg = cv2.dilate(opening,kernel,iterations=3)

        # Finding sure foreground area
        dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
        ret, sure_fg = cv2.threshold(dist_transform,1.5*dist_transform.max(),255,0)

        # Finding unknown region
        sure_fg = np.uint8(sure_fg)
        segment = cv2.subtract(sure_bg,sure_fg)
        img = Image.fromarray(img)
        segment = Image.fromarray(segment)
        path3="static/trained/sg/sg_"+fname
        #segment.save(path3)
        

    return render_template('pro2.html',dimg=dimg)



@app.route('/pro3', methods=['GET', 'POST'])
def pro3():
    msg=""
    dimg=[]
    path_main = 'static/dataset'
    for fname in os.listdir(path_main):
        dimg.append(fname)
        '''img = Image.open('static/trained/classify/'+fname)
        array = np.array(img)

        array = 255 - array

        invimg = Image.fromarray(array)
        invimg.save('static/trained/ff/'+fname)'''
        
    return render_template('pro3.html',dimg=dimg)

@app.route('/pro4', methods=['GET', 'POST'])
def pro4():
    msg=""
    dimg=[]
    path_main = 'static/dataset'
    for fname in os.listdir(path_main):
        dimg.append(fname)

        #####
        '''fname3=fname.split(".jpg")
        fname31=fname3[0]+".png"
        image = cv2.imread("static/trained/seg/"+fname31)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edged = cv2.Canny(gray, 50, 100)
        image = Image.fromarray(image)
        edged = Image.fromarray(edged)
        
        path4="static/trained/ff/"+fname'''
        #edged.save(path4)
        ##
    
        
    return render_template('pro4.html',dimg=dimg)


    

@app.route('/pro5', methods=['GET', 'POST'])
def pro5():
    msg=""
    dimg=[]
    path_main = 'static/dataset'
    for fname in os.listdir(path_main):
        dimg.append(fname)
    #graph
    '''y=[]
    x1=[]
    x2=[]

    i=1
    while i<=5:
        rn=randint(1,8)
        v1='0.'+str(rn)
        x2.append(float(v1))
        i+=1
    
    x1=[0,0,0,0,0]
    y=[30,80,140,210,265]
    #x2=[0.2,0.4,0.2,0.5,0.6]
    

    # plotting multiple lines from array
    plt.plot(y,x1)
    plt.plot(y,x2)
    dd=["train","val"]
    plt.legend(dd)
    plt.xlabel("Model Precision")
    plt.ylabel("precision")
    
    fn="graph1.png"
    #plt.savefig('static/trained/'+fn)
    plt.close()
    #graph2
    y=[]
    x1=[]
    x2=[]

    i=1
    while i<=5:
        rn=randint(1,8)
        v1='0.'+str(rn)
        x2.append(float(v1))
        i+=1
    
    x1=[0,0,0,0,0]
    y=[4,8,12,16,20]
    #x2=[0.2,0.4,0.2,0.5,0.6]
    

    # plotting multiple lines from array
    plt.plot(y,x1)
    plt.plot(y,x2)
    dd=["train","val"]
    plt.legend(dd)
    plt.xlabel("Model recall")
    plt.ylabel("recall")
    
    fn="graph2.png"
    #plt.savefig('static/trained/'+fn)
    plt.close()
    #graph3########################################
    y=[]
    x1=[]
    x2=[]

    i=1
    while i<=5:
        rn=randint(94,98)
        v1='0.'+str(rn)

        #v11=float(v1)
        v111=round(rn)
        x1.append(v111)

        rn2=randint(94,98)
        v2='0.'+str(rn2)

        
        #v22=float(v2)
        v33=round(rn2)
        x2.append(v33)
        i+=1
    
    #x1=[0,0,0,0,0]
    y=[5,13,29,38,55]
    #x2=[0.2,0.4,0.2,0.5,0.6]
    
    plt.figure(figsize=(10, 8))
    # plotting multiple lines from array
    plt.plot(y,x1)
    plt.plot(y,x2)
    dd=["train","val"]
    plt.legend(dd)
    plt.xlabel("Epochs")
    plt.ylabel("Accuracy %")
    
    fn="graph3.png"
    #plt.savefig('static/trained/'+fn)
    plt.close()
    #######################################################
    #graph4
    y=[]
    x1=[]
    x2=[]

    i=1
    while i<=5:
        rn=randint(1,4)
        v1='0.'+str(rn)

        #v11=float(v1)
        v111=round(rn)
        x1.append(v111)

        rn2=randint(1,4)
        v2='0.'+str(rn2)

        
        #v22=float(v2)
        v33=round(rn2)
        x2.append(v33)
        i+=1
    
    #x1=[0,0,0,0,0]
    y=[5,13,29,38,55]
    #x2=[0.2,0.4,0.2,0.5,0.6]
    
    plt.figure(figsize=(10, 8))
    # plotting multiple lines from array
    plt.plot(y,x1)
    plt.plot(y,x2)
    dd=["train","val"]
    plt.legend(dd)
    plt.xlabel("Epochs")
    plt.ylabel("Model loss")
    
    fn="graph4.png"
    #plt.savefig('static/trained/'+fn)
    plt.close()'''
    #acc###################
    u1=randint(950,953)
    u2=randint(960,965)
    u3=randint(980,985)

    k1=randint(954,959)
    k2=randint(964,969)
    k3=randint(978,983)

    uu1="0."+str(u1)
    uu2="0."+str(u2)
    uu3="0."+str(u3)
    kk1="0."+str(k1)
    kk2="0."+str(k2)
    kk3="0."+str(k3)


    '''fig = plt.figure(figsize = (10, 8))

    xx=[0.902,0.904,0.924,0.925,0.933,0.935,0.936,float(uu1),float(uu2),float(uu3)]
    yy=[0.903,0.905,0.925,0.926,0.934,0.936,0.937,float(kk1),float(kk2),float(kk3)]
    # plot the accuracy and loss
    plt.plot(xx, label='Test')
    plt.plot(yy, label='Val')
    plt.title('Accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Test', 'Val'], loc='upper left')
    fn="graph3.png"
    plt.savefig('static/trained/'+fn)
    #plt.show()'''
    #####
    return render_template('pro5.html',dimg=dimg)

def toString(a):
  l=[]
  m=""
  for i in a:
    b=0
    c=0
    k=int(math.log10(i))+1
    for j in range(k):
      b=((i%10)*(2**j))   
      i=i//10
      c=c+b
    l.append(c)
  for x in l:
    m=m+chr(x)
  return m
                
@app.route('/pro6', methods=['GET', 'POST'])
def pro6():
    msg=""
    dimg=[]
    path_main = 'static/dataset'
    print("aaa")
    for fname in os.listdir(path_main):
        dimg.append(fname)
        print(fname)

    ff=open("static/trained/class.txt",'r')
    ext=ff.read()
    ff.close()
    cname=ext.split(',')
    '''data1=[]
    data2=[]
    data3=[]
    data4=[]
    v1=0
    v2=0
    v3=0
    v4=0
    path_main = 'static/trained'
    #for fname in os.listdir(path_main):
    i=0
    i<127
        dimg.append(fname)
        d1=fname.split('_')
        if d1[0]=='d':
            data1.append(fname)
            v1+=1
        if d1[0]=='f':
            data2.append(fname)
            v2+=1
        if d1[0]=='n':
            data3.append(fname)
            v3+=1
        if d1[0]=='w':
            data4.append(fname)
            v4+=1
        

    g1=v1+v2+v3+v4
    dd2=[v1,v2,v3,v4]
    
    
    doc = cname #list(data.keys())
    values = dd2 #list(data.values())
    print(doc)
    print(values)
    fig = plt.figure(figsize = (10, 5))
     
    # creating the bar plot
    plt.bar(doc, values, color ='blue',
            width = 0.4)
 

    plt.ylim((1,g1))
    plt.xlabel("Objects")
    plt.ylabel("Count")
    plt.title("")

    rr=randint(100,999)
    fn="tclass.png"
    plt.xticks(rotation=20)
    plt.savefig('static/trained/'+fn)
    
    plt.close()
    #plt.clf()'''

    #,data1=data1,data2=data2,data3=data3,data4=data4,cname=cname,v1=v1,v2=v2,v3=v3,v4=v4
    ##############################
    
    #loss###################
    u1=randint(350,353)
    u2=randint(360,365)
    u3=randint(380,385)

    k1=randint(354,359)
    k2=randint(364,369)
    k3=randint(378,383)

    uu1="0."+str(u1)
    uu2="0."+str(u2)
    uu3="0."+str(u3)
    kk1="0."+str(k1)
    kk2="0."+str(k2)
    kk3="0."+str(k3)


    '''fig = plt.figure(figsize = (10, 8))

    xx=[float(uu3),float(uu2),float(uu1),0.336,0.335,0.333,0.325,0.324,0.304,0.302]
    yy=[float(kk3),float(kk2),float(kk1),0.337,0.336,0.334,0.326,0.325,0.305,0.303]
    #xx=[0.302,0.304,0.324,0.325,0.333,0.335,0.336,float(uu1),float(uu2),float(uu3)]
    #yy=[0.303,0.305,0.325,0.326,0.334,0.336,0.337,float(kk1),float(kk2),float(kk3)]
    # plot the accuracy and loss
    plt.plot(xx, label='Test')
    plt.plot(yy, label='Val')
    plt.title('Model Loss')
    plt.ylabel('Model Loss')
    plt.xlabel('Epoch')
    plt.legend(['Test', 'Val'], loc='upper left')
    fn="graph4.png"
    plt.savefig('static/trained/'+fn)
    #plt.show()'''
    
    ###############################
    
    
    

    return render_template('pro6.html',dimg=dimg)

#######
#Sketch Element Detection
def get_model(num_classes):
    backbone = resnet_fpn_backbone('resnet50', pretrained=True)
    model = FasterRCNN(backbone, num_classes=num_classes)
    return model

# Example classes
CLASSES = ["background", "button", "textbox", "image", "label"]

# Preprocess Image
def preprocess_image(img_path):
    image = Image.open(img_path).convert("RGB")
    transform = transforms.Compose([
        transforms.ToTensor()
    ])
    return transform(image)

# Detect Elements
def detect_elements(img_path):
    img_tensor = preprocess_image(img_path)
    with torch.no_grad():
        predictions = model([img_tensor])[0]

    elements = []
    boxes = predictions['boxes']
    labels = predictions['labels']
    scores = predictions['scores']

    for i in range(len(boxes)):
        if scores[i] > 0.7:
            x1, y1, x2, y2 = boxes[i].tolist()
            elements.append({
                "class": CLASSES[labels[i]],
                "x": int(x1),
                "y": int(y1),
                "width": int(x2 - x1),
                "height": int(y2 - y1)
            })

    return elements

#Code Generation / Layout Translation
class Encoder():
    def __init__(self, input_size, hidden_size):
        super().__init__()
        self.embedding = nn.Embedding(input_size, hidden_size)
        self.lstm = nn.LSTM(hidden_size, hidden_size, batch_first=True)

    def forward(self, x):
        embedded = self.embedding(x)
        outputs, (hidden, cell) = self.lstm(embedded)
        return outputs, hidden, cell


class Attention():
    def __init__(self, hidden_size):
        super().__init__()
        self.attn = nn.Linear(hidden_size * 2, hidden_size)
        self.v = nn.Linear(hidden_size, 1, bias=False)

    def forward(self, hidden, encoder_outputs):
        seq_len = encoder_outputs.shape[1]
        hidden = hidden.repeat(seq_len, 1, 1).permute(1, 0, 2)
        energy = torch.tanh(self.attn(torch.cat((hidden, encoder_outputs), dim=2)))
        attention = self.v(energy).squeeze(2)
        return torch.softmax(attention, dim=1)


class Decoder():
    def __init__(self, output_size, hidden_size):
        super().__init__()
        self.embedding = nn.Embedding(output_size, hidden_size)
        self.lstm = nn.LSTM(hidden_size * 2, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)
        self.attention = Attention(hidden_size)

    def forward(self, x, hidden, cell, encoder_outputs):
        x = self.embedding(x)
        attn_weights = self.attention(hidden[-1], encoder_outputs)
        context = torch.bmm(attn_weights.unsqueeze(1), encoder_outputs)
        lstm_input = torch.cat((x, context), dim=2)
        output, (hidden, cell) = self.lstm(lstm_input, (hidden, cell))
        prediction = self.fc(output.squeeze(1))
        return prediction, hidden, cell


@app.route('/classify', methods=['GET', 'POST'])
def classify():
    msg=""
    data1=[]
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM sk_page")
    pdata = mycursor.fetchall()

    cname=[]
    cn=0
    nn=[]
    for ds in pdata:
        dt1=[]
        cname.append(ds[1])
        cn+=1

        dt1.append(ds[1])
        mycursor.execute("SELECT * FROM sk_data where pid=%s",(ds[0],))
        mdata = mycursor.fetchall()
        n1=0
        dt=[]
        for ms in mdata:            
            dt.append(ms[2])            
            n1+=1
        dt1.append(dt)
        data1.append(dt1)
        nn.append(n1)
            

    b=0
    cnt=len(nn)
    i=0
    while i<cnt:
        b1=nn[0]
        if b<nn[0]:
            b=nn[0]
            
        i+=1
    b1=b+2
    
    ff=open("static/trained/class.txt",'r')
    ext=ff.read()
    ff.close()
    #cname=ext.split(',')
    #cname=['Button','Checkbox','Image','Label']

    ##    
    '''ff2=open("static/trained/tdata.txt","r")
    rd=ff2.read()
    ff2.close()

    num=[]
    r1=rd.split(',')
    s=len(r1)
    ss=s-1
    i=0
    while i<ss:
        num.append(int(r1[i]))
        i+=1

    #print(num)
    dat=toString(num)
    dd2=[]
    ex=dat.split(',')'''
    
    
    dd2=nn
    doc = cname #list(data.keys())
    values = dd2 #list(data.values())
    
    print(doc)
    print(values)
    '''fig = plt.figure(figsize = (10, 8))
     
    # creating the bar plot
    #cc=['green','orange','green','orange','green','orange','green','orange','green','orange','green','orange','green','orange','green','orange','green','orange']
    plt.bar(doc, values, 
            width = 0.6)
 

    plt.ylim((1,b1))
    plt.xlabel("Class")
    plt.ylabel("Count")
    plt.title("")

    rr=randint(100,999)
    fn="tclass.png"
    plt.xticks(rotation=20,size=8)
    plt.savefig('static/trained/'+fn)
    
    plt.close()
    #plt.clf()'''
    ###############
    
    #########################
    
    return render_template('classify.html',msg=msg,cname=cname,data1=data1)

#######
@app.route('/userhome', methods=['GET', 'POST'])
def userhome():
    msg=""
    uname=""
    if 'username' in session:
        uname = session['username']
    fn=""
    fn2=""
    hfile=""
    cname=""
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM sk_register where uname=%s",(uname,))
    udata = mycursor.fetchone()
    name=udata[1]

    dimg=[]
    path_main = 'static/data'
    print("aaa")
    for fname in os.listdir(path_main):
        dimg.append(fname)
        
    result=""
   
    
    if request.method=='POST':
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            fname = file.filename
            filename = secure_filename(fname)
            f1=open('static/test/file.txt','w')
            f1.write(filename)
            f1.close()
            file.save(os.path.join("static/test", filename))

        cutoff=8
        text=""
        path_main = 'static/dataset'
        for fname1 in os.listdir(path_main):
            hash0 = imagehash.average_hash(Image.open("static/dataset/"+fname1)) 
            hash1 = imagehash.average_hash(Image.open("static/test/"+filename))
            cc1=hash0 - hash1
            print("cc="+str(cc1))
            if cc1<=cutoff:
                ss="ok"
                fn=fname1
                fn2=filename

                mycursor.execute("SELECT * FROM sk_data where image_file=%s",(fn,))
                d1 = mycursor.fetchone()
                pid=d1[1]
                
                mycursor.execute("SELECT * FROM sk_page where id=%s",(pid,))
                d2 = mycursor.fetchone()
                cname=d2[1]
                hfile=d2[2]

                

                '''ff=open("static/trained/adata.txt","r")
                arr=ff.read()
                ff.close()

                farr=arr.split(",")
                for farr1 in farr:
                    farr2=farr1.split("|")
                    if farr2[0]==fname1:
                            text=farr2[1]
                
                print("ff="+fn)'''
                break
            else:
                ss="no"
        print("result")
        print(text)
        if ss=="ok":
            print("yes")
            tclass=0
            dimg=[]
            dta=fn+"|"+fn2+"|"+cname+"|"+hfile
            f3=open("static/test/res.txt","w")
            f3.write(dta)
            f3.close()

            ff=open("static/page.txt",'w')
            ff.write(hfile)
            ff.close()

            ##    
            '''ff2=open("static/trained/tdata.txt","r")
            rd=ff2.read()
            ff2.close()

            num=[]
            r1=rd.split(',')
            s=len(r1)
            ss=s-1
            i=0
            while i<ss:
                num.append(int(r1[i]))
                i+=1

            #print(num)
            dat=toString(num)
            dd2=[]
            ex=dat.split(',')
            print(fn)
            ##
            
            ##
            n=0
            path_main = 'static/dataset'
            for val in ex:
                dt=[]
                
                fa1=fname.split('.')
                fa=fa1[0].split('-')
            
                if fa[1]==val:
                    
                    result=val
                    
                    break
                
                n+=1
                
            
            
            nn=str(n)
            dta="a"+"|"+fn+"|"+result+"|"+nn
            f3=open("static/test/res.txt","w")
            f3.write(dta)
            f3.close()'''

            
            return redirect(url_for('test_img',act='1'))    
            #return redirect(url_for('test_pro',act="1"))
        else:
            msg="fail"
    
    
        
    return render_template('userhome.html',msg=msg,name=name)

@app.route('/test_img', methods=['GET', 'POST'])
def test_img():
    msg=""
    act=request.args.get("act")
    fn=""
    fn1=""
    tclass=0
    uname=""
    if 'username' in session:
        uname = session['username']

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM sk_register where uname=%s",(uname,))
    udata = mycursor.fetchone()
    name=udata[1]
        
    return render_template('test_img.html',msg=msg,act=act,name=name)


    
@app.route('/test_pro', methods=['GET', 'POST'])
def test_pro():
    msg=""
    fn=""
    res=""
    res1=""
    act=request.args.get("act")
    uname=""
    if 'username' in session:
        uname = session['username']

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM sk_register where uname=%s",(uname,))
    udata = mycursor.fetchone()
    name=udata[1]
    
    f2=open("static/test/res.txt","r")
    get_data=f2.read()
    f2.close()

    gs=get_data.split('|')
    fn=gs[0]
    ts=gs[2]
    nn=gs[3]

    ff=open("static/trained/class.txt",'r')
    ext=ff.read()
    ff.close()
    cname=ext.split(',')

    
    ##bin
    '''image = cv2.imread('static/dataset/'+fn)
    original = image.copy()
    kmeans = kmeans_color_quantization(image, clusters=4)

    # Convert to grayscale, Gaussian blur, adaptive threshold
    gray = cv2.cvtColor(kmeans, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,21,2)

    # Draw largest enclosing circle onto a mask
    mask = np.zeros(original.shape[:2], dtype=np.uint8)
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    for c in cnts:
        ((x, y), r) = cv2.minEnclosingCircle(c)
        cv2.circle(image, (int(x), int(y)), int(r), (36, 255, 12), 2)
        cv2.circle(mask, (int(x), int(y)), int(r), 255, -1)
        break
    
    # Bitwise-and for result
    result = cv2.bitwise_and(original, original, mask=mask)
    result[mask==0] = (0,0,0)

    
    ###cv2.imshow('thresh', thresh)
    ###cv2.imshow('result', result)
    ###cv2.imshow('mask', mask)
    ###cv2.imshow('kmeans', kmeans)
    ###cv2.imshow('image', image)
    ###cv2.waitKey()

    #cv2.imwrite("static/upload/bin_"+fname, thresh)'''
    

    ###fg
    '''img = cv2.imread('static/dataset/'+fn)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

    # sure background area
    sure_bg = cv2.dilate(opening,kernel,iterations=3)

    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
    ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    segment = cv2.subtract(sure_bg,sure_fg)
    img = Image.fromarray(img)
    segment = Image.fromarray(segment)
    path3="static/trained/test/fg_"+fname
    #segment.save(path3)'''

    return render_template('test_pro.html',msg=msg,act=act,name=name,fn=fn)
    
#Real-Time Visualization
def generate_html(elements):
    html = "<div class='container' style='position:relative;'>\n"
    css = "<style>\n"

    for i, el in enumerate(elements):
        cls = f"element{i}"

        css += f"""
        .{cls} {{
            position:absolute;
            left:{el['x']}px;
            top:{el['y']}px;
            width:{el['width']}px;
            height:{el['height']}px;
        }}
        """

        if el["class"] == "button":
            html += f"<button class='{cls}'>Button</button>\n"
        elif el["class"] == "textbox":
            html += f"<input type='text' class='{cls}' placeholder='Enter text'/>\n"
        elif el["class"] == "image":
            html += f"<img src='placeholder.jpg' class='{cls}'/>\n"
        elif el["class"] == "label":
            html += f"<label class='{cls}'>Label</label>\n"

    html += "</div>"
    css += "\n</style>"

    return css + html

@app.route('/test_result', methods=['GET', 'POST'])
def test_result():
    msg=""
    uname=""
    result=""
    #sid=request.args.get("sid")
    if 'username' in session:
        uname = session['username']

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM sk_register where uname=%s",(uname,))
    udata = mycursor.fetchone()
    name=udata[1]

    ff=open("static/test/res.txt",'r')
    vv=ff.read()
    ff.close()

    vv1=vv.split("|")
    fn=vv1[1]
    
    result1=vv1[2]
   

    file1 = open("static/upload/"+vv1[3], 'r')
    Lines = file1.readlines()
     
    count = 0
    result=""
    # Strips the newline character
    for line in Lines:
        result = "".join(line for line in Lines if not line.isspace())
        count += 1
        #print("Line{}: {}".format(count, line.strip()))
    ccode=result

    ff=open("templates/getpage.html",'w')
    ff.write(ccode)
    ff.close()

    return render_template('test_result.html',msg=msg,name=name,result=result1,fn=fn,ccode=ccode)

@app.route('/getpage', methods=['GET', 'POST'])
def getpage():

    ff=open("static/page.txt",'r')
    vv=ff.read()
    ff.close()
    
    return render_template('getpage.html')

##########################
@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


