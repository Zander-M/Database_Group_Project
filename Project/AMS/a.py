# -*- coding: UTF-8 -*- #
# Author: Zander_M
# Time: April, 25, 2019
# Title: Airline Staff Blueprint 

import functools
import pymysql

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from AMS.db import get_db, get_cursor
import datetime


# import AMS.auth as auth # import authentication functions

role = 'a'  # declare current role

bp = Blueprint('a', __name__, url_prefix="/a")


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
        cursor.execute('SELECT dept_airport, arrv_airport, DATE_FORMAT(dept_time, "%%Y %%M %%D %%T"), DATE_FORMAT(dept_time, "%%Y %%M %%D %%T"), flight_status, base_price, flight_id FROM flight WHERE airline = %s AND DATE(dept_time) BETWEEN DATE(%s) AND DATE(%s)',
                       (g.user[5], start_date, end_date))
        flights = cursor.fetchall()
        n_flights = []
        for flight in flights:
            flight = list(flight)
            if flight[4] == 0:
                flight[4] = "On Time"
            elif flight[4] == 1:
                flight[4] = "Delayed"
            n_flights.append(flight)
    else:
        # get flights in the following 30 days
        cursor.execute(
            'SELECT dept_airport, arrv_airport, DATE_FORMAT(dept_time, "%%Y %%M %%D %%T"), DATE_FORMAT(dept_time, "%%Y %%M %%D %%T"), flight_status, base_price, flight_id FROM flight WHERE airline = %s AND DATE(dept_time) BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY)', (g.user[5]))
        flights = cursor.fetchall()
        n_flights = []
        for flight in flights:
            flight = list(flight)
            if flight[4] == 0:
                flight[4] = "On Time"
            elif flight[4] == 1:
                flight[4] = "Delayed"
            n_flights.append(flight)
    return render_template('a/flights.html', flights=n_flights)


@bp.route('/flights/info/<flight_id>', methods=["GET", "POST"])
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
            cursor.execute(
                "UPDATE flight SET flight_status=%s WHERE flight_id = %s", (status, flight_id))
            db.commit()
            return redirect(url_for('a.confirm', action="Change Status"))
        except pymysql.Error as e:
            db.rollback()
            flash(e)

    cursor = get_cursor()
    cursor.execute(
        "SELECT email, name FROM customer JOIN ticket ON email = customer_email WHERE airline = %s AND flight_id = %s", (g.user[5], flight_id,))
    customers = cursor.fetchall()
    return render_template("a/flight_info.html", flight_id=flight_id, customers=customers)


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
        dept_time = request.form['dept_date'] + ' ' + request.form['dept_time']
        arrv_time = request.form['arrv_date'] + ' ' + request.form['arrv_time']
        dept_airport = request.form['dept_airport']
        arrv_airport = request.form['arrv_airport']
        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("INSERT INTO flight (airline, airplane_id, base_price, flight_status, dept_time, arrv_time, dept_airport, arrv_airport) values (%s,%s,%s,%s,%s,%s,%s,%s)",
                           (airline, airplane_id, base_price, flight_status, dept_time, arrv_time, dept_airport, arrv_airport))
            db.commit()
            return redirect(url_for('a.confirm', action="Add Flight"))
        except pymysql.Error as e:
            flash(e)
            db.rollback()

    cursor = get_cursor()
    # select all airplane of the company
    cursor.execute(
        "SELECT airplane_id FROM airplane WHERE airline = %s", (g.user[5]))
    airplanes = cursor.fetchall()
    # select all airports
    cursor.execute("SELECT name FROM airport")
    airports = cursor.fetchall()
    return render_template('a/addflights.html', airplanes=airplanes, airports=airports)


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
            cursor.execute(
                "INSERT INTO airplane (airline, seat) values (%s, %s)", (g.user[5], seat))
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
            flash(error)
        else:
            try:
                cursor.execute(
                    "INSERT INTO airport (name, city) values (%s, %s)", (name, city))
                db.commit()
                return redirect(url_for('a.confirm', action="Add airport"))
            except pymysql.Error as e:
                db.rollback()
                flash(e)
    return render_template('a/addairport.html')


