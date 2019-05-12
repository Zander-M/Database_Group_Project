# Database Group Project Doc

## Introduction

This document is a descriptions of the Airline Management System designed by Yijian Liu(yjl450) and Zander Mao (zm800). We've designed and implemented different functions for different pages and for different users. You can find how every function is implemented in this doc and also some other details.

## Overview

Front-end: Bootstrap 4 + Jquery
Back-end: Flask
Database: MySQL

## Project Structure

### Directory Tree:

└─AMS
    ├─db
    ├─static
    │  └─js
    │      └─bootstrap-4.3.1-dist
    │          └─bootstrap-4.3.1-dist
    │              ├─css
    │              └─js
    ├─templates
    │  ├─a
    │  ├─b
    │  └─c
    ├─tests
    └─venv

db:  
All the database related files, including SQL required to initialize the database and the data for test cases.

static:  
Static files, including photos for index page, dashboard page, favicon and other js dependencies, like jQuery and Bootstrap.

templates:  
HTML templates. All the HTML templates here. Page templates for different users are stored in the corresponding folders.

tests:  
Test functions for the system. Not finished yet.

venv:  
Environment related files. Currently not used.

## File Tree:

db:  

* AMS_ddl.sql: Original SQL than initialize the database. Not used currently since we changed several tables.  
* AMS_insert.sql: Test insertion. Not used currently since we changed several tables.  
* AMS_query.sql: Test queries. Not used currently since we changed several tables.  
* ams_schema.sql: The latest database structure. Exported from MySQL. Used to initialize the database.  

static:

* favicon.ico: Favicon.
* footer.jpg: Footer image
* journey.jpg: Banner image

* js
  * awesome.js: Awesome font javascript
  * jquery-3.4.0.js: jQuery javascript
  * bootstrap-4.3.1-dist: Directory for bootstrap javascript modules

templates:

* a: Directory for airline staff pages.
* b: Directory for booking agent pages.
* c: Directory for customer pages.
* 404.html: Page Not Found Template
* auth_index.html: Not login redirect page. If a user is not logged in and tries to access one of the pages that requires login, the user will reach this page and will be redirected to the index page in 5 secs.
* dashboard.html: template for (some) of the user dashboards, showing the header banner and footer.
