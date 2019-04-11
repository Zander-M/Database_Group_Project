#By Zander Mao (zm800) and Yijian Liu (yjl450)

INSERT INTO airline VALUES('China Eastern');
INSERT INTO airport VALUES('JFK', 'NYC');
INSERT INTO airport VALUES('PVG', 'Shanghai');
INSERT INTO customer VALUES('user@nyu.edu', 'user', '123456', 'Silver Center', '31 Washington Pl', 'NYC', 'NY', '123456789', '2019-01-01', 'China', '1996-03-21');
INSERT INTO customer VALUES('customer@gmail.com', 'customer', '654321', 'Tandon', 'Jay St', 'NYC', 'NY', '445566778899', '2021-04-05', 'United States', '1996-03-21');
INSERT INTO customer_phone VALUES(18635498725, 'customer@gmail.com');
INSERT INTO customer_phone VALUES(13954854762, 'user@nyu.edu');
INSERT INTO booking_agent VALUES('booking@live.com', 'password', null);
INSERT INTO booking_agent VALUES('agent@yahoo.com', '22446688', null);
INSERT INTO airplane VALUES(null, 'China Eastern', 200);
INSERT INTO airplane VALUES(null, 'China Eastern', 400);
INSERT INTO staff VALUES('abc123', 'pwdstaff', 'First', 'Last', '1986-12-08', 'China Eastern');
INSERT INTO staff_phone VALUES(18654788456, 'abc123');
INSERT INTO flight VALUES(null, 'China Eastern', 2, 2000, 0, '2019-08-01 19:00:00', '2019-08-02 22:00:00', 'PVG', 'JFK');
INSERT INTO flight VALUES(null, 'China Eastern', 1, 5800, 1, '2019-06-30 00:20:00', '2019-06-30 23:58:00', 'JFK', 'PVG');
INSERT INTO ticket VALUES(null, 2, 'China Eastern', 'user@nyu.edu', NULL, 5678, 0, '2549987526548457', 'ALEX Nelson', '2021-07-31', null);
INSERT INTO ticket VALUES(null, 1, 'China Eastern', 'customer@gmail.com', 1, 1980, 1, '4987582214569854', 'KIMBERLY HARRISON', '2019-08-04', null);