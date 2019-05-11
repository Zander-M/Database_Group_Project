# -*- coding: UTF-8 -*- #
# Author: Zander_M
# Time: April, 25, 2019
# Title: Customer Blueprint 

import functools
from werkzeug.security import check_password_hash

import pymysql

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from AMS.db import get_db, get_cursor

bp = Blueprint('c',__name__,url_prefix='/c')

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
        elif g.role != 'c':
            return render_template('role_err.html')
        return view(**kwargs)

    return wrapped_view

@bp.route('/')
@login_required
def index():
    """
    Return Customer index page.
    
    Args:
        None
    
    Returns:
        Customer index page
    """
    
    return render_template('c/index_c.html')

@bp.route('/flights')
@login_required
def flights():
    """
    Return Customer flights.
    
    Args:
        None
    
    Returns:
        Customer flights page
    """
    cursor = get_cursor()
    cursor.execute("SELECT airline, dept_time, dept_airport, arrv_time, arrv_airport, flight_status FROM flight NATURAL JOIN ticket WHERE customer_email = %s", (g.user[0],))
    flights = list(cursor.fetchall())
    n_flights = [] # store them in a new list to change the status
    for row in flights:
        row = list(row)
        if row[-1] == 0: # 0 for on time
            row[-1] = 'On time'
        elif row[-1] == 1: # 1 for delay
            row[-1] = 'Delayed'
        n_flights.append(row)
    return render_template('c/flights.html', flights = n_flights)

