# -*- coding: UTF-8 -*- #
# Author: Zander_M
# Time: April, 18, 2019
# Title: Init file
'''
This file initialize most of the packages.
'''

from flask import Flask, render_template, redirect, g, session, url_for, request
import os
import pymysql

# read settings from setting.py
# app.config.from_object('setting')
# app.config.from_envvar('FLASKR_SETTINGS')


def create_app(test_config=None):
    """
    Create and configure the app 
    
    Args:
        param: param description.
    
    Returns:
        The return value.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'AMS.sql')
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register database functions
    from . import db
    db.init_app(app)

    # register auth blueprint
    from . import auth
    app.register_blueprint(auth.bp)

    # register customer blueprint
    from . import c 
    app.register_blueprint(c.bp)

    # register airline staff blueprint
    from . import a 
    app.register_blueprint(a.bp)

    # register booking agent blueprint
    from . import b 
    app.register_blueprint(b.bp)

    from . import utils
    app.register_blueprint(utils.bp)

    app.register_error_handler(404, page_not_found)

    return app
    
def page_not_found(e):
    return render_template('404.html'), 404
    
