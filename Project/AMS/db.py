# -*- coding: UTF-8 -*- #
# Author: Zander_M
# Time: April, 24, 2019
# Title: Database Setup
# This file initialize the connection to MySQL Database using pymysql

import pymysql
from flask import current_app, g
from flask.cli import with_appcontext
import click

def init_app(app):
    """
    Register function when app launches.
    
    Args:
        None.    
    Returns:
        None.
    """
    
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def get_db():
    """
    This function connects to database.
    
    Args:
        None   
    Returns:
        Database object.
    """

    if 'db' not in g:
        g.db = pymysql.connect(
            host="localhost", # host
            user="root", # username
            password="", # password
            db="ams" # database name
            )
    return g.db

def get_cursor():
    """
    Return the cursor of the current database.
    
    Args:
        None.
    Returns:
        pymysql cursor.
    """
    
    if 'db' not in g:
        db = get_db()
        return db.cursor()
    return g.db.cursor()
    
# create cursor

def init_db():
    """
    This function initialize the database.
    
    Args:
        None.    
    Returns:
        None.
    """
    cursor = get_cursor()
    with current_app.open_resource('static/init.sql') as f:
        cursor.execute(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    """
    Clear existing data and create new tables. Insert certain test data. Echo 'Database Initialized' if succeeded.
    
    Args:
        None.    
    Returns:
        None.
    """
    init_db()
    click.echo('Database Initialized')
    
def close_db(e=None):
    """
    Close database connection.
    
    Args:
        e: event. Default none.    
    Returns:
        None
    """
    db = g.pop('db',None)
    if db is not None:
        db.close()

    