@bp.route('/search', methods=["GET","POST"])
@login_required
def search():
    """
    Return Customer search flight page.
    
    Args:
        None
    
    Returns:
        Customer index page
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
    if request.method == "POST": # from search form submit

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
                    cursor.execute("SELECT seat FROM airplane where airplane_id = %s",(flight[2]))
                    seat = cursor.fetchone()[0]
                    if ticket_sold == seat:
                        price = 'Sold Out'
                    elif ticket_sold / seat >= 0.7:
                        price = int(base_price * 1.2)  # when 70% of tickets are sold, raise the price
                    else:
                        price = base_price
                    b_flight = [b_flight[1], b_flight[5], b_flight[6], price, b_flight[0]] # airline, dept_time, arrv_time, price, flight_id
                    b_n_flights.append(flight)
            else:
                b = 'e'
    return render_template('c/search.html', dept_airport = dept_airport, arrv_airport = arrv_airport, result= n_flights, back = b_n_flights)

@bp.route('/confirm_order', methods=["POST"])
@login_required
def confirm_order():
    """
    Confirm order
    
    Args:
        None
    
    Returns:
        Customer index page
    """
    db = get_db()
    cursor = db.cursor()
    # check ticket price
    
    if request.form['type'] == 'search':
        g.flight_id = request.form['flight_id']
        cursor.execute("SELECT * FROM flight WHERE flight_id = %s", (g.flight_id,))
        flight = list(cursor.fetchone())
        base_price = flight[3]
        # find out how many tickets are sold
        cursor.execute("SELECT * FROM ticket WHERE flight_id = %s", flight[0])
        ticket_sold = len(cursor.fetchall())
        # find out how many seats are available
        cursor.execute("SELECT seat FROM airplane where airplane_id = %s",(flight[2]))
        seat = cursor.fetchone()[0]
        if ticket_sold / seat >= 0.7:
            price = int(base_price * 1.2)  # when 70% of tickets are sold, raise the price
        else:
            price = base_price
            result = [flight[1], flight[7], flight[5], flight[8], flight[6], price, flight[0]]

    elif request.form['type'] == 'confirm':
        error = None
        flight_id = request.form['flight_id']
        payment = request.form['payment']
        card_number = request.form['card_number']
        name_on_card = request.form['name_on_card']
        exp_date = request.form['exp_date']
        pwd = request.form['pwd']
        cursor.execute("SELECT * FROM flight WHERE flight_id = %s", (flight_id,))
        flight = cursor.fetchone()
        base_price = flight[3]
        # find out how many tickets are sold
        cursor.execute("SELECT * FROM ticket WHERE flight_id = %s", flight[0])
        ticket_sold = len(cursor.fetchall())
        # find out how many seats are available
        cursor.execute("SELECT seat FROM airplane where airplane_id = %s",(flight[2]))
        seat = cursor.fetchone()[0]
        if ticket_sold / seat >= 0.7:
            price = int(base_price * 1.2)  # when 70% of tickets are sold, raise the price
        else:
            price = base_price
        result = [flight[1], flight[7], flight[5], flight[8], flight[6], price, flight[0]]
        if not check_password_hash(g.user[2], pwd):
            error = "Sorry, wrong password"
        if error is None:
            try:
                cursor.execute("INSERT INTO ticket (flight_id, airline, customer_email, sold_price, payment_method, card_number, name_on_card, expiration_date, purchase_date_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,CURTIME())", (flight[0], flight[1],g.user[0], price, payment, card_number, name_on_card, exp_date))
                cursor.execute("SELECT * FROM ticket WHERE flight_id = %s", flight[0])
                ticket_sold = len(cursor.fetchall())
                # find out how many seats are available
                cursor.execute("SELECT seat FROM airplane where airplane_id = %s",(flight[2]))
                seat = cursor.fetchone()[0]
                if seat < ticket_sold:
                    db.rollback()
                    error = "Sorry, the ticket sold out."
                else:
                    db.commit()
                    return redirect(url_for('c.purchase_success'))
            except pymysql.Error as e:
                error = e 
        flash(error)
    return render_template('c/confirm_order.html', result = result)

@bp.route('/purchase_success')
@login_required
def purchase_success():
    """
    Return purchase success page.
    
    Args:
        None
    
    Returns:
        Customer index page
    """
    
    return render_template('c/purchase_success.html')

@bp.route('/bill', methods=["GET", "POST"])
@login_required
def bill():
    """
    Return Past year bill.
    
    Args:
        None
    
    Returns:
        Customer index page
    """
    search_result = 'n' # n stands for not searching 
    if request.method == "POST":
        error = None
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        cursor = get_cursor()    
        cursor.execute("SELECT SUM(sold_price) from ticket where DATE(purchase_date_time) BETWEEN %s AND %s AND customer_email = %s GROUP BY customer_email", (start_date, end_date, g.user[0],))
        search_result = cursor.fetchall()
        if not search_result:
            search_result = 'e' # e stands for empty
    
    cursor = get_cursor()    
    cursor.execute("SELECT SUM(sold_price) from ticket where purchase_date_time BETWEEN DATE_SUB(NOW(), INTERVAL 1 YEAR) AND NOW() AND customer_email = %s GROUP BY customer_email", (g.user[0],))
    past_year_spent = cursor.fetchone()
    if not past_year_spent:
        past_year_spent = 'e' # e stands for empty
    past_six_month_spent = []
    for i in range(6, -1, -1):
        cursor.execute("SELECT DATE_FORMAT(purchase_date_time, '%%Y-%%m'), SUM(sold_price) from ticket where MONTH(purchase_date_time) = MONTH(NOW()) - %s AND customer_email = %s GROUP BY customer_email", (i, g.user[0],))
        past_six_month_spent.append(cursor.fetchone())
    if len(past_six_month_spent) == 0:
        past_six_month_spent = 'e' # e stands for empty
    return render_template('c/bill.html', past_year_spent = past_year_spent, past_six_month_spent = past_six_month_spent, search_result = search_result)

@bp.route('/settings', methods=["GET", "POST"])
@login_required
def settings():
    """
    Customer Settings Page. Can add phone number. 
    
    Args:
        None.
    
    Returns:
        Airline Staff settings page
    """
    db = get_db()
    cursor = db.cursor()
    error = None
    if request.method == "POST":
        phone_number = request.form["phone_number"]
        cursor.execute("SELECT * FROM customer_phone WHERE phone= %s", (phone_number))
        if cursor.fetchone() is not None:
            error = "Phone number already in system"
        if error is None:
            try:
                cursor.execute("INSERT INTO customer_phone (phone, email) values (%s, %s)", (phone_number, g.user[0]))
                db.commit()
            except pymysql.Error as e:
                db.rollback()
        flash(error)
    email = g.user[0]
    name = g.user[1]
    building_number = g.user[3]
    street = g.user[4]
    city = g.user[5]
    state = g.user[6]
    passport_number = g.user[7]
    passport_exp = g.user[8]
    passport_country = g.user[9]
    bday = g.user[10]
    cursor.execute("SELECT phone FROM customer_phone WHERE email = %s", (g.user[0]))
    phones = cursor.fetchall()
    return render_template("c/settings.html", phones = phones, email = email, name = name , building_number = building_number, street = street, city = city, state = state, passport_number = passport_number, passport_country = passport_country, passport_exp = passport_exp, bday = bday)