# -*- coding: UTF-8 -*- #
# Author: Zander_M
# Time: April, 25, 2019
# Title: Booking Agent Blueprint 

import functools

import pymysql

from werkzeug.security import check_password_hash

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for 
)

from AMS.db import get_db, get_cursor

bp = Blueprint('b',__name__, url_prefix="/b")

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
        elif g.role != 'b':
            return render_template('role_err.html')
        return view(**kwargs)
    return wrapped_view

@bp.route('/')
@login_required
def index():
    """
    Return Booking Agent index page.
    
    Args:
        None
    
    Returns:
        Booking Agent index page
    """
    
    return render_template('b/index_b.html')

@bp.route('/flights')
@login_required
def flights():
    """
    View all the flights the agent purchased representing a customer.

    Args:
        None
    
    Returns:
        Booking Agent index page
    """
    cursor = get_cursor()
    cursor.execute("SELECT customer.name, customer.email, airline, dept_time, dept_airport, arrv_time, arrv_airport, flight_status FROM flight NATURAL JOIN ticket JOIN customer on customer.email = ticket.customer_email WHERE BAID = %s AND dept_time > NOW()", (g.BAID,))
    flights = list(cursor.fetchall())
    n_flights = [] # store them in a new list to change the status
    for row in flights:
        row = list(row)
        if row[-1] == 0: # 0 for on time
            row[-1] = 'On time'
        elif row[-1] == 1: # 1 for delay
            row[-1] = 'Delayed'
        n_flights.append(row)
    return render_template('b/flights.html', flights = n_flights)

@bp.route('/search', methods=["GET", "POST"])
@login_required
def search():
    """
    Search future flights    

    Args:
        None
    
    Returns:
        Booking Agent index page
    """
    n_flights = 'e' 
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT distinct dept_airport from flight")
    dept_airport = cursor.fetchall()
    cursor.execute("SELECT distinct arrv_airport from flight")
    arrv_airport = cursor.fetchall()
    b_n_flights = None
    if request.method == "POST": # from search form submit

        f_dept_airport = request.form['dept_airport'] # search form names
        f_dept_time = request.form['dept_time']

        f_arrv_airport= request.form['arrv_airport']
        cursor.execute("SELECT * from `flight` WHERE dept_airport= %s AND arrv_airport = %s and DATE(dept_time) = %s",(f_dept_airport, f_arrv_airport,f_dept_time))     
        flights = cursor.fetchall() # all the planes that matches the result
        n_flights = []
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
        # if comming back
        if request.form['trip'] == 'twoway':
            f_back_time = request.form['back_time']
            cursor.execute("SELECT * from `flight` WHERE dept_airport= %s AND arrv_airport = %s and DATE(dept_time) = %s",(f_arrv_airport, f_dept_airport,f_back_time))     
            b_flights = cursor.fetchall() # all the planes that matches the result
            b_n_flights = []
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
    return render_template('b/search.html', dept_airport = dept_airport, arrv_airport = arrv_airport, result= n_flights, back = b_n_flights)

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
        customer_email = request.form['customer_email']
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
        if not check_password_hash(g.user[1], pwd):
            error = "Sorry, wrong password"
        cursor.execute("SELECT * FROM customer WHERE email = %s", (customer_email))
        if not cursor.fetchone():
            error = "Can't find this user"
        if error is None:
            try:
                cursor.execute("INSERT INTO ticket (flight_id, airline, customer_email, sold_price, payment_method, card_number, name_on_card, expiration_date, purchase_date_time, BAID) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,CURTIME(), %s)", (flight[0], flight[1],customer_email, price, payment, card_number, name_on_card, exp_date,g.BAID))
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
                    return redirect(url_for('b.purchase_success'))
            except pymysql.Error as e:
                error = e 
        flash(error)
    return render_template('b/confirm_order.html', result = result)

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
    
    return render_template('b/purchase_success.html')

