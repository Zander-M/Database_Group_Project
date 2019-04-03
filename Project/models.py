# -*- coding: UTF-8 -*- #
# Author: Zander_M
# Time: April, 03, 2019
# Title: Database Related Functions
# This file contains the database related functions.

import pymysql

conn = pymysql.connect(
    host = 'localhost',
    port = 3306,
    user = 'root',
    password = '',
    db = 'dfp'
)