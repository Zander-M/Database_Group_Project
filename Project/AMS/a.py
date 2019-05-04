# -*- coding: UTF-8 -*- #
# Author: Zander_M
# Time: April, 25, 2019
# Title: Airline Staff File

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from AMS.db import get_db, get_cursor

# import AMS.auth as auth # import authentication functions

role = 'a' # declare current role

bp = Blueprint('a',__name__, url_prefix="/a")

def login_required(view):
    """
    For index pages for users, login is required. If not logged in, redirect to 
    login index page. Also, check if the page matches the user's role. Every page
    must first start with the 
    
    Args:
        view: View that requires login.
    
    Returns:
        wrapped_view: view that wrapped with login check.
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        
        if g.user is None:
            return redirect(url_for('auth.login_index'))
        elif g.role != 'a':
            return render_template('role_err.html')
        return view(**kwargs)

    return wrapped_view

@bp.route('/')
@login_required
def index():
    """
    Return Airline Staff index page.
    
    Args:
        None
    
    Returns:
        Airline Staff index page
    """
    
    return render_template('index_a.html')
