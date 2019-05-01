# -*- coding: UTF-8 -*- #
# Author: Zander_M
# Time: April, 25, 2019
# Title: Airline Staff File

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from AMS.db import get_db, get_cursor

import AMS.auth as auth # import authentication functions

role = 'a' # declare current role

bp = Blueprint('a',__name__, url_prefix="/a")

@bp.route('/')
def index():
    """
    Return Airline Staff index page.
    
    Args:
        None
    
    Returns:
        Airline Staff index page
    """
    
    return render_template('index_a.html')

#TODO: a login required function is needed for the page (check g.role)