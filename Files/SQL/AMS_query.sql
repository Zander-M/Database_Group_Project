#By Zander Mao (zm800) and Yijian Liu (yjl450)

SELECT * FROM flight WHERE dept_time > CURRENT_TIMESTAMP();
select * FROM flight WHERE flight_status = 1;
SELECT name FROM customer INNER JOIN ticket ON customer.email = ticket.customer_email AND booking_agent_id IS NOT NULL;
SELECT * FROM airplane WHERE airline = 'China Eastern';