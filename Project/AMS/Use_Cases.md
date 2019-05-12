# Use cases required by the system

1. View Public Info: All users, whether logged in or not, can  

    a. Search for future flights based on source city/airport name, destination city/airport name, departure date for one way (departure and arrival dates for round trip).  

    Implemented in utils.py. Users can search based on departure date, arrival date, departure airport and arrival airport in the index page. Result will be displayed under the search the form. Ticket price is calculated by getting the seat on the plane and counting the ticket sold. If choose to do round trip, search again by reversing the departure airport and arrival airport and search again based on back date.  

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

        Insert phone number: INSERT INTO staff_phone (phone_number, username) values (%phone_number%,%username%)  

    Booking Agent Register:  

        Check Email Duplicate: SELECT email FROM booking_agent WHERE email = %email%  

        Check Booking Agent Duplicate: SELECT * FROM booking_agent WHERE BAID = %booking agent ID%  

        Register:  INSERT INTO booking_agent (email, pwd, BAID) values (%email%,%password%,%booking agent ID%)  

    Customer Register:


3. Login: 3 types of user login (Customer, Booking agent, Airline Staff). Users enters their username (email address will be used as username), x, and password, y, via forms on login page. This data is sent as POST parameters to the login-authentication component, which checks whether there is a tuple in the Person table with username=x and the password = md5(y).
a. If so, login is successful. A session is initiated with the member’s username stored as a session variable. Optionally, you can store other session variables. Control is redirected to a component that displays the user’s home page.
b. If not, login is unsuccessful. A message is displayed indicating this to the user.
Note: In real applications, members’ passwords are stored as md5/other hashes, not as plain text. This keeps the passwords more secure, in case someone is able to break into the system and see the passwords. You can perform the hash using MySQL’s md5 function or a library provided with your host language.) Once a user has logged in, reservation system should display his/her home page. Also, after other actions or sequences of related actions, are executed, control will return to component that displays the home page. The home page should display
c. Error message if the previous action was not successful,
d. Some mechanism for the user to choose the use case he/she wants to execute. You may choose to provide links to other URLS that will present the interfaces for other use cases, or you may include those interfaces directly on the home page.
e. Any other information you’d like to include. For example, you might want to show customer's future flights information on the customer's home page, or you may prefer to just show them when he/she does some of the following use cases.
Customer use cases:
After logging in successfully a user(customer) may do any of the following use cases:
4. View My flights: Provide various ways for the user to see flights information which he/she purchased. The default should be showing for the future flights. Optionally you may include a way for the user to specify a range of dates, specify destination and/or source airport name or city name etc.
5. Search for flights: Search for future flights (one way or round trip) based on source city/airport name, destination city/airport name, dates (departure or arrival).
6. Purchase tickets: Customer chooses a flight and purchase ticket for this flight, providing all the needed data, via forms. You may find it easier to implement this along with a use case to search for flights.
7.Track My Spending: Default view will be total amount of money spent in the past year and a bar
chart showing month wise money spent for last 6 months. He/she will also have option to specify a
range of dates to view total amount of money spent within that range and a bar chart showing month
wise money spent within that range.
8.Logout: The session is destroyed and a “goodbye” page or the login page is displayed.
Booking agent use cases:
After logging in successfully a booking agent may do any of the following use cases:
4. View My flights: Provide various ways for the booking agents to see flights information for which he/she purchased on behalf of customers. The default should be showing for the future flights. Optionally you may include a way for the user to specify a range of dates, specify destination and/or source airport name and/or city name etc to show all the flights for which he/she purchased tickets.
5. Search for flights: Search for future flights (one way or round trip) based on source city/airport name, destination city/airport name, dates (departure or arrival).
6. Purchase tickets: Booking agent chooses a flight and purchases tickets for other customers giving customer information and payment information, providing all the needed data, via forms. You may find it easier to implement this along with a use case to search for flights.
7. View my commission: Default view will be total amount of commission received in the past 30 days and the average commission he/she received per ticket booked in the past 30 days and total number of tickets sold by him in the past 30 days. He/she will also have option to specify a range of dates to view total amount of commission received and total numbers of tickets sold.
8. View Top Customers: Top 5 customers based on number of tickets bought from the booking agent in the past 6 months and top 5 customers based on amount of commission received in the last year. Show a bar chart showing each of these 5 customers in x-axis and number of tickets bought in y-axis. Show another bar chart showing each of these 5 customers in x-axis and amount commission received in y-axis.
9. Logout: The session is destroyed and a “goodbye” page or the login page is displayed.
Airline Staff use cases:
After logging in successfully an airline staff may do any of the following use cases:
4. View My flights: Defaults will be showing all the future flights operated by the airline he/she works for the next 30 days. He/she will be able to see all the current/future/past flights operated by the airline he/she works for based range of dates, source/destination airports/city etc. He/she will be able to see all the customers of a particular flight.
5. Create new flights: He or she creates a new flight, providing all the needed data, via forms. The application should prevent unauthorized users from doing this action. Defaults will be showing all the future flights operated by the airline he/she works for the next 30 days.
6. Change Status of flights: He or she changes a flight status (from on-time to delayed or vice versa) via forms.
7. Add airplane in the system: He or she adds a new airplane, providing all the needed data, via forms. The application should prevent unauthorized users from doing this action. In the confirmation page, she/he will be able to see all the airplanes owned by the airline he/she works for.
8. Add new airport in the system: He or she adds a new airport, providing all the needed data, via forms. The application should prevent unauthorized users from doing this action.
9. View all the booking agents: Top 5 booking agents based on number of tickets sales for the past month and past year. Top 5 booking agents based on the amount of commission received for the last year.
10. View frequent customers: Airline Staff will also be able to see the most frequent customer within the last year. In addition, Airline Staff will be able to see a list of all flights a particular Customer has taken only on that particular airline.
11. View reports: Total amounts of ticket sold based on range of dates/last year/last month etc. Month wise tickets sold in a bar chart.
12. Comparison of Revenue earned: Draw a pie chart for showing total amount of revenue earned from direct sales (when customer bought tickets without using a booking agent) and total amount of revenue earned from indirect sales (when customer bought tickets using booking agents) in the last month and last year.
13. View Top destinations: Find the top 3 most popular destinations for last 3 months and last year.
14. Logout: The session is destroyed and a “goodbye” page or the login page is displayed.
Additional Requirements:
You should implement Air ticket reservation system as a web-based application. If you want to use a DBMS other than MySQL, SQLserver, Oracle, Mongodb or to use a programming language other than Python/Flask, Java/JDBC/Servlets, PHP, C#, node.js, or javascripts please check with me first. You will need to bring the host computer to the demo/test session at the end of the semester or make the application available remotely over the web.
Enforcing complex constraints: Your air ticket reservation system implementation should prevent users from doing actions they are not allowed to do. For example, system should prevent users who are not authorized to do so from adding flight information. This should be done by querying the database to check whether the user is an airline staff or not before allowing him to create the flight. You may also use the interface to help the user to avoid violating the constraints. However, you should not rely solely
on client-side interactions to enforce the constraint, since a user could bypass the client-side interface and send malicious http requests.
When a user logs in, a session should be initiated; relevant session variables should be stored. When the member logs out, the session should be terminated. Each component executed after the login component should authenticate the session and retrieve the user’s pid from a stored session variable. (If you’re using Python/Flask, you can follow the model in the Flask examples presented to do this.)
You must use prepared statements if your programming language supports them. (This is the style used in Flask; if you’re using PHP, use the MySQLi interface; if you’re using Java/JDBC, use the PreparedStmt class.) If your programming language does not support prepared statements, Free form inputs (i.e., text entered through text boxes) that is incorporated into SQL statements should be validated or cleaned to prevent SQL injection.
You should take measures to prevent cross-site scripting vulnerabilities, such as passing any text that comes from users through htmlspecialchars or some such function, before incorporating it into the html that air ticket reservation system produces.
The user interface should be usable, but it does not need to be fancy. For each type of users, you need to implement different home pages where you only show relevant use cases for that type of users and you should not show/combine all the use cases in one page.
For testing/debugging you will probably find it useful to execute your SQL queries directly through PHPmyAdmin (if you use MySQL) or using your database provided client program, before incorporating them in your application code.