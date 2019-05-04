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
    
    return render_template('a/index_a.html')

@bp.route('/flights')
@login_required
def flights():
    """
    Return Airline staff flights page. By default it displays the flights in 30 days. By POST query it returns the date within certain time range.

    Args:
        None
    
    Returns:
        Airline Staff flights page
    """
    
    return render_template('a/flights.html')

@bp.route('/addflights')
@login_required
def addflights():
    """
    Return add flights page. Airline staffs can add flights for their company.

    Args:
        None
    
    Returns:
        Airline Staff add flights page
    """
    
    return render_template('a/addflights.html')

@bp.route('/addplane')
@login_required
def addplane():
    """
    Return add plane page. Airline staffs can add planes for their company.

    Args:
        None
    
    Returns:
        Airline Staff add flights page
    """
    
    return render_template('a/addplane.html')

@bp.route('/addairport')
@login_required
def addairport():
    """
    Return add airport page. Airline staffs can add airports for their company.
    
    Args:
        None
    
    Returns:
        Airline Staff add airport page
    """
    
    return render_template('a/addairport.html')

@bp.route('/ba')
@login_required
def booking_agent():
    """
    Return booking agent page. Includes top 5 ticket sell in the last year and the last month
    Args:
        None
    
    Returns:
        Airline Staff booking agent page
    """
    
    return render_template('a/ba.html')

@bp.route('/customer')
@login_required
def customer():
    """
    
    Return customer page. Includes most frequent customer last year. Also, Airline staff can also see all the boarding records of a customer.
    Args:
        None
    
    Returns:
        Airline Staff customer page
    """
    
    return render_template('a/customer.html')

@bp.route('/reports')
@login_required
def reports():
    """
    Ticket info in the past month/year based on time range.    
    Args:
        None
    
    Returns:
        Airline Staff report page
    """
    
    return render_template('a/reports.html')

@bp.route('/revenue')
@login_required
def revenue():
    """
    Revenue from the last month/year from direct sell/indirect sell    
    Args:
        None
    
    Returns:
        Airline Staff revenue page
    """
    
    return render_template('a/revenue.html')

@bp.route('/topdest')
@login_required
def topdest():
    """
    Top destination    
    Args:
        None
    
    Returns:
        Airline Staff top destination page
    """
    
    return render_template('a/topdest.html')
