
from tokenize import group
from flask import Flask, render_template, request, redirect, url_for, session
from user.models import user_functions

from hashlib import sha256




def home():
    return render_template('home.html')


def signin():
    return render_template('login.html')


def signup():
    
    if request.method=='POST':
        print("u"*55)
        email=request.form['Email']
        name=request.form['Name']
        age=request.form['Age']
        gender=request.form['Gender']
        phone=request.form['Phone']
        group=request.form['Group']
        district=request.form['District']
        panchayath=request.form['Panchayath']
        ward=request.form['Ward']
        houseNo=request.form['House Number']
        password=request.form['Pwd']
        rpassword=request.form['Rpwd']
        

        encode=lambda arg1: sha256(arg1.encode('utf-8')).hexdigest()
        arg=district+panchayath+ward
        

        user_obj={
        "_id":encode(email),
        "email":email,
        "name":name,
        "age":age,
        "gender":gender,
        "phone":phone,
        "group":group,
        "district":district,
        "panchayath":panchayath,
        "ward":ward,
        "houseno":houseNo,
        "password":password,
        "member_id":encode(arg),
        }



        status=user_functions(user_obj)

        if (status):
            return render_template('home.html')
        else:
            return render_template('signup.html')

    else:
        
        return render_template('signup.html')

def admin():
    return render_template()

