#By Zander Mao (zm800) and Yijian Liu (yjl450)

CREATE DATABASE AMS;
USE AMS;

CREATE TABLE airline (
    name VARCHAR(20) PRIMARY KEY
);

CREATE TABLE staff (
    username VARCHAR(10) PRIMARY KEY,
    pwd VARCHAR(40),
    first_name VARCHAR(10),
    last_name VARCHAR(10),
    date_of_birth DATE,
    airline VARCHAR(20),
    FOREIGN KEY (airline)
        REFERENCES airline (name)
        ON DELETE CASCADE
);

CREATE TABLE staff_phone (
    phone_number NUMERIC(15 , 0 ) PRIMARY KEY,
    username VARCHAR(10),
    FOREIGN KEY (username)
        REFERENCES staff (username)
        ON DELETE CASCADE
);

CREATE TABLE airplane (
    airplane_id INT UNSIGNED AUTO_INCREMENT,
    airline VARCHAR(20),
    seat INT CHECK (seat > 0 AND seat < 600),
    PRIMARY KEY (airline , airplane_id),
    FOREIGN KEY (airline)
        REFERENCES airline (name)
        ON DELETE CASCADE,
    KEY (airplane_id)
);

CREATE TABLE airport (
    name CHAR(3) PRIMARY KEY,
    city VARCHAR(20)
);

CREATE TABLE flight (
    flight_id INT UNSIGNED AUTO_INCREMENT,
    airline VARCHAR(20),
    airplane_id INT UNSIGNED,
    base_price INT,
    flight_status INT, # 0 as on-time, 1 as delayed
    dept_time DATETIME,
    arrv_time DATETIME,
    dept_airport CHAR(3),
    arrv_airport CHAR(3),
    KEY (flight_id),
    PRIMARY KEY (airline , flight_id),
    FOREIGN KEY (airline , airplane_id)
        REFERENCES airplane (airline , airplane_id)
        ON DELETE CASCADE,
    FOREIGN KEY (dept_airport)
        REFERENCES airport (name),
    FOREIGN KEY (arrv_airport)
        REFERENCES airport (name)
);

CREATE TABLE booking_agent (
    email VARCHAR(30),
    pwd VARCHAR(8),
    booking_agent_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY
);

CREATE TABLE customer (
    email VARCHAR(30) PRIMARY KEY,
    name VARCHAR(20),
    pwd VARCHAR(40),
    building_number VARCHAR(20),
    street VARCHAR(20),
    city VARCHAR(20),
    state VARCHAR(14),
    passport_number VARCHAR(20),
    passport_expiration_date DATE,
    passport_country VARCHAR(20),
    date_of_birth DATE
);

CREATE TABLE customer_phone (
    phone_number NUMERIC(15 , 0 ) PRIMARY KEY,
    email VARCHAR(30),
    FOREIGN KEY (email)
        REFERENCES customer (email)
        ON DELETE CASCADE
);

CREATE TABLE ticket (
    ticket_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    flight_id INT UNSIGNED,
    airline VARCHAR(20),
    customer_email VARCHAR(30),
    booking_agent_id INT UNSIGNED,
    sold_price INT,
    payment_method INT, # 0 as credit, 1 as debit
    card_number NUMERIC(20 , 0 ),
    name_on_card VARCHAR(20),
    expiration_date DATE,
    purchase_date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (airline , flight_id)
        REFERENCES flight (airline , flight_id)
        ON DELETE CASCADE,
    FOREIGN KEY (booking_agent_id)
        REFERENCES booking_agent (booking_agent_id),
    FOREIGN KEY (customer_email)
        REFERENCES customer (email)
);