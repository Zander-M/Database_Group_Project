# Use cases required by the system

###### content wrapped in the percentage sign indicates the user input.

1. View Public Info: All users, whether logged in or not, can  

    a. Search for future flights based on source city/airport name, destination city/airport name, departure date for one way (departure and arrival dates for round trip).  

    Implemented in utils.py. Users can search based on departure date, arrival date, departure airport and arrival airport in the index page. Result will be displayed under the search the form. Ticket price is calculated by getting the seat on the plane and counting the ticket sold and operate on the base price. If choose to do round trip, search again by reversing the departure airport and arrival airport and search again based on back date.  

        Search for flights: SELECT * from `flight` WHERE dept_airport= %departure airport% AND arrv_airport = %arrival airport% and DATE(dept_time) = %departure date%  

        Count ticket sold: SELECT COUNT(flight_id) FROM ticket WHERE flight_id = %flight id% GROUP BY flight_id  

        Find out seat available: SELECT seat FROM airplane where airplane_id = %airplane id%  

    b. Will be able to see the flights status based on airline name, flight number, arrival/departure date.  

    Implemented in utils.py. Users can search based on flight id, airline, departure date and arrival date in the index page. A list of search result will be displayed under the search form.  

        Search for flights: SELECT * from `flight` WHERE flight_id = %flight id$ AND DATE(dept_time)= %departure date% AND DATE(arrv_time)= %arrival date% and airline = %airline%  

        Count ticket sold & Find out seat available are the same as search based on departure date and arrival date.  

2. Register: 3 types of user registrations (Customer, Booking agent, Airline Staff) option via forms.  

    All the register functions are implemented in the Navigation Bar>Register tab. Click corresponding tab to register for different users.  

    Airline Staff Register:  

        Check Duplicate:  SELECT * from `staff` WHERE `username` = %username%  

        Register:  INSERT INTO staff (username, pwd, first_name, last_name, date_of_birth, airline) values(%username%,%password%,%first_name%,%last_name%,%date_of_birth%,%airline%)

        Choose Airline:  SELECT * from airline

        Insert phone number: INSERT INTO staff_phone (phone_number, username) values (%phone_number%,%username%)  

    Booking Agent Register:  

        Check Email Duplicate: SELECT email FROM booking_agent WHERE email = %email%  

        Check Booking Agent Duplicate: SELECT * FROM booking_agent WHERE BAID = %booking agent ID%  

        Register:  INSERT INTO booking_agent (email, pwd, BAID) values (%email%,%password%,%booking agent ID%)  

    Customer Register:

        Check Email Duplicate: SELECT * FROM customer where email = %s

        Register: INSERT INTO customer (email, name, pwd, building_number, street, city, state, passport_number, passport_expiration_date, passport_country, date_of_birth) values (%email%,%name%,%password%,%building number%,%street%,%city%,%state%,%passport number%,%passport expiration date%,%passport country%,%date of birth%)

3. Login: 3 types of user login (Customer, Booking agent, Airline Staff). Users enters their username (email address will be used as username), x, and password, y, via forms on login page. This data is sent as POST parameters to the login-authentication component, which checks whether there is a tuple in the Person table with username=x and the password = md5(y).

    All the login functions are implemented in the Navigation Bar>Register tab. Click corresponding tab to register for different users.  

        Airline Staff Login: SELECT * from staff WHERE username = %username%

        Booking Agent Login: SELECT * FROM booking_agent WHERE BAID = %booking agent ID%

        Customer Login: SELECT * FROM customer WHERE email = %email%

Customer use cases:
After logging in successfully a user(customer) may do any of the following use cases:

All the customer related functions are in the c.py file.

4. View My flights: Provide various ways for the user to see flights information which he/she purchased. The default should be showing for the future flights. Optionally you may include a way for the user to specify a range of dates, specify destination and/or source airport name or city name etc.

    By default, when logged in, customers will directly go to the index page displaying all the purchased flights.

        Search for flights: SELECT airline, dept_time, dept_airport, arrv_time, arrv_airport, flight_status FROM flight NATURAL JOIN ticket WHERE customer_email = %customer email%

