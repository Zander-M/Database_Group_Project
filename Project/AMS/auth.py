# -*- coding: UTF-8 -*- #
# Author: Zander_M
# Time: April, 25, 2019
# Title: Authentications

'''
    This file contains all the functions related to account management, such as register, login, logout, change password, etc.
'''

import functools
import uuid
import pymysql

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from AMS.db import get_db, get_cursor

bp = Blueprint('auth', __name__, url_prefix="/auth")


@bp.route('/')
def auth_index():
    """
    Authentication index page. User can register, login, logout from this page

    Args:
        param: param description.

    Returns:
        The return value.
    """

    return render_template('auth_index.html')


@bp.route('/register/')
def reg_index():
    """
    Return Registration index page.

    Args:
        None.
    Returns:
        Registration index page
    """

    return render_template('reg_index.html')


@bp.route('/register/<role>', methods=('GET', 'POST'))
def register(role):
    """
    Register in the system. Based on different roles in the system, return
    different register page.

    Args:
        role: Role of the user. Default is user.

    Returns:
        If requested by get, return rendered register page.
        If requested by post, redirect to reg_confirm page if registered successfully,
        else return error msg.
    """
    error = None
    db = get_db()
    cursor = db.cursor()
    # from register form submit, verify if register is successful.
    if request.method == "POST":
        # by default, Booking Agent ID is some random content.
        BAID = 'success'

        # Airline Staff Register
        if role == 'a':  # a for Airline Staff
            username = request.form['username']
            password = request.form['password']
            password_c = request.form['password_c']
            fname = request.form['fname']  # first name
            lname = request.form['lname']  # last name
            bday = request.form['bday']  # birthday
            airline = request.form['airline']  # airline name
            phone = request.form['phone']
            # query database to check if the username is used
            cursor.execute(
                "SELECT * from `staff` WHERE `username` = %s", (username,))
            if not username:
                error = 'Username is required'
            elif not password:
                error = 'Password is required'
            elif password != password_c:
                error = 'Passwords do not match.'
            elif not fname:
                error = 'First name is required'
            elif not lname:
                error = 'Last name is required'
            elif not bday:
                error = 'Date of birth is required'
            elif not phone:
                error = "Phone number is required"
            elif cursor.fetchone() is not None:
                error = 'Airline Staff {} already exists.'.format(username)
            elif error is None:
                try:
                    cursor.execute("INSERT INTO staff (username, pwd, first_name, last_name, date_of_birth, airline) values(%s,%s,%s,%s,%s,%s)", (
                        username, generate_password_hash(password), fname, lname, bday, airline))
                    db.commit()
                    cursor.execute(
                        'INSERT INTO staff_phone (phone_number, username) values (%s,%s)', (phone, username))
                    db.commit()
                    return redirect(url_for('auth.register_confirm', role=role, BAID=BAID))
                except pymysql.Error as e:
                    db.rollback()  # if register not successful then rollback
                    error = e.args[1]
            flash(error)

        # Booking Agent Register
        elif role == 'b':  # b for Booking Agent
            email = request.form['email']
            password = request.form['password']
            password_c = request.form['password_c']
            cursor.execute(
                'SELECT email FROM booking_agent WHERE email = %s', (email,))
            if not email:
                error = "Email is required."
            elif not password:
                error = "Password is required."
            elif password_c != password:
                error = "Passwords do not match"
            elif cursor.fetchone() is not None:
                error = "Email is already used."
            elif error is None:
                BAID = str(uuid.uuid4())[:8]  # generate Booking Agent ID
                cursor.execute(
                    "SELECT * FROM booking_agent where BAID = %s", (BAID,))
                if cursor.fetchone() is not None:
                    BAID = str(uuid.uuid4())[:8]  # generate Booking Agent ID
                try:
                    cursor.execute("INSERT INTO booking_agent (email, pwd, BAID) values (%s,%s,%s)", (
                        email, generate_password_hash(password), BAID))
                    db.commit()
                    return redirect(url_for('auth.register_confirm', role=role, BAID=BAID))

                except:
                    db.rollback()
                    error = 'DBError'
            flash(error)

        # Customer Register.
        elif role == 'c':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            password_c = request.form['password_c']
            building = request.form['building']
            street = request.form['street']
            city = request.form['city']
            state = request.form['state']
            phone = request.form['phone']
            passport = request.form['passport']
            # Passport Expiration Date
            passport_exp = request.form['passport_exp']
            passport_country = request.form['passport_country']
            bday = request.form['bday']  # Date of birth
            cursor.execute('SELECT * FROM customer where email = %s', email)
            if not username:
                error = "Username is required"
            elif not email:
                error = "Email is required"
            elif not password:
                error = "Password is required"
            elif password != password_c:
                error = "Passwords do not match"
            elif not building:
                error = "Building is required"
            elif not street:
                error = "Street is required"
            elif not city:
                error = "City is required"
            elif not state:
                error = "State is required"
            elif not passport:
                error = "Passport is required"
            elif not passport_exp:
                error = "Passport expiration date is required"
            elif not passport_country:
                error = "Passport Country is required"
            elif not phone:
                error = "Phone is required"
            elif not bday:
                error = "Date of birth is required"
            elif cursor.fetchone() is not None:
                error = "This Email is already registered."
            elif error is None:
                try:
                    cursor.execute("INSERT INTO customer (email, name, pwd, building_number, street, city, state, passport_number, passport_expiration_date, passport_country, date_of_birth) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
                        email, username, generate_password_hash(password), building, street, city, state, passport, passport_exp, passport_country, bday))
                    db.commit()
                    cursor.execute(
                        "INSERT INTO customer_phone (phone, email) values (%s, %s)", (phone, email))
                    db.commit()
                    return redirect(url_for('auth.register_confirm', role=role, BAID=BAID))
                except pymysql.Error as e:
                    db.rollback()
                    error = e.args[1]
            flash(error)
            # redirect(url_for('auth.login'), role = role)

    if role == 'a':  # fetch all airline names if visiting airline staff registration page
        cursor.execute("SELECT * from airline")
        airlines = cursor.fetchall()
        return render_template('a/reg_a.html', error=error, role=role, airlines=airlines)
    # Booking Agent & Customer Login
    return render_template('{}/reg_{}.html'.format(role, role), error=error, role=role)


