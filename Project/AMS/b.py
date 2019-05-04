# -*- coding: UTF-8 -*- #
# Author: Zander_M
# Time: April, 25, 2019
# Title: Authentication File

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for 
)

from AMS.db import get_db, get_cursor

bp = Blueprint('b',__name__, url_prefix="/b")

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
        elif g.role != 'b':
            return render_template('role_err.html')
        return view(**kwargs)
    return wrapped_view

@bp.route('/')
@login_required
def index():
    """
    Return Booking Agent index page.
    
    Args:
        None
    
    Returns:
        Booking Agent index page
    """
    
    return render_template('b/index_b.html')

@bp.route('/flights')
@login_required
def flights():
    """
    View all the flights the agent purchased representing a customer.

    Args:
        None
    
    Returns:
        Booking Agent index page
    """
    
    return render_template('b/flights.html')

@bp.route('/search')
@login_required
def search():
    """
    Search future flights    

    Args:
        None
    
    Returns:
        Booking Agent index page
    """
    
    return render_template('b/search.html')

@bp.route('/commission')
@login_required
def commission():
    """
     View total amount of commission received in the past 30 days and the average commission he/she received per ticket booked in the past 30 days and total number of tickets sold by him in the past 30 days. Specifing time range is also allowed.
    
    Args:
        None
    
    Returns:
        Booking Agent commission page
    """
    
    return render_template('b/commission.html')

@bp.route('/customer')
@login_required
def customer():
    """
    Show top 5 customer based on tickets purchased in last 6 months, and top 5 customer based on commissions received last year.    
    Args:
        None
    
    Returns:
        Booking Agent index page
    """
    
    return render_template('b/customer.html')