@bp.route('/ba')
@login_required
def booking_agent():
    """
    Return booking agent page. Includes top 5 booking agent in terms of tickets 
    number sold/ commission received in the last year and the last 5 months, and 
    a list of all agents.
    Args:
        None

    Returns:
        Airline Staff booking agent page
    """
    cursor = get_cursor()
    # top 5 booking agent in terms of number in three months
    cursor.execute("SELECT BAID, COUNT(BAID)FROM ticket WHERE BAID IS NOT NULL AND airline = %s AND DATE(purchase_date_time) BETWEEN DATE_SUB(CURDATE(), INTERVAL 3 MONTH) AND CURDATE() GROUP BY BAID ORDER BY COUNT(BAID) DESC LIMIT 5",(g.user[5],))
    last_three_months_n = cursor.fetchall() 
    # top 5 booking agent in terms of commission fee in three month 
    cursor.execute("SELECT BAID, SUM(sold_price)*0.1 FROM ticket WHERE BAID IS NOT NULL AND airline=%s AND DATE(purchase_date_time) BETWEEN DATE_SUB(CURDATE(), INTERVAL 3 MONTH) AND CURDATE() GROUP BY BAID ORDER BY SUM(sold_price) DESC LIMIT 5",(g.user[5],))
    last_three_months_c = cursor.fetchall() 
    # top 5 booking agent in terms of number in one year 
    cursor.execute("SELECT BAID, COUNT(BAID)FROM ticket WHERE BAID IS NOT NULL AND airline = %s AND DATE(purchase_date_time) BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 YEAR) AND CURDATE() GROUP BY BAID ORDER BY COUNT(BAID) DESC LIMIT 5", (g.user[5],))
    last_year_n = cursor.fetchall() 
    # top 5 booking agent in terms of commission fee in one year
    cursor.execute("SELECT BAID, SUM(sold_price)*0.1 FROM ticket WHERE BAID IS NOT NULL AND airline = %s AND DATE(purchase_date_time) BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 YEAR) AND CURDATE() GROUP BY BAID ORDER BY SUM(sold_price) DESC LIMIT 5",(g.user[5],))
    last_year_c = cursor.fetchall() 
    cursor.execute("SELECT BAID, COUNT(BAID)FROM ticket WHERE BAID IS NOT NULL AND airline = %s GROUP BY BAID ORDER BY COUNT(BAID) DESC",(g.user[5],))
    all_agents = cursor.fetchall() 

    return render_template(
        'a/ba.html',
        last_three_months_n=last_three_months_n,
        last_three_months_c=last_three_months_c,
        last_year_n=last_year_n,
        last_year_c=last_year_c,
        all_agents=all_agents,
        )


@bp.route('/customer', methods = ["GET", "POST"])
@login_required
def customer():
    """

    Return customer page. Includes most frequent customer last year. Also, 
    Airline staff can also see all the boarding records of a customer.
    Args:
        None

    Returns:
        Airline Staff customer page
    """
    customer_info = None 
    customer_email = None
    if request.method == "POST":
        customer_email = request.form['customer_email'] 
        cursor = get_cursor()
        cursor.execute("SELECT flight.flight_id, dept_airport, dept_time, arrv_airport, arrv_time FROM flight LEFT JOIN ticket on ticket.flight_id = flight.flight_id WHERE ticket.customer_email = %s AND flight.airline = %s", (customer_email, g.user[5]))
        customer_info = cursor.fetchall()
        if not customer_info:
            customer_info = "e" # Stands for empty. Front-end will display No data
    cursor = get_cursor()
    cursor.execute("SELECT name, email, COUNT(customer_email) FROM customer RIGHT JOIN ticket on customer.email = ticket.customer_email WHERE airline = %s GROUP BY email ORDER BY COUNT(customer_email) DESC LIMIT 1", (g.user[5],))
    top_customer = cursor.fetchone()
    return render_template('a/customer.html', top_customer = top_customer, customer_info = customer_info, email = customer_email)


