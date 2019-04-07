# -*- coding: UTF-8 -*- #
# Author: Zander_M
# Time: April, 03, 2019
# Title: Controller
#This file contains the major functions for the app.

from flask import session
import models as M 

def loginAuth(username, password):
    """
    Test if the login is valid. If it is, go to user dashboard, if not, return
    error value.
    
    Args:
        username: username
        password: password
    
    Returns:
        retval: return value. Return true if login is valid, else false.
        error: error message.
    """
    
    pass
    
def regAuth(username, password):
    """
    Test if registration is valid. If valid, register the user, update relevant 
    info in database, if not, return error.
    
    Args:
        username: username.
        password: password.
    
    Returns:
        retval: If valid return True, else False.
        error: Error info.
    """
    csr = M.conndb()



def valid_login():

    pass

def login_user():
    pass