5. Search for flights: Search for future flights (one way or round trip) based on source city/airport name, destination city/airport name, dates (departure or arrival).

    By clicking Home/Search button on the navigation bar, customer can go to a page similar to the index homepage and perform search. Query is the same as the homepage.  
    To go back to my flights, click Navigation Bar->{username}-> My Dashboard

6. Purchase tickets: Customer chooses a flight and purchase ticket for this flight, providing all the needed data, via forms. You may find it easier to implement this along with a use case to search for flights.

    After Search, user can click the order button next to the search result. Then the webpage will redirect the user to an order confirm page. After an order is confirmed, redirect to order confirm page.

        Order Ticket: INSERT INTO ticket (flight_id, airline, customer_email, sold_price, payment_method, card_number, name_on_card, expiration_date, purchase_date_time) VALUES (%flight id%,%airline%,%customer email%,%sold price%,%payment method%,%card number%,%name on card%,%expiration date%,CURTIME())

7. Track My Spending: Default view will be total amount of money spent in the past year and a bar chart showing month wise money spent for last 6 months. He/she will also have option to specify a range of dates to view total amount of money spent within that range and a bar chart showing month wise money spent within that range.  

    Click Spending tab in the dashboard to navigate to the page displaying expenses.

        Search expenses: SELECT SUM(sold_price) from ticket where DATE(purchase_date_time) BETWEEN %start date% AND %end date% AND customer_email = %customer email% GROUP BY customer_email
        Past year expenses: SELECT SUM(sold_price) from ticket where purchase_date_time BETWEEN DATE_SUB(NOW(), INTERVAL 1 YEAR) AND NOW() AND customer_email = %customer email% GROUP BY customer_email

    For past six months' expenses we perform query for six times (so the chart can be drawn easier).

        Past six month expenses: SELECT SUM(sold_price) from ticket where MONTH(purchase_date_time) = MONTH(NOW()) - %s AND customer_email = %s GROUP BY customer_email

8. Logout: The session is destroyed and a “goodbye” page or the login page is displayed.

    Click Navigation bar->{user name}->logout

Booking agent use cases:
After logging in successfully a booking agent may do any of the following use cases:

All the booking agent related functions are in the b.py file.

4. View My flights: Provide various ways for the booking agents to see flights information for which he/she purchased on behalf of customers. The default should be showing for the future flights. Optionally you may include a way for the user to specify a range of dates, specify destination and/or source airport name and/or city name etc to show all the flights for which he/she purchased tickets.

    By default, when logged in, booking agent will directly go to the index page displaying all the purchased flights.

        Search for flights: SELECT airline, dept_time, dept_airport, arrv_time, arrv_airport, flight_status FROM flight NATURAL JOIN ticket WHERE BAID = %booking agent ID%

5. Search for flights: Search for future flights (one way or round trip) based on source city/airport name, destination city/airport name, dates (departure or arrival).

    By clicking Home/Search button on the navigation bar, booking agent can go to a page similar to the index homepage and perform search. Query is the same as the homepage.  
    To go back to my flights, click Navigation Bar->{username}-> My Dashboard

6. Purchase tickets: Booking agent chooses a flight and purchases tickets for other customers giving customer information and payment information, providing all the needed data, via forms. You may find it easier to implement this along with a use case to search for flights.

    After Search, booking agent can click the order button next to the search result. Then the webpage will redirect the user to an order confirm page. After an order is confirmed, redirect to order confirm page. The only difference between this form and customer purchase form is that customer email is required in this form, and the booking agent id will be inserted to the table.

        Order Ticket: INSERT INTO ticket (flight_id, airline, customer_email, BAID, sold_price, payment_method, card_number, name_on_card, expiration_date, purchase_date_time) VALUES (%flight id%,%airline%,%customer email%, %booking agent id%, %sold price%,%payment method%,%card number%,%name on card%,%expiration date%,CURTIME())

