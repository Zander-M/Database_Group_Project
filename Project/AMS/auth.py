# -*- coding: UTF-8 -*- #
# Author: Zander_M
# Time: April, 25, 2019
# Title: Authentication File

import functools
import uuid

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from AMS.db import get_db, get_cursor

bp = Blueprint('auth',__name__, url_prefix="/auth")

@bp.route('/register/<role>', methods=('GET', 'POST'))
def register(role='c'):
    """
    Register in the system. Based on different roles in the system, return
    different register page.
    
    Args:
        role: Role of the user. Default is user.
    
    Returns:
        If requested by get, return rendered register page.
        If requested by post, redirect to login page if registered successfully,
        else return error msg.
    """
    error = None
    db = get_db()
    cursor = db.cursor()
    if request.method == "POST": # from register form submit, verify if register is successful.

        # Airline Staff register
        if role == 'a': # a for Airline Staff
            username = request.form['username']
            password = request.form['password']
            password_c = request.form['password_c']
            fname = request.form['fname'] # first name
            lname = request.form['lname'] # last name
            bday = request.form['bday'] # birthday
            airline = request.form['airline'] # birthday
            phone = request.form['phone']
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
            elif cursor.execute(
                'SELECT username from staff WHERE username = "%s"',(username)).fetchone() is not None:
                error = 'Airline Staff {} already exists.'.format(username)
            elif error is None:
                try:
                    cursor.execute('INSERT INTO staff values("%s","%s","%s","%s","%s","%s",)',(username,generate_password_hash(password), fname, lname, bday, airline))
                    cursor.execute('INSERT INTO staff_phone values ("%s","%s")',(phone, username))
                    db.commit()
                    return redirect(url_for('auth.login',role = role))
                except:
                    db.rollback() # if register not successful then rollback
            
        # Booking Agent Register
        elif role == 'b': # b for Booking Agent
            email = request.form['email']
            password = request.form['password']
            password_c = request.form['password_c']
            if not email:
                error = "Email is required."
            elif not password:
                error = "Password is required."
            elif password_c != password:
                error = "Passwords do not match"
            elif cursor.execute('SELECT email FROM booking_agent WHERE email = "%s"', (email)).fetchone() is not None:
                error = "Email is already used."
            elif error is None:
                BAID = str(uuid.uuid4())[:8] # generate Booking Agent ID
                if cursor.execute("SELECT * FROM booking_agent where booking_agent_id = '%s'", (BAID)).fetchone() is not None:
                    BAID = str(uuid.uuid4())[:8] # generate Booking Agent ID
            try:
                cursor.execute("INSERT INTO booking_agent values ('%s','%s','%s')",(email, generate_password_hash(password), BAID))
                db.commit()
            except:
                db.rollback()
            return redirect(url_for('auth.login', role=role))

        # Customer Register. By default, 
        elif role == 'c':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            password_c = request.form['password_c']
            building = request.form['building']
            street = request.form['street']
            state = request.form['state']
            phone = request.form['phone']
            passport = request.form['passport']
            passport_exp= request.form['passport_exp'] # Passport Expiration Date
            passport_country = request.form['passport_country']
            bday = request.form['bday'] # Date of birth
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
            elif cursor.execute('SELECT * FROM customer where email = "%s"', email).fetchone() is not None:
                error = "This Email is already registered."
            elif error is None:
                try:
                    cursor.execute("INSERT INTO customer values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',)",(email, username, generate_password_hash(password), building, street, state, passport, passport_exp, passport_country, bday))
                    cursor.execute("INSERT INTO customer_phone values ('%s', '%s')", (phone, email)) 
                    db.commit()
                except:
                    db.rollback()
            redirect(url_for(auth.login), role = role)


    if role == 'a': # fetch all airline names if role is airline staff
        cursor.execute("SELECT * from airline")
        airlines = cursor.fetchall()
    flash(error)
    return render_template('reg_{}.html'.format(role), error = error, role = role, airlines = airlines)

@bp.route('/login/<role>')
def login(role):
    """
    Login function depending on roles.
    
    Args:
        role: role.
    
    Returns:
        Redirect to index if login successful. Error message otherwise.
    """
    pass
    