# -*- coding: UTF-8 -*- #
# Author: Zander_M
# Time: April, 25, 2019
# Title: Customer Blueprint 

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from AMS.db import get_db

bp = Blueprint('c',__name__,url_prefix='/c')

@bp.route('/')
def index():
    """
    Return Airline Staff index page.
    
    Args:
        None
    
    Returns:
        Customer index page
    """
    
    return render_template('index_c.html')


#TODO: a login required function is needed for the page (check g.role)