@bp.route('/register/confirm/<role>/<BAID>')
def register_confirm(role, BAID):
    """
    Registration Confirm Page.

    Args:
        BAID: Booking Agent ID, if a booking agent registered.
        role: role of the user who tries to register

    Returns:
        Confirm Page
    """

    return render_template('reg_confirm.html', role=role, BAID=BAID)


@bp.route('/login/')
def login_index():
    """
    Return Login Index page.

    Args:
        None.    
    Returns:
        The Login index page.
    """

    return render_template('login_index.html')


@bp.route('/login/<role>', methods=('GET', 'POST'))
def login(role):
    """
    Login function depending on roles.

    Args:
        role: role.

    Returns:
        Redirect to index if login successful. Error message otherwise.
    """
    if request.method == 'POST':
        # requested by POST
        error = None
        db = get_db()
        cursor = db.cursor()
        # airline staff
        if role == 'a':
            username = request.form['username']
            password = request.form['password']
            cursor.execute('SELECT * from staff WHERE username = %s',
                           (username,))  # Fetch user info
            user = cursor.fetchone()
            if user is None:
                error = "Incorrect Username"
            elif not check_password_hash(user[1], password):
                error = "Incorrect Password"

            if error is None:
                session.clear()
                session['role'] = 'a'
                session['username'] = username
                return redirect(url_for('a.index'))

            flash(error)
            return render_template('a/login_a.html')

        # booking agent
        if role == 'b':
            email = request.form['email']
            BAID = request.form['BAID']
            password = request.form['password']
            cursor.execute(
                'SELECT * FROM booking_agent WHERE BAID = %s', (BAID,))
            user = cursor.fetchone()
            if user is None:
                error = "Incorrect BAID"
            elif user[0] != email:
                error = "Incorrect Email"
            elif not check_password_hash(user[1], password):
                error = "Incorrect Password"

            if error is None:
                session.clear()
                session['BAID'] = BAID
                session['role'] = 'b'
                return redirect(url_for('b.index'))

            flash(error)
            return render_template('b/login_b.html')

        # customer
        if role == 'c':
            email = request.form['email']
            password = request.form['password']
            cursor.execute("SELECT * FROM customer WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user is None:
                error = 'Incorrect Email'
            elif not check_password_hash(user[2], password):
                error = 'Incorrect Password'
            if error is None:
                session.clear()
                session['email'] = email
                session['role'] = 'c'
                return redirect(url_for('c.index'))
            flash(error)
            return render_template('c/login_c.html')

    # Requested by GET, the user is trying to login
    if role == 'a':
        return render_template('a/login_a.html')
    if role == 'b':
        return render_template('b/login_b.html')
    if role == 'c':
        return render_template('c/login_c.html')


@bp.before_app_request
def load_logged_in_user():
    """
    If logged in and session hasn't expired, user doesn't need to login again.
    By default, all identity information is stored in g.user

    Args:
        None    
    Returns:
        None
    """

    role = session.get('role')
    if role == 'a':
        username = session.get('username')
        if username is None:
            g.user = None
        else:
            cursor = get_cursor()
            cursor.execute(
                "SELECT * FROM staff WHERE username = %s", (username,))
            g.user = cursor.fetchone()
            g.username = username
            g.role = role
    elif role == 'b':
        BAID = session.get('BAID')
        if BAID is None:
            g.user = None
        else:
            cursor = get_cursor()
            cursor.execute(
                "SELECT * FROM booking_agent WHERE BAID = %s", (BAID,))
            g.user = cursor.fetchone()
            g.BAID = BAID  # Booking Agent ID
            g.role = role
    elif role == 'c':
        email = session.get('email')
        name = session.get('name')
        if email is None:
            g.user = None
            g.role = role
        else:
            cursor = get_cursor()
            cursor.execute("SELECT * FROM customer WHERE email = %s", (email,))
            g.user = cursor.fetchone()
            g.username = g.user[1]  # username column
            g.role = role
    else:
        g.user = None


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('utils.index'))


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
        return view(**kwargs)

    return wrapped_view
