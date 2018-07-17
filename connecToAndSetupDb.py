from __future__ import print_function
import time
import datetime
import mysql.connector
from mysql.connector import errorcode

config = {
  'user': 'root',
  'password': 'INSERT YOUR PASSWORD HERE',
  'database': 'bmtrsdb',
  'raise_on_warnings': True,
}

cnx = mysql.connector.connect(**config)
DB_NAME = 'bmtrsdb'

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cnx.database = DB_NAME  
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)


TABLES = {}

TABLES['museum'] = (
    "CREATE TABLE `museum` ("
    "`museum_name` VARCHAR(100) NOT NULL,"
    "`curator_email` VARCHAR(100),"
    "PRIMARY KEY (`museum_name`),"
    "FOREIGN KEY (`curator_email`)"
    "REFERENCES `visitor` (`email`)"
    ") ENGINE=InnoDB;")

 

TABLES['admin_user'] = (
    "CREATE TABLE `admin_user` ("
    "  `email` VARCHAR(100) NOT NULL,"
    "  `password` VARCHAR(100) NOT NULL,"
    "  PRIMARY KEY (`email`)"
    ") ENGINE=InnoDB")

TABLES['visitor'] = (
    "CREATE TABLE `visitor` ("
    "  `email` VARCHAR(100) NOT NULL,"
    "  `password` VARCHAR(100) NOT NULL,"
    "  `credit_card_num` CHAR(16) NOT NULL,"
    "  `expiration_month` INT NOT NULL,"
    "  `expiration_year` CHAR(4) NOT NULL,"
    "  `credit_card_security_num` INT NOT NULL,"
    "  PRIMARY KEY (`email`)"
    ") ENGINE=InnoDB")

TABLES['curator_request'] = (
    "CREATE TABLE `dept_emp` ("
    "  `email` VARCHAR(100) NOT NULL,"
    "  `museum_name` VARCHAR(100) NOT NULL,"
    "  PRIMARY KEY (`museum_name`,`email`),"
    "  FOREIGN KEY (`email`) "
    "     REFERENCES `visitor` (`email`) ON DELETE NO ACTION,"
    "  FOREIGN KEY (`museum_name`) "
    "     REFERENCES `museum` (`museum_name`) ON DELETE NO ACTION"
    ") ENGINE=InnoDB")

TABLES['review'] = (
    "  CREATE TABLE `review` ("
    "  `email` VARCHAR(100) NOT NULL,"
    "  `museum_name` VARCHAR(100) NOT NULL,"
    "  `comment` VARCHAR(140) NULL,"
    "  `rating` INT NOT NULL,"
    "  PRIMARY KEY (`email`,`museum_name`),"
    "  FOREIGN KEY (`email`) "
    "     REFERENCES `visitor` (`email`) ON DELETE NO ACTION,"
    "  FOREIGN KEY (`museum_name`) "
    "     REFERENCES `museum` (`museum_name`) ON DELETE NO ACTION"
    ") ENGINE=InnoDB")

TABLES['ticket'] = (
    "CREATE TABLE `ticket` ("
    "  `email` VARCHAR(100) NOT NULL,"
    "  `museum_name` VARCHAR(100) NOT NULL,"
    "  `price` VARCHAR(140) NULL,"
    "  `purchase_timestamp` DATETIME,"
    "  PRIMARY KEY (`email`,`museum_name`),"
    "  FOREIGN KEY (`email`)"
    "     REFERENCES `visitor` (`email`),"
    "  FOREIGN KEY (`museum_name`)"
    "     REFERENCES `museum` (`museum_name`)"
    ") ENGINE=InnoDB")

TABLES['exhibit'] = (
    "CREATE TABLE `exhibit` ("
    "  `museum_name` VARCHAR(100) NOT NULL,"
    "  `exhibit_name` VARCHAR(100) NOT NULL,"
    "  `year` INT,"
    "  `url` VARCHAR(100),"
    "  PRIMARY KEY (`museum_name`,`exhibit_name`),"
    "  FOREIGN KEY (`museum_name`)"
    "     REFERENCES `museum` (`museum_name`)"
    ") ENGINE=InnoDB")


cursor = cnx.cursor()

#for name, ddl in TABLES.items():
#    try:
#        print("Creating table {}: ".format(name), end='')
#       cursor.execute(ddl)
#    except mysql.connector.Error as err:
#        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
#            print("already exists.")
#       else:
#            print(err.msg)
#    else:
#        print("OK")

add_admin = ("INSERT INTO admin_user "
               "VALUES (%s, %s)")
