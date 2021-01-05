-- Create Database --
create database BusBooking;
-- Navigating to Database --
use BusBooking;
-- Creating Bus Table --
create table Bus (
    bid integer primary key,
    bno varchar(10) unique not null,
    btype varchar(10) not null
);
-- Creating Routes Table --
create table Route (
    rno integer primary key,
    source varchar(30) not null,
    destination varchar(30) not null
);
-- Create Relation b/w bus and routes --
create table Service (
    sid integer auto_increment primary key,
    bid integer not null,
    rno integer not null,
    source_time time not null,
    destination_time time not null,
    sunday char(1),
    monday char(1),
    tuesday char(1),
    wednesday char(1),
    thursday char(1),
    friday char(1),
    saturday char(1)
);
-- Adding foreign keys --
alter table Service
add constraint bus_fk foreign key(bid) references Bus(bid),
add constraint rno_fk foreign key(rno) references Route(rno);
-- Creating Customer table --
create table Customer (
    cid integer auto_increment primary key,
    fname varchar(30) not null,
    lname varchar(30) not null,
    phone varchar(10) not null,
    email varchar(30),
    username varchar(20) unique not null,
    password varchar(20) not null
);
-- Creating Booking Table --
create table Booking (
    cid integer not null,
    sid integer not null,
    seat1 integer not null,
    seat2 integer
);
-- Adding foreign keys --
alter table Booking
add constraint cid_fk_ foreign key(cid) references Customer(cid),
add constraint sid_fk_ foreign key(sid) references Service(sid);