7. View my commission: Default view will be total amount of commission received in the past 30 days and the average commission he/she received per ticket booked in the past 30 days and total number of tickets sold by him in the past 30 days. He/she will also have option to specify a range of dates to view total amount of commission received and total numbers of tickets sold.

    Click Commission tab to visit commission page. By default, past 30-day data will be presented. Also, booking agent can specify a time range to see the commission data within that time range.

        Search past 30 day commission: SELECT SUM(sold_price)*0.1 FROM ticket WHERE BAID = %booking agent id% AND purchase_date_time BETWEEN DATE_SUB(CURDATE(), INTERVAL 30 DAY) AND NOW()
        Search past 30 day commission average: SELECT AVG(sold_price)*0.1 FROM ticket WHERE BAID = %booking agent id% AND purchase_date_time BETWEEN DATE_SUB(CURDATE(), INTERVAL 30 DAY) AND NOW()
        Search past 30 day commission number: SELECT COUNT(*) FROM ticket WHERE BAID = %booking agent id% AND purchase_date_time BETWEEN DATE_SUB(CURDATE(), INTERVAL 30 DAY) AND NOW()

8. View Top Customers: Top 5 customers based on number of tickets bought from the booking agent in the past 6 months and top 5 customers based on amount of commission received in the last year. Show a bar chart showing each of these 5 customers in x-axis and number of tickets bought in y-axis. Show another bar chart showing each of these 5 customers in x-axis and amount commission received in y-axis.

    Click Top Customer tab to visit top customer page. By default, data& bar chart of the customer who purchased most tickets in the last 6 month and data& bar chart of the customer who provided most commissions will be displayed.

        Select user who purchased most tickets in the past 6 months: SELECT name, email, COUNT(email) FROM customer RIGHT JOIN ticket on customer.email = ticket.customer_email WHERE BAID=%booking agent id%  AND purchase_date_time BETWEEN DATE_SUB(CURDATE(), INTERVAL 6 MONTH) AND NOW() GROUP BY(email) ORDER BY COUNT(email) DESC LIMIT 5

        Select user who contributed most commission fee: SELECT name, email, SUM(sold_price)*0.1 FROM customer RIGHT JOIN ticket on customer.email = ticket.customer_email WHERE BAID = %booking agent id% AND purchase_date_time BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 YEAR) AND NOW() GROUP BY(email) ORDER BY SUM(sold_price) DESC LIMIT 5

9. Logout: The session is destroyed and a “goodbye” page or the login page is displayed.

    Click Navigation bar->{user name}->logout

Airline Staff use cases:
After logging in successfully an airline staff may do any of the following use cases:

All the Airline Staff functions are in the a.py file.

4. View My flights: Defaults will be showing all the future flights operated by the airline he/she works for the next 30 days. He/she will be able to see all the current/future/past flights operated by the airline he/she works for based range of dates, source/destination airports/city etc. He/she will be able to see all the customers of a particular flight.

    By default, when an airline staff is logged in, the user will go to view my flights page. The flights of the airline the user is working for will be displayed in a table. Additionally, airline staff can specify a time range, departure airport and arrival airport.

        Search future 30 day flights: SELECT dept_airport, arrv_airport, DATE_FORMAT(dept_time, "%Y %M %D %T"), DATE_FORMAT(dept_time, "%Y %M %D %T"), flight_status, base_price, flight_id FROM flight WHERE airline = %airline% AND DATE(dept_time) BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY)
        Search arbitrary time range flights: SELECT dept_airport, arrv_airport, DATE_FORMAT(dept_time, "%Y %M %D %T"), DATE_FORMAT(dept_time, "%Y %M %D %T"), flight_status, base_price, flight_id FROM flight WHERE airline = %airline% AND DATE(dept_time) BETWEEN DATE(%start_time%) AND DATE(%end time%) AND dept_airport = %departure airport% AND arrv_airport = %arrival airport%

