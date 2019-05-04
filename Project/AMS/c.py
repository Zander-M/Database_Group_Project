# -*- coding: UTF-8 -*- #
# Author: Zander_M
# Time: April, 25, 2019
# Title: Customer Blueprint 

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from AMS.db import get_db, get_cursor

bp = Blueprint('c',__name__,url_prefix='/c')

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
        elif g.role != 'c':
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
        Customer index page
    """
    
    return render_template('c/index_c.html')

@bp.route('/flights')
@login_required
def flights():
    """
    Return Customer flights.
    
    Args:
        None
    
    Returns:
        Customer flights page
    """
    cursor = get_cursor()
    cursor.execute("SELECT airline, dept_time, dept_airport, arrv_time, arrv_airport, flight_status FROM flight NATURAL JOIN ticket WHERE customer_email = %s", (g.user[0],))
    flights = list(cursor.fetchall())
    for row in flights:
        row = list(row)
        if row[-1] == 0: # 0 for on time
            row[-1] = 'On time'
        elif row[-1] == 1: # 1 for delay
            row[-1] = 'Delay'
        assert row
    return render_template('c/flights.html', flights = flights)

@bp.route('/search')
@login_required
def search():
    """
    Return Customer search flight page.
    
    Args:
        None
    
    Returns:
        Customer index page
    """
    
    return render_template('c/search.html')

@bp.route('/bill')
@login_required
def bill():
    """
    Return Airline Staff index page.
    
    Args:
        None
    
    Returns:
        Customer index page
    """
    
    return render_template('c/bill.html')