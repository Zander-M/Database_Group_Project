# -*- coding: UTF-8 -*- #
# Author: Zander_M
# Time: April, 18, 2019
# Title: Init file
'''
This file initialize most of the packages.
'''

from flask import Flask
import os
import pymysql
# create project
app = Flask(__name__)
# read settings from setting.py
app.config.from_object('setting')
app.config.from_envvar('FLASKR_SETTINGS')

# connect database, create cursor

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

    # register user blueprint
    from . import user
    app.register_blueprint(user.bp)

    # register airline staff blueprint
    from . import a_s 
    app.register_blueprint(a_s.bp)

    # register booking agent blueprint
    from . import b_a
    app.register_blueprint(b_a.bp)

    return app
    
    
