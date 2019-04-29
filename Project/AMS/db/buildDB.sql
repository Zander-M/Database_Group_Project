create table Airline_Staff{
    username varchar(30) not null,
    password char(40) not null,
    first_name varchar(20) not null,
    last_name varchar(20) not null,
    date_of_birth date not null,
    airline_name references Airline(name) not null,
    primary key(username)  
};

create table Airline{
    name varchar(30),
    primary key(name)
};

create table A2AS{
    
}