add_visitor = ("INSERT INTO visitor "
                   "VALUES (%s, %s, %s, %s, %s, %s)")
add_museum = ("INSERT INTO museum "
                  "VALUES(%s, %s)")
add_curator_request = ("INSERT INTO curator_request "
                           "VALUES (%s, %s)")
add_review = ("INSERT INTO review "
                  "VALUES(%s, %s, %s, %s)")
add_ticket = ("INSERT INTO ticket "
                  "VALUES (%s, %s, %s, %s)")
add_exhibit = ("INSERT INTO exhibit "
                   "VALUES (%s, %s, %s, %s)")
#---------------------------ADMIN DATA----------------------------------
#data_admin = ('alex@gatech.edu', 'iamadmin')
# Insert new admin
#cursor.execute(add_admin, data_admin)

#--------------------------VISITOR DATA----------------------------------
# email, password, credit card num, expiry month, expiry year, security num
data_visitor = []
#data_visitor.append(('themuseumguy@gmail.com', 'themuseumguy', '1111222233334444', 12, '1999', 666)) 
#data_visitor.append(('daniel@gatech.edu', 'bilingual', '1234567812345670', 1, '2020', 123))
#data_visitor.append(('helen@gatech.edu', 'architecture4ever', '8765432187654320', 2, '2021', 456))
#data_visitor.append(('zoe@gatech.edu', 'yogasister', '2468135924681350', 3, '2022', 789))
#for v in range(len(data_visitor)):
#    cursor.execute(add_visitor, data_visitor[v])
#    print("visitor added...")
#    v += 1

#--------------------------MUSEUM DATA-----------------------------------
# museum name, curator email (optional)
data_museum = []
#data_museum.append(('MACBA', 'zoe@gatech.edu'))
#data_museum.append(('Picasso Museum', None))
#data_museum.append(('CCCB', 'helen@gatech.edu'))
#for v in range(len(data_museum)):
#    cursor.execute(add_museum, data_museum[v])
#    print("museum added...")
#    v += 1
    
#-------------------------CURATOR REQUEST DATA---------------------------
# email, museum name
data_curator_request = []
#data_curator_request.append(('zoe@gatech.edu', 'Picasso Museum'))
#for v in range(len(data_curator_request)):
#    cursor.execute(add_curator_request, data_curator_request[v])
#   print("curator_request added...")
#    v += 1

#-------------------------REVIEW DATA------------------------------------
# email, museum name, comment (optional), rating
data_review = []
#data_review.append(('zoe@gatech.edu', 'MACBA', 'Didn\'t get it', 1))
#data_review.append(('helen@gatech.edu', 'Picasso Museum', 'So many shapes!', 5))
#data_review.append(('helen@gatech.edu', 'CCCB', 'Scary, but cool', 3))
#for v in range(len(data_review)):
#    cursor.execute(add_review, data_review[v])
#    print("review added...")
#    v += 1

#-------------------------TICKET DATA------------------------------------
# email, museum name, price, purchase_timestamp
data_ticket = []
#data_ticket.append(('zoe@gatech.edu', 'MACBA', 5, '2018-05-20'))
#data_ticket.append(('helen@gatech.edu', 'Picasso Museum', 20, '2018-06-11'))
#data_ticket.append(('helen@gatech.edu', 'CCCB', 20, '2018-06-29'))
#for v in range(len(data_ticket)):
#    cursor.execute(add_ticket, data_ticket[v])
#    print("ticket added...")
#    v += 1
#-------------------------EXHIBIT DATA-----------------------------------
# museum name, exhibit name, year, url
data_exhibit = []
#data_exhibit.append(('MACBA', 'Bird', '2018', 'www.macba.es/bird/'))
#data_exhibit.append(('MACBA', 'Plane', '2018', 'www.macba.es/plane/'))
#data_exhibit.append(('MACBA', 'Train', '2018', 'www.macba.es/train/'))
#data_exhibit.append(('Picasso Museum', 'Geometric Shapes', '1900', 'www.picassomuseo.com/geo/'))
#data_exhibit.append(('CCCB', 'Black Light 1', '1985', 'www.cccb.com/bl1'))
#data_exhibit.append(('CCCB', 'Black Light 2', '1986', 'www.cccb.com/bl2'))
#for v in range(len(data_exhibit)):
#   cursor.execute(add_exhibit, data_exhibit[v])
#    print("exhibit added...")
#    v += 1

# Make sure data is committed to the database
cnx.commit()
cursor.close()
cnx.close()