@bp.route('/commission', methods=["GET", "POST"])
@login_required
def commission():
    """
     View total amount of commission received in the past 30 days and the average commission he/she received per ticket booked in the past 30 days and total number of tickets sold by him in the past 30 days. Specifing time range is also allowed.
    
    Args:
        None
    
    Returns:
        Booking Agent commission page
    """
    cursor = get_cursor() 
    search_commission = None 
    search_cnt = None 
    if request.method == "POST":
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        cursor.execute("SELECT SUM(sold_price)*0.1 FROM ticket WHERE BAID = %s AND purchase_date_time BETWEEN %s AND %s", (g.BAID,start_date, end_date,))
        search_commission = cursor.fetchall()
        search_commission = search_commission[0]
        cursor.execute("SELECT COUNT(*) FROM ticket WHERE BAID = %s AND purchase_date_time BETWEEN %s AND %s", (g.BAID,start_date, end_date))
        search_cnt = cursor.fetchone()
    # fetch past 30 days commission
    cursor.execute("SELECT SUM(sold_price)*0.1 FROM ticket WHERE BAID = %s AND purchase_date_time BETWEEN DATE_SUB(CURDATE(), INTERVAL 30 DAY) AND NOW()", (g.BAID,))
    thirty_day_commission = cursor.fetchone()
    cursor.execute("SELECT AVG(sold_price)*0.1 FROM ticket WHERE BAID = %s AND purchase_date_time BETWEEN DATE_SUB(CURDATE(), INTERVAL 30 DAY) AND NOW()", (g.BAID,))
    thirty_day_avg = cursor.fetchone()
    cursor.execute("SELECT COUNT(*) FROM ticket WHERE BAID = %s AND purchase_date_time BETWEEN DATE_SUB(CURDATE(), INTERVAL 30 DAY) AND NOW()", (g.BAID,))
    thirty_day_cnt = cursor.fetchone()
    return render_template('b/commission.html', search_cnt = search_cnt, search_commission = search_commission, thirty_day_avg = thirty_day_avg, thirty_day_cnt = thirty_day_cnt, thirty_day_commission = thirty_day_commission)

@bp.route('/customer')
@login_required
def customer():
    """
    Show top 5 customer based on tickets purchased in last 6 months, and top 5 customer based on commissions received last year.    
    Args:
        None
    
    Returns:
        Booking Agent index page
    """
    cursor = get_cursor()
    # 6 months number
    cursor.execute("SELECT name, email, COUNT(email) FROM customer RIGHT JOIN ticket on customer.email = ticket.customer_email WHERE BAID=%s  AND purchase_date_time BETWEEN DATE_SUB(CURDATE(), INTERVAL 6 MONTH) AND NOW() GROUP BY(email) ORDER BY COUNT(email) DESC LIMIT 5 ", (g.BAID))
    six_months_cnt = cursor.fetchall()
    print(six_months_cnt)
    ticket_based = [[],[]]
    for a,b,c in six_months_cnt:
        ticket_based[0].append(a)
        ticket_based[1].append(c)
    # one year commission
    cursor.execute("SELECT name, email, SUM(sold_price)*0.1 FROM customer RIGHT JOIN ticket on customer.email = ticket.customer_email WHERE BAID = %s AND purchase_date_time BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 YEAR) AND NOW() GROUP BY(email) ORDER BY SUM(sold_price) DESC LIMIT 5 ", (g.BAID))
    one_year_commission = cursor.fetchall()
    comm_based = [[],[]]
    for a,b,c in one_year_commission:
        comm_based[0].append(a)
        comm_based[1].append(float(c))
    return render_template('b/customer.html', six_months_cnt = six_months_cnt, one_year_commission = one_year_commission, ticket_based = ticket_based, comm_based = comm_based)

@bp.route('/settings')
@login_required
def settings():
    """
    Booking Agent Settings Page. Booking Agent can see his/her information.
    
    Args:
        None.
    
    Returns:
        Booking agent settings page
    """
    return render_template("b/settings.html")
