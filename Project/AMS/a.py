# -*- coding: UTF-8 -*- #
# Author: Zander_M
# Time: April, 25, 2019
# Title: Airline Staff File

import functools
import pymysql

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from AMS.db import get_db, get_cursor


# import AMS.auth as auth # import authentication functions

role = 'a' # declare current role

bp = Blueprint('a',__name__, url_prefix="/a")

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
        elif g.role != 'a':
            return render_template('role_err.html')
        return view(**kwargs)

    return wrapped_view

@bp.route('/')
@login_required
def index():
    """
    Return Airline Staff index page.
    
    Args:
        None
    
    Returns:
        Airline Staff index page
    """
    
    return render_template('a/index_a.html')

@bp.route('/flights', methods=["GET", "POST"])
@login_required
def flights():
    """
    Return Airline staff flights page. By default it displays the flights in 30 days. By POST query it returns the date within certain time range.

    Args:
        None
    
    Returns:
        Airline Staff flights page
    """
    cursor = get_cursor()
    if request.method == "POST":
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        cursor.execute('SELECT dept_airport, arrv_airport, DATE_FORMAT(dept_time, "%%Y %%M %%D %%T"), DATE_FORMAT(dept_time, "%%Y %%M %%D %%T"), flight_status, base_price, flight_id FROM flight WHERE airline = %s AND DATE(dept_time) BETWEEN DATE(%s) AND DATE(%s)', (g.user[5], start_date, end_date))
        flights = cursor.fetchall()
        n_flights = []
        for flight in flights:
            flight = list(flight)
            if flight[4] == 0:
                flight[4] = "On Time"
            elif flight[4] == 1:
                flight[4] = "Delay"
            n_flights.append(flight)
    else:
        # get flights in the following 30 days
        cursor.execute('SELECT dept_airport, arrv_airport, DATE_FORMAT(dept_time, "%%Y %%M %%D %%T"), DATE_FORMAT(dept_time, "%%Y %%M %%D %%T"), flight_status, base_price, flight_id FROM flight WHERE airline = %s AND DATE(dept_time) BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY)',(g.user[5]))
        flights = cursor.fetchall()
        n_flights = []
        for flight in flights:
            flight = list(flight)
            if flight[4] == 0:
                flight[4] = "On Time"
            elif flight[4] == 1:
                flight[4] = "Delay"
            n_flights.append(flight)
    return render_template('a/flights.html', flights = n_flights)

@bp.route('/flights/info/<flight_id>', methods=["GET","POST"])
@login_required
def flight_info(flight_id):
    """
    Return certain flight info. Displaying all the passengers.
    Args:
        None
    
    Returns:
        Airline Staff flights page
    """
    if request.method == "POST":
        error = None
        flight_id = request.form["flight_id"]
        status = request.form["status"]
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("UPDATE flight SET flight_status=%s WHERE flight_id = %s",(status, flight_id))
            db.commit()
            return redirect(url_for('a.confirm', action = "Change Status"))
        except pymysql.Error as e:
            db.rollback()
            flash(e)

    cursor = get_cursor()
    cursor.execute("SELECT email, name FROM customer JOIN ticket ON email = customer_email WHERE airline = %s AND flight_id = %s",(g.user[5], flight_id,))
    customers = cursor.fetchall()
    return render_template("a/flight_info.html", flight_id = flight_id, customers = customers)
 
@bp.route('/addflights', methods=["GET", "POST"])
@login_required
def addflights():
    """
    Return add flights page. Airline staffs can add flights for their company.

    Args:
        None
    
    Returns:
        Airline Staff add flights page
    """
    if request.method == "POST":
        error = None
        airline = g.user[5]
        airplane_id = request.form['airplane_id']
        base_price = request.form['base_price']
        flight_status = request.form['flight_status']
        dept_time = request.form['dept_date'] +' ' + request.form['dept_time']
        arrv_time = request.form['arrv_date'] +' ' + request.form['arrv_time']
        dept_airport = request.form['dept_airport']
        arrv_airport = request.form['arrv_airport']
        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("INSERT INTO flight (airline, airplane_id, base_price, flight_status, dept_time, arrv_time, dept_airport, arrv_airport) values (%s,%s,%s,%s,%s,%s,%s,%s)", (airline, airplane_id, base_price, flight_status, dept_time, arrv_time, dept_airport, arrv_airport))
            db.commit()
            return redirect(url_for('a.confirm', action = "Add Flight"))
        except pymysql.Error as e:
            flash(e)
            db.rollback()
        
    cursor = get_cursor()
    # select all airplane of the company
    cursor.execute("SELECT airplane_id FROM airplane WHERE airline = %s",(g.user[5]))
    airplanes = cursor.fetchall()
    # select all airports 
    cursor.execute("SELECT name FROM airport")
    airports = cursor.fetchall()
    return render_template('a/addflights.html', airplanes = airplanes, airports = airports)

