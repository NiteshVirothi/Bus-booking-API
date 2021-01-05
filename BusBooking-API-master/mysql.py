import pymysql

cid = -1
'''NOTE: change password to your database password in the 3rd argument of pymysql.connect()'''
database = pymysql.connect('localhost', 'root', '')
database.autocommit(True)
db = database.cursor()

def initialise():
    '''
    initialise()
    :return: None

    Creates database if it doesn't exist
    '''

    db.execute("SHOW DATABASES")
    databases = db.fetchall()
    if ('BusBooking',) in databases:
        db.execute('USE BusBooking')
        return

    file = 'createdb.sql'
    with open(file, 'r') as queries_file:
        queries = queries_file.read()
        query = queries.split('--')
        for i in range(0, len(query), 2):
            new_query = query[i]
            new_query = new_query.replace('\n', ' ')
            new_query = new_query.replace('\t', ' ')
            if new_query == '' or 'delimiter' in new_query.lower(): continue
            try:
                db.execute(new_query)
            except:
                return


def signup(*user_signup):
    '''
    signup(*user_signup)
    :param user_signup: Tuple of all user data
    :return: None

    Inserts the user details into customer database
    '''
    if user_signup[-1] != user_signup[-2]:
        raise ValueError('passwords do not match')

    query = """
            insert into Customer(fname, lname, phone, email, username, password)
            values
            ('%s', '%s', '%s', '%s', '%s', '%s')""" % user_signup[:-1]
    db.execute(query)

def login(*credentials):
    '''
    login(*credentials)
    :param credentials: Tuple (username, password)
    :return: True if the username and password are correct, False if not.

    Used for authentication of user by passing the username and password
    '''
    query = """
            select * from Customer
            where username = '%s' and password = '%s'""" % credentials
    db.execute(query)
    data = db.fetchall()
    global cid
    query = """
            select cid from Customer
            where username = '%s'""" % (credentials[0])
    db.execute(query)
    cid = db.fetchall()[0][0]
    if len(data) == 1:
        return True
    return False

def get_all_source():
    query = """
            select distinct source from Route"""
    db.execute(query)
    source_data = db.fetchall()
    sources = [data[0] for data in source_data]
    return tuple(sources)

def get_all_destination():
    query = """
            select distinct destination from Route"""
    db.execute(query)
    destination_data = db.fetchall()
    destinations = [data[0] for data in destination_data]
    return tuple(destinations)

def book(sid, seat1 = None, seat2 = None):
    '''
    book(*booking_data, seat1 = None, seat2 = None)
    :param sid: service id
    :param seat1: no of first seat, not null
    :param seat2: no of second seat, optional
    :return: None

    Will insert the data into the booking table
    implies a ticket is booked by a person
    '''
    global cid
    if seat2 == None:
        query = """
                insert into Booking(cid, sid, seat1)
                values
                (%s, %s, %s)""" % (cid, sid, seat1)
    else:
        query = """
                insert into Booking
                values
                (%s, %s, %s, %s)""" % (cid, sid, seat1, seat2)

    db.execute(query)

def search_bus(source, destination, day):
    '''
    search_bus(source, destination, day)
    :param source: The starting location of the bus
    :param destination: The destination location of the bus
    :param day: The day of the service
    :return: Tuple of all busses in accordance with the input data

    this func will search all the busses for the given criteria
    '''
    query = """
            select S.* from Service S, Route R
            where R.source = '%s' and R.destination = '%s'
            and R.rno = S.rno and S.%s = 'Y'""" % (source, destination, day)
    db.execute(query)
    busses = db.fetchall()
    return busses

def get_booking_data(sid):
    '''
    get_booking_data(sid)
    :param sid: the service id to retrieve booking data
    :return: list of all booking data

    Returns all the booked seats for a given sid
    '''
    query = """select seat1, seat2 from Booking where sid = %s""" % (sid)
    db.execute(query)
    booking_data = db.fetchall()

    booked_seats = []
    for seats in booking_data:
        for seat in seats:
            if type(seat).__name__ != 'int': continue
            booked_seats.append(seat)

    return set(booked_seats)

initialise()
