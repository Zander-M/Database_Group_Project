# -*- coding: UTF-8 -*- #
# Author: Zander_M
# Time: April, 03, 2019
# Title: This is a airline management system written in Flask
#This file contains the major functions of the system.

from flask import Flask, render_template, session, redirect, url_for, request
import controllers as C
import views as V
import models as M

app = Flask(__name__)

# index page
@app.route('/')
def index():
    return render_template('index.html')

# registration page
@app.route('/reg',methods=['GET','POST'])
def reg():
    if request.method == 'POST':
        return 
    elif request.method == 'GET':
        return render_template('register.html')
    else:
        return "How on earth did you get here?!"

def regAuth():
    pass

# login page
@app.route('/login', methods = ['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if C.valid_login(
            request.form['username'],
            request.form['password']
        ):
            return C.login_user(request.form['username'])
        else:
            error = 'Invalid Username/Password'
    return render_template('login.html', error = error)

#logout function
@app.route('/logout')
def logout():
    pass

@app.route('/test')
def test():
    return "Hello"

if __name__ == "__main__":
    app.run()