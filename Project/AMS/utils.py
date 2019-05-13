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
    # initialize the search result to be empty

    n_flights = 'n' # n for null
    b_n_flights = 'o' # stands for one way
    db = get_db()
    cursor = db.cursor()
    # cursor.execute("SELECT distinct dept_airport from flight")
    # dept_airport = cursor.fetchall()
    # cursor.execute("SELECT distinct arrv_airport from flight")
    cursor.execute("SELECT name FROM airport")
    dept_airport = arrv_airport = cursor.fetchall()
    cursor.execute("SELECT name FROM airline")
    airlines = cursor.fetchall()
    if request.method == "POST": # from search form submit
        if request.form['content'] == "trip":
            f_dept_airport = request.form['dept_airport'] # search form names
            f_dept_time = request.form['dept_time']

            f_arrv_airport= request.form['arrv_airport']
            cursor.execute("SELECT * from `flight` WHERE dept_airport= %s AND arrv_airport = %s and DATE(dept_time) = %s",(f_dept_airport, f_arrv_airport,f_dept_time))     
            flights = cursor.fetchall() # all the planes that matches the result
            n_flights = []
            if flights:
                for flight in flights:
                    flight = list(flight)
                    base_price = flight[3]
                    # find out how many tickets are sold
                    cursor.execute("SELECT COUNT(flight_id) FROM ticket WHERE flight_id = %s GROUP BY flight_id", flight[0])
                    ticket_sold = cursor.fetchone()[0]
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
                    n_flights.append(flight)
            else:
                n_flights = 'e' # e for empty
            # if comming back
            if request.form['trip'] == 'twoway':
                f_back_date = request.form['back_date']
                cursor.execute("SELECT * from `flight` WHERE dept_airport= %s AND arrv_airport = %s and DATE(dept_time) = %s",(f_arrv_airport, f_dept_airport,f_back_date))     
                b_flights = cursor.fetchall() # all the planes that matches the result
                b_n_flights = []
                if b_flights:
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
                        b_n_flights.append(b_flight)
                else:
                    b_n_flights = 'e'
        elif request.form['content'] == "flight":
            f_airline = request.form['airline']
            f_flight_id = request.form['flight_id']
            f_dept_date = request.form['dept_date']
            f_arrv_date = request.form['arrv_date']
            cursor.execute("SELECT * from `flight` WHERE flight_id = %s AND DATE(dept_time)= %s AND DATE(arrv_time)= %s and airline = %s",(f_flight_id, f_dept_date, f_arrv_date,f_airline))     
            flights = cursor.fetchall() # all the planes that matches the result
            n_flights = []
            if flights:
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
                    n_flights.append(flight)
    return render_template('index.html', dept_airport = dept_airport, arrv_airport = arrv_airport, result= n_flights, back = b_n_flights, airlines = airlines)