@bp.route('/addplane', methods=["GET", "POST"])
@login_required
def addplane():
    """
    Return add plane page. Airline staffs can add planes for their company.

    Args:
        None
    
    Returns:
        Airline Staff add flights page
    """
    if request.method == "POST":
        seat = request.form['seat']
        db = get_db()
        cursor = get_cursor()
        try:
            cursor.execute("INSERT INTO airplane (airline, seat) values (%s, %s)", (g.user[5], seat))
            db.commit()
            return redirect(url_for('a.confirm', action="Add airplane"))
        except pymysql.Error as e:
            db.rollback()
            flash(e)
    return render_template('a/addplane.html')

@bp.route('/addairport', methods=["GET", "POST"])
@login_required
def addairport():
    """
    Return add airport page. Airline staffs can add airports for their company.
    
    Args:
        None
    
    Returns:
        Airline Staff add airport page
    """
    
    if request.method == "POST":
        error = None
        name = request.form['name']
        city = request.form['city']
        db = get_db()
        cursor = get_cursor()
        cursor.execute("SELECT * FROM airport WHERE name = %s", (name,))
        if cursor.fetchone() is not None:
            error = "The airport is already in the system" 
        try:
            cursor.execute("INSERT INTO airport (name, city) values (%s, %s)", (name, city))
            db.commit()
            return redirect(url_for('a.confirm', action = "Add airport"))
        except pymysql.Error as e:
            db.rollback()
            flash(e)
        flash(error)
    return render_template('a/addairport.html')

@bp.route('/ba')
@login_required
def booking_agent():
    """
    Return booking agent page. Includes top 5 ticket sell in the last year and the last month
    Args:
        None
    
    Returns:
        Airline Staff booking agent page
    """
    
    return render_template('a/ba.html', booking_agent = booking_agent)

@bp.route('/customer')
@login_required
def customer():
    """
    
    Return customer page. Includes most frequent customer last year. Also, Airline staff can also see all the boarding records of a customer.
    Args:
        None
    
    Returns:
        Airline Staff customer page
    """
    
    return render_template('a/customer.html')

@bp.route('/reports')
@login_required
def reports():
    """
    Ticket info in the past month/year based on time range.    
    Args:
        None
    
    Returns:
        Airline Staff report page
    """
    
    return render_template('a/reports.html')

@bp.route('/revenue')
@login_required
def revenue():
    """
    Revenue from the last month/year from direct sell/indirect sell    
    Args:
        None
    
    Returns:
        Airline Staff revenue page
    """
    
    return render_template('a/revenue.html')

@bp.route('/topdest')
@login_required
def topdest():
    """
    Top destination    
    Args:
        None
    
    Returns:
        Airline Staff top destination page
    """
    cursor = get_cursor()
    cursor.execute("SELECT * from (SELECT arrv_airport FROM flight WHERE airline = %s AND dept_time BETWEEN DATE_SUB(CURDATE(), INTERVAL 3 MONTH) AND CURDATE() GROUP BY arrv_airport ORDER BY COUNT(arrv_airport) DESC) as T LIMIT 3 ", (g.user[5]))
    last_three_months = cursor.fetchall()
    cursor.execute("SELECT * from (SELECT arrv_airport FROM flight WHERE flight.airline = %s AND dept_time BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 YEAR) AND CURDATE() GROUP BY arrv_airport ORDER BY COUNT(arrv_airport) DESC) as T LIMIT 3 ",g.user[5])
    last_year= cursor.fetchall()
    return render_template('a/topdest.html', last_three_months = last_three_months, last_year = last_year )

@bp.route('/confirm/<action>')
@login_required
def confirm(action):
    """
    Top destination    
    Args:
        None
    
    Returns:
        Airline Staff top destination page
    """
    
    return render_template('a/confirm.html', action = action)
