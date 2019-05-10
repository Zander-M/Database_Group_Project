# -*- coding: UTF-8 -*- #
# Author: Zander_M
# Time: May, 09, 2019
# Title: Utils Blueprint
"""
    This file stores the functions that can be used without login
"""

import pymysql
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from AMS.db import get_db, get_cursor

bp = Blueprint('utils',__name__)

@bp.route('/', methods=["GET", "POST"])
def index():
    """
    Index page for the site. Users can search flights 
    
    Args:
        None.
    
    Returns:
        Index Page.
    """
    go_flights = 'e'  # assume search result is empty at first
    back_flights = 'e' 
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT name FROM airport")
    dept_airport = arrv_airport = cursor.fetchall()
    # cursor.execute("SELECT distinct dept_airport from flight")
    # dept_airport = cursor.fetchall()
    # cursor.execute("SELECT distinct arrv_airport from flight")
    # arrv_airport = cursor.fetchall()
    if request.method == "POST": # from search form submit

        f_dept_airport = request.form['dept_airport'] # search form names
        f_dept_time = request.form['dept_time']
        f_arrv_airport= request.form['arrv_airport']
        cursor.execute("SELECT * from `flight` WHERE dept_airport= %s AND arrv_airport = %s and DATE(dept_time) = %s",(f_dept_airport, f_arrv_airport,f_dept_time))     
        flights = cursor.fetchall() # all the planes that matches the result
        if flights is not None:
            go_flights = []
            for flight in flights:
                flight = list(flight)
                base_price = flight[3]
                # find out how many tickets are sold
                cursor.execute("SELECT * FROM ticket WHERE flight_id = %s", flight[0])
                ticket_sold = len(cursor.fetchall())
                # find out how many seats are available
                cursor.execute("SELECT seat FROM airplane where airplane_id = %s",(flight[2]))
                seat = cursor.fetchone()[0]
                if ticket_sold == seat:
                    price = 'Sold Out'
                elif ticket_sold / seat >= 0.7:
                    price = int(base_price * 1.2)  # when 70% of tickets are sold, raise the price
                else:
                    price = base_price
                flight = [flight[1], flight[5], flight[6], price, flight[0]] # airline, dept_time, arrv_time, price, flight_id
                go_flights.append(flight)
        # if comming back
        if request.form['trip'] == 'twoway':
            f_back_time = request.form['back_time']
            cursor.execute("SELECT * from `flight` WHERE dept_airport= %s AND arrv_airport = %s and DATE(dept_time) = %s",(f_arrv_airport, f_dept_airport,f_back_time))     
            b_flights = cursor.fetchall() # all the planes that matches the result
            if b_flights is not None:
                back_flights = []
                for b_flight in b_flights:
                    b_flight = list(b_flight)
                    base_price = b_flight[3]
                    # find out how many tickets are sold
                    cursor.execute("SELECT * FROM ticket WHERE flight_id = %s", b_flight[0])
                    ticket_sold = len(cursor.fetchall())
                    # find out how many seats are available
                    cursor.execute("SELECT seat FROM airplane where airplane_id = %s",(b_flight[2]))
                    seat = cursor.fetchone()[0]
                    if ticket_sold == seat:
                        price = 'Sold Out'
                    elif ticket_sold / seat >= 0.7:
                        price = int(base_price * 1.2)  # when 70% of tickets are sold, raise the price
                    else:
                        price = base_price
                    b_flight = [b_flight[1], b_flight[5], b_flight[6], price, b_flight[0]] # airline, dept_time, arrv_time, price, flight_id
                    back_flights.append(b_flight)
    return render_template('index.html', dept_airport = dept_airport, arrv_airport = arrv_airport, result= go_flights, back = back_flights)