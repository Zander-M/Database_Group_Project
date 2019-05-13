# Database Group Project Doc

## Introduction

This document is a descriptions of the Airline Management System designed by Yijian Liu(yjl450) and Zander Mao (zm800). We've designed and implemented different functions for different pages and for different users. You can find how every function is implemented in this doc and also some other details.

## Overview

Front-end: Bootstrap 4 + Jquery
Back-end: Flask
Database: MySQL

## Project Structure

### Directory Tree:
```
└─AMS
    ├─db
    ├─static
    ├─templates
    │  ├─a
    │  ├─b
    │  └─c
    ├─tests
    └─venv
```
db:  
All the database related files, including SQL required to initialize the database and the data for test cases.

static:  
Static files, including images for index page, dashboard page, favicon.

templates:  
HTML templates. All the HTML templates here. Page templates for different users are stored in the corresponding folders.

tests:  
Test functions for the system. Not finished yet.

venv:  
Environment related files. Currently not used.

### File Tree: 

/ (root folder)

* /_\_init__.py: initialize flask app

* /a.py: generate staff's profile setting and dashboard pages.

* /b.py: generate booking agent's profile setting and dashboard pages.

* /c.py: generate customer's profile setting and dashboard pages.

* /auth.py: handle user registeration, login, and logout.

* /db.py: interact with database.

* /utils.py: generate index page and handle general flight search.

/db 

* /AMS_ddl.sql: Original SQL than initialize the database. **NOT** used currently since we changed several tables.  
* /AMS_insert.sql: Test insertion. **NOT** used currently since we changed several tables.  
* /AMS_query.sql: Test queries. **NOT** used currently since we changed several tables.  
* /ams_schema.sql: The latest database structure. Exported from MySQL. Used to initialize the database. 

/templates
* /index.html: index page, including flight search, flight information search and ordering tickets (for customer and booking agent only)

* /login_index.html: prompt when the the user enter a page that requires a valid account without logging in.

* /login.html: skeleton for all the login pages.

* /reg.html: skeleton for all the registration pages.

* /reg_confirm.html: prompt when a new account is successfully registered and redirect the user to index page.

* /dashboard.html: skeleton for all the dashboard pages and profile pages.

* /role_err.html: prompt when the type of the account does not match the required type of the page and redirect the user to previous page.

* /404.html: special error 404 page.

/templates/c

* /reg_c.html: customer registeration page.

* /login_c.html: customer login page.

* /index_c.html: redirect to customer dashboard page.

* /flights.html: default view of customer dashboard for viewing purchased tickets.

* /bill.html: second tab of dashboard page, displaying spending statistic and bar chart.

* /confirm_order.html: input additional information when purchasing tickets.

* /purchase_success.html: redirect user to dashboard after purchasing ticket.

* /settings.html: view profile and adding phone numbers.

/templates/b

* /login_b.html, /reg_b.html, /index_b.html, /confirm_order.html, /purchase_success.html: similar to customer cases.

* /flights.html: default of dashboard, displaying tickets purchased for customers.

* /commission.html: show commission statistics.

* /customer.html: show the top customers and the commission and ticket number from them.

* /settings.html: special profile page.

/templates/a

* /login_a.html, /reg_a.html, /index_a.html, /settings.html: similar to customer cases.

* /flights.html: display and search for the flights belonging to the airline of the staff.

* /flight_info.html: display the customers of this flight and change its status.

* /add.html: skeleton for addflights.html, addplane.html and addairport.html

* /addflights.html: input information and add a new flight to the database

* /addplane.html: add a new plane and its seat number to the database, and list the current planes.

* /addairport.html: add a new airport to the database, require airport code and the city name.

* /confirm.html: indicate successfule operation after setting flight status, add flights, airplanes or airports and redirect the user to the dashboard. 

* /ba.html: display all the booking agents who have purchased tickets for this airline or some top booking agents.

* /customer.html: display top customer in the last year and allow user to search the order history of a specific customer.

* /reports.html: display various sales statistics, including tickets sold, revenue comparison, top destinations, monthly sales, and detailed purchase over the last month.

/static
* /favicon.ico, /journey.jpg, /footer.jpg
images used in browser tab, banner, and footer