5. Create new flights: He or she creates a new flight, providing all the needed data, via forms. The application should prevent unauthorized users from doing this action. Defaults will be showing all the future flights operated by the airline he/she works for the next 30 days.

    To create new flights, go to tab Add->Add flights. Put in all required data and click submit, then a new flight will be added in the system.

        Get all planes owned by the company: SELECT airplane_id FROM airplane WHERE airline = %airline%
        Add new flight: INSERT INTO flight (airline, airplane_id, base_price, flight_status, dept_time, arrv_time, dept_airport, arrv_airport) values (%airline%,%airplane id%,%base price%,%flight statue%,%departure time%,%arrival time%,%departure airport%,%arrival airport%)

6. Change Status of flights: He or she changes a flight status (from on-time to delayed or vice versa) via forms.

    Such can be done by changing the status in the View My flights page: at the end of each search result there is a More Info & Changes Status button. Click the button, it will lead the user to a flight info & change flight status page. On that page, airline staff can see all customers who is on that flight and can change the flight status.

        Change status: UPDATE flight SET flight_status=%flight status% WHERE flight_id = %flight_id%

7. Add airplane in the system: He or she adds a new airplane, providing all the needed data, via forms. The application should prevent unauthorized users from doing this action. In the confirmation page, she/he will be able to see all the airplanes owned by the airline he/she works for.

    To add new planes, go to tab Add->Add Plane, input the seat number of the plane and a new plane will be added.

        Display all current planes of the airline: SELECT airplane_id, seat FROM airplane WHERE airline = %airline%
        Add plane: INSERT INTO airplane (airline, seat) values (%airline%, %seat%)

8. Add new airport in the system: He or she adds a new airport, providing all the needed data, via forms. The application should prevent unauthorized users from doing this action.

    To add new airports, go to tab Add->Add Airport, input the airport name and city of the airport and a new airport will be added. If the airport is in the system, an error message will be displayed.

        Check airport: SELECT * FROM airport WHERE name = %airport name%
        Add airport: INSERT INTO airport (name, city) values (%airport name%, %airport city%)

9.  View all the booking agents: Top 5 booking agents based on number of tickets sales for the past month and past year. Top 5 booking agents based on the amount of commission received for the last year.

    To see such information go to Booking Agent tab. Tables of results will be displayed: All booking agent data, Top 5 Booking agent based on commission fee 3 months/year wise and Top 5 Booking Agent based on tickets sold 3 months/year wise. Click on different tabs to see different results.

        All booking agent: SELECT BAID, COUNT(BAID)FROM ticket WHERE BAID IS NOT NULL AND airline = %s GROUP BY BAID ORDER BY COUNT(BAID) DESC
        Last 3 months ordering by number of tickets sold: SELECT BAID, COUNT(BAID)FROM ticket WHERE BAID IS NOT NULL AND airline = %airline% AND DATE(purchase_date_time) BETWEEN DATE_SUB(CURDATE(), INTERVAL 3 MONTH) AND CURDATE() GROUP BY BAID ORDER BY COUNT(BAID) DESC LIMIT 5
        Last year ordering by number of tickets sold: SELECT BAID, COUNT(BAID)FROM ticket WHERE BAID IS NOT NULL AND airline = %airline% AND DATE(purchase_date_time) BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 YEAR) AND CURDATE() GROUP BY BAID ORDER BY COUNT(BAID) DESC LIMIT 5
        Last 3 months ordering by commission fee: SELECT BAID, SUM(sold_price)*0.1 FROM ticket WHERE BAID IS NOT NULL AND airline=%airline% AND DATE(purchase_date_time) BETWEEN DATE_SUB(CURDATE(), INTERVAL 3 MONTH) AND CURDATE() GROUP BY BAID ORDER BY SUM(sold_price) DESC LIMIT 5
        Last year ordering by commission fee: SELECT BAID, SUM(sold_price)*0.1 FROM ticket WHERE BAID IS NOT NULL AND airline = %airline% AND DATE(purchase_date_time) BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 YEAR) AND CURDATE() GROUP BY BAID ORDER BY SUM(sold_price) DESC LIMIT 5

