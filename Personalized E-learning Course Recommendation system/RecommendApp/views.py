from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
import os
import pymysql
from django.core.files.storage import FileSystemStorage
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer #loading tfidf vector
from sklearn.metrics.pairwise import linear_kernel
from numpy import dot
from numpy.linalg import norm

global username

dataset = pd.read_csv("Dataset/Coursera.csv")
data = pd.read_csv("Dataset/Coursera.csv", usecols=['University','Difficulty Level','Course Rating'])
data = data.values
X = []
for i in range(len(data)):
    university = data[i,0].strip().lower()
    difficulty = data[i,1].strip().lower()
    ratings = str(data[i,2]).strip().lower()
    X.append(str(university)+" "+str(difficulty)+" "+str(ratings))
tfidf_vectorizer = TfidfVectorizer()
X = tfidf_vectorizer.fit_transform(X).toarray()

def GetRecommendAction(request):
    if request.method == 'POST':
        global dataset, X, tfidf_vectorizer
        university = request.POST.get('t1', False)
        difficulty = request.POST.get('t2', False)
        ratings = request.POST.get('t3', False)
        recommend = []
        query = university.strip().lower()+" "+difficulty.strip().lower()+" "+ratings.strip().lower()
        query = tfidf_vectorizer.transform([query]).toarray()
        for i in range(len(X)):
            score = dot(X[i], query[0])/(norm(X[i])*norm(query[0]))
            if score > 0:
                recommend.append([i, score])
        recommend.sort(key = lambda x : x[1], reverse=True)
        recommend = recommend[0:10]
        cols = ['Course Name', 'Description', 'Skills', 'URL']
        output = '<table border="1" align="center" width="100%"><tr>'
        font = '<font size="3" color="black">'
        for i in range(len(cols)):
            output += "<td>"+font+cols[i]+"</font></td>"
        output += "</tr>"
        for i in range(len(recommend)):
            rec = recommend[i]
            value = dataset.iloc[[rec[0]]]
            course_name = value['Course Name'].ravel()[0]
            desc = value['Course Description'].ravel()[0]
            skills = value['Skills'].ravel()[0]
            link = value['Course URL'].ravel()[0]
            output += '<tr><td>'+font+course_name+'</td>'
            output += '<td>'+font+desc+'</td>'
            output += '<td>'+font+skills+'</td>'
            output += '<td>'+font+link+'</td></tr>'
    context= {'data':output}
    return render(request, 'UserScreen.html',context)            

def GetRecommend(request):
    if request.method == 'GET':
        global dataset
        output = '<tr><td><font size="3" color="black">Choose&nbsp;University</td><td><select name="t1">'
        university = np.unique(dataset['University']).ravel()
        for i in range(len(university)):
            output += '<option value="'+university[i]+'">'+university[i]+"</option>"
        output += '</select></td></tr>'
        context= {'data1':output}
        return render(request, 'GetRecommend.html',context)

def RegisterAction(request):
    if request.method == 'POST':
        global username
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        contact = request.POST.get('t3', False)
        email = request.POST.get('t4', False)
        address = request.POST.get('t5', False)        
        
        output = "none"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'courserecommend',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username:
                    output = username+" Username already exists"
                    break                
        if output == "none":
            db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'courserecommend',charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO register VALUES('"+username+"','"+password+"','"+contact+"','"+email+"','"+address+"')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            print(db_cursor.rowcount, "Record Inserted")
            if db_cursor.rowcount == 1:
                output = "Signup process completed. Login to perform course recommendation activities"
        context= {'data':output}
        return render(request, 'Register.html', context)
        

def UserLoginAction(request):
    global username
    if request.method == 'POST':
        global username
        status = "none"
        users = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'courserecommend',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username,password FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == users and row[1] == password:
                    username = users
                    status = "success"
                    break
        if status == 'success':
            context= {'data':'Welcome '+username}
            return render(request, "UserScreen.html", context)
        else:
            context= {'data':'Invalid username'}
            return render(request, 'UserLogin.html', context)

def Register(request):
    if request.method == 'GET':        
        return render(request, 'Register.html',{})

def UserLogin(request):
    if request.method == 'GET':
       return render(request, 'UserLogin.html', {})

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

