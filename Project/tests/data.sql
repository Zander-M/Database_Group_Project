INSERT INTO airline (name)
VALUES
("China Eastern")

INSERT INTO airport (name, city)
VALUES
("JFK", "New York"),
("CAN", "Guangzhou");

INSERT INTO airplane(airplane_id, airline, seats)
VALUES
(1, "China Eastern", 400)

INSERT INTO `booking_agent`(email, pwd, BAID)
VALUES
("b@test.com", "pbkdf2:sha256:150000$Xztca8lY$4a432c486e6cffb86bde24c69ea7b5e0bcd780f7b21fb5e9a820d47ecfe10dcc", 100)


INSERT INTO `customer`(email, name, pwd, BAID, building_number, street, city, state, passport_number, passport_expiration_date, passport_country, date_of_birth)
VALUES
("f@test.com", "pbkdf2:sha256:150000$SqeCfYik$96f2fac51cf8a115ea6ed6f0f46dd791109ec096e99289d47fe11f9156d86f71", 1, "Second Street", "NYC", "NY", "jke3234", "2019-10-09T16:00:00.000Z", "Jupiter","1985-02-04T16:00:00.000Z")

INSERT INTO `customer_phone`(phone, email)
VALUES
( 18900010001, "f@test.com")

INSERT INTO `flight`(flight_id, airline, airplane_id, base_price, flight_status, dept_time, arrv_time, dept_airport, arrv_airport )
VALUES
(1, "China Eastern", 1, 4000, 0, "2019-06-29T16:20:00.000Z", "2019-06-30T15:58:00.000Z", "CAN", "JFK")

INSERT INTO `staff`(username, pwd, first_name, last_name, date_of_birth, airline)
VALUES
("m", "pbkdf2:sha256:150000O9qPrFVuO9qPrFVud0015140200dc5648fa14018166a2c7c4b3f99a059e868a6f1170ef890dbc337", "m", "m", "1999-12-30T16:00:00.000Z", "China Eastern")

INSERT INTO `staff_phone`(phone_number, username)
VALUES
(12312311223, "m")

INSERT INTO "ticket"(ticket_id, flight_id, `airline`, customer_email, BAID, sold_price, payment_method, card_number, name_on_card, expiration_date, purchase_date_time)
VALUES
(1,1,"China Eastern", "f@test.com", 100, 5800, 0, 1122332211, "f", "2019-08-03T16:00:00.000Z","2019-04-11T23:40:28.000Z")