@bp.route('/reports', methods = ["GET", "POST"])
@login_required
def reports():
    mon_convert = {	1: 'Janauary',
		2:'February',
		3:'March',
		4:'April',
		5:'May',
		6:'June',
		7:'July',
		8:'August',
		9:'September',
		10:'October',
		11:'November',
		12:'December'}
    current_month = int(datetime.datetime.now().strftime("%m"))
    """
    Ticket info in the past month/year based on time range.    
    Args:
        None

    Returns:
        Airline Staff report page
    """
    cursor = get_cursor()
    search_result = None
    start_date = None
    end_date = None
    if request.method == "POST":
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        cursor.execute("SELECT COUNT(*) FROM ticket WHERE purchase_date_time BETWEEN %s AND %s AND airline = %s", (start_date, end_date, g.user[5]))
        search_result = cursor.fetchone()
    #fetch last one month date
    cursor.execute("SELECT name, customer_email, purchase_date_time FROM ticket LEFT JOIN customer ON ticket.customer_email = customer.email WHERE purchase_date_time BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 MONTH) AND CURDATE() AND airline = %s", (g.user[5]))
    last_month = cursor.fetchall()
    #fetch last one year date
    cursor.execute("SELECT MONTH(purchase_date_time), COUNT(*) FROM ticket WHERE purchase_date_time BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 YEAR) AND CURDATE() AND airline = %s GROUP BY MONTH(purchase_date_time) ORDER BY MONTH(purchase_date_time) ASC", (g.user[5]))
    last_year= cursor.fetchall()
    #rearrange query result of last year
    last_year_month = []
    last_year_sale = []
    for i in last_year:
        last_year_month.append(i[0])
        last_year_sale.append(i[1])
    last_year_convert = [[],[]]
    for i in range(1, 13):
        month = i + current_month
        if month > 12:
            month = month - 12
        if month in last_year_month:
            idx = last_year_month.index(month)
            last_year_convert[0].append(mon_convert[month])
            last_year_convert[1].append(last_year_sale[idx])
        else:
            last_year_convert[0].append(mon_convert[month])
            last_year_convert[1].append(0)
    return render_template('a/reports.html', last_month = last_month, last_year = last_year_convert, search_result = search_result, start_date=start_date, end_date=end_date)


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
    cursor = get_cursor()
    cursor.execute("SELECT SUM(sold_price)*0.9 FROM ticket WHERE BAID IS NOT NULL AND airline = %s AND purchase_date_time BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 MONTH) AND CURDATE()", (g.user[5]))
    indirect_sell_month = cursor.fetchone()
    cursor.execute("SELECT SUM(sold_price) FROM ticket WHERE BAID IS NULL AND airline = %s AND purchase_date_time BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 MONTH) AND CURDATE()", (g.user[5]))
    direct_sell_month = cursor.fetchone()
    cursor.execute("SELECT SUM(sold_price)*0.9 FROM ticket WHERE BAID IS NOT NULL AND airline = %s AND purchase_date_time BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 YEAR) AND CURDATE()", (g.user[5]))
    indirect_sell_year = cursor.fetchone()
    cursor.execute("SELECT SUM(sold_price) FROM ticket WHERE BAID IS NULL AND airline = %s AND purchase_date_time BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 YEAR) AND CURDATE()", (g.user[5]))
    direct_sell_year = cursor.fetchone()
    return render_template('a/revenue.html', direct_sell_month = direct_sell_month, indirect_sell_month = indirect_sell_month, direct_sell_year = direct_sell_year, indirect_sell_year = indirect_sell_year)


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
    cursor.execute(
        "SELECT arrv_airport FROM flight WHERE airline = %s AND dept_time BETWEEN DATE_SUB(CURDATE(), INTERVAL 3 MONTH) AND CURDATE() GROUP BY arrv_airport ORDER BY COUNT(arrv_airport) DESC LIMIT 3 ", (g.user[5]))
    last_three_months = cursor.fetchall()
    cursor.execute(
        "SELECT arrv_airport FROM flight WHERE flight.airline = %s AND dept_time BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 YEAR) AND CURDATE() GROUP BY arrv_airport ORDER BY COUNT(arrv_airport) DESC LIMIT 3 ", g.user[5])
    last_year = cursor.fetchall()
    return render_template('a/topdest.html', last_three_months=last_three_months, last_year=last_year)


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

    return render_template('a/confirm.html', action=action)

    @bp.route('/settings', methods=["GET", "POST"])	
@login_required	
def settings():	
    """	
    Airline Staff Settings Page. Airline staff can see his/her information, including Name, Email, Phone Number, etc. Airline Staff can also add phone numbers.	
    	
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
        cursor.execute("SELECT * FROM staff_phone WHERE phone_number = %s", (phone_number))	
        if cursor.fetchone() is not None:	
            error = "Phone number already in system"	
        if error is None:	
            try:	
                cursor.execute("INSERT INTO staff_phone (phone_number, username) values (%s, %s)", (phone_number, g.user[0]))	
                db.commit()	
            except pymysql.Error as e:	
                db.rollback()	
        flash(error)	
    username = g.user[0]	
    fname = g.user[2]	
    lname = g.user[3]	
    bday = g.user[4]	
    airline = g.user[5]	
    cursor.execute("SELECT phone_number FROM staff_phone WHERE username = %s", (g.user[0]))	
    phones = cursor.fetchall()	
    return render_template("a/settings.html", username = username, fname = fname, lname = lname, bday = bday, airline = airline, phones = phones ) 
