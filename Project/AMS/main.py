# -*- coding: UTF-8 -*- #
# Author: Zander_M
# Time: April, 03, 2019
# Title: This is a airline management system written in Flask
'''
    This file contains the main logic of the app. It routes the user to different
    pages and renders the views for different pages. Database related functions 
    are in the models.py, Controlling related functions are in the controllers.py.
'''

from flask import Flask, render_template, session, redirect, url_for, request
import uuid # use uuid.uuid3() as a unique session id
import controllers as C
app = Flask(__name__)

# Pages

# index page
@app.route('/')
def index():
    """ This function direct to the index page, which contains the basic searching
    box and basic dashboard.
    
    Args:
        None.    

    Returns:
        Rendered index page.
    """

    return render_template('index.html')

# registration page
@app.route('/reg',methods=['GET','POST'])
def reg():
    """ 
    Registration Page. If requested by GET method, return the register page,
    if requested by POST method, check if the registration info is valid, and
    perform registration.
    
    Args:
        None.
    
    Returns:
    Rendered page if registration unsuccessful, redirect to login page if
    registered Successfully.
    """
    
    error = None # error info
    if request.method == 'POST':
        retval, error = C.regAuth(
            request.form['username'],
            request.form['password']
        )
        if retval:
            redirect("/login")
    return render_template('register.html', error = error)

# login page
@app.route('/login', methods = ['GET','POST'])
def login():
    """
    Login page. If request method is POST, test if the login infomation is
    correct. Redirect to personal front page if succeeded. Else return error info.
    
    Args:
        None.
    
    Returns:
        None.
    
    """
    
    error = None # error info
    if request.method == 'POST':
        retval, error = C.loginAuth(
            request.form['username'],
            request.form['password']
        )
        if retval:
            C.loginUser(request.form['username'])
            redirect('/dashboard')
    return render_template('login.html', error = error)

#logout function
@app.route('/logout')
def logout():
    """
    Log out current user. Redirect to index page.
    
    Args:
        None.
    
    Returns:
        None.
    """
    
    pass

@app.route('/dashboard')
def dashboard():
    """
    User dashboard page. User can perform different actions based on different
     roles in the system.
    
    Args:
        None.    
    Returns:
        None.
    """
    
    pass

# 
# Error page
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html',error = error), 404
    
@app.route('/test')
def test():
    return "Hello"

if __name__ == "__main__":
    app.run()