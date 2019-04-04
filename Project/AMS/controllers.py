# -*- coding: UTF-8 -*- #
# Author: Zander_M
# Time: April, 03, 2019
# Title: Controller
#This file contains the major functions for the app.

from flask import session
import models as M 

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
