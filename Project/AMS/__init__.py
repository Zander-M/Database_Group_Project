# -*- coding: UTF-8 -*- #
# Author: Zander_M
# Time: April, 18, 2019
# Title: Init file
'''
This file initialize most of the packages.
'''

from flask import Flask
import pymysql
# create project
app = Flask(__name__)
# read settings from setting.py
app.config.from_object('setting')
app.config.from_envvar('FLASKR_SETTINGS')

# connect database, create cursor