10. View frequent customers: Airline Staff will also be able to see the most frequent customer within the last year. In addition, Airline Staff will be able to see a list of all flights a particular Customer has taken only on that particular airline.

    To see frequent customers, go to tab Frequent Customer. By default most frequent customer in the past year will be displayed. To see all the flights a particular customer has taken, input the customer's email in the search box and click submit, a table of all the flights of the customer taken in the airline will be displayed.

        Search most frequent customer: SELECT name, email, COUNT(customer_email) FROM customer RIGHT JOIN ticket on customer.email = ticket.customer_email WHERE airline = %airline% GROUP BY email ORDER BY COUNT(customer_email) DESC LIMIT 1
        Search particular customer: SELECT flight.flight_id, dept_airport, dept_time, arrv_airport, arrv_time FROM flight LEFT JOIN ticket on ticket.flight_id = flight.flight_id WHERE ticket.customer_email = %customer email% AND flight.airline = %airline%

11. View reports: Total amounts of ticket sold based on range of dates/last year/last month etc. Month wise tickets sold in a bar chart.
12. Comparison of Revenue earned: Draw a pie chart for showing total amount of revenue earned from direct sales (when customer bought tickets without using a booking agent) and total amount of revenue earned from indirect sales (when customer bought tickets using booking agents) in the last month and last year.
13. View Top destinations: Find the top 3 most popular destinations for last 3 months and last year.
    
    All the functions above are implemented in the Sales Report tab.
    By default, bar chart of tickets sold in the past year, purchase record of last month, pie chart of revenue comparison of the past month/year, top destination of past 3 month/ year will be shown. Airline staff can also specify a range to see how many tickets are sold during the time interval.

        Last month sales data: SELECT name, customer_email, purchase_date_time FROM ticket LEFT JOIN customer ON ticket.customer_email = customer.email WHERE purchase_date_time BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 MONTH) AND CURDATE() AND airline = %airline%
        Last year sales data: SELECT MONTH(purchase_date_time), COUNT(*) FROM ticket WHERE purchase_date_time BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 YEAR) AND CURDATE() AND airline = %s GROUP BY MONTH(purchase_date_time) ORDER BY MONTH(purchase_date_time) ASC
        Last month indirect sales data: SELECT SUM(sold_price)*0.9 FROM ticket WHERE BAID IS NOT NULL AND airline = %airline% AND purchase_date_time BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 MONTH) AND CURDATE()
        Last month direct sales data: SELECT SUM(sold_price) FROM ticket WHERE BAID IS NULL AND airline = %airline% AND purchase_date_time BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 MONTH) AND CURDATE()
        Last year indirect sales data: SELECT SUM(sold_price)*0.9 FROM ticket WHERE BAID IS NOT NULL AND airline = %airline% AND purchase_date_time BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 YEAR) AND CURDATE()
        Last year direct sales data: SELECT SUM(sold_price) FROM ticket WHERE BAID IS NULL AND airline = %airline% AND purchase_date_time BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 YEAR) AND CURDATE()
        Top 3 Destination in last 3 months: SELECT arrv_airport FROM flight WHERE airline = %airline% AND dept_time BETWEEN DATE_SUB(CURDATE(), INTERVAL 3 MONTH) AND CURDATE() GROUP BY arrv_airport ORDER BY COUNT(arrv_airport) DESC LIMIT 3
        Top 3 Destination in last year: SELECT arrv_airport FROM flight WHERE flight.airline = %s AND dept_time BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 YEAR) AND CURDATE() GROUP BY arrv_airport ORDER BY COUNT(arrv_airport) DESC LIMIT 3

14. Logout: The session is destroyed and a “goodbye” page or the login page is displayed.

    Click Navigation bar->{user name}->logout

15. Security Concerns:

    When an user is logged in, we will store the role of the user in the session. Before responding to any request for an login required/ role specific page, we check whether the user is logged in and whether the user's role matches the role required to perform such action. When a user is logged out, the session will be destroyed.  
    For every SQL query, we use templates to process the inputs to prevent SQL injection.
    