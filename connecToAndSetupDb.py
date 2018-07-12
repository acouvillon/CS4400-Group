from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode

config = {
  'user': 'root',
  'password': 'De5hNeh@',
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

for name, ddl in TABLES.items():
    try:
        print("Creating table {}: ".format(name), end='')
       cursor.execute(ddl)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
       else:
            print(err.msg)
    else:
        print("OK")

add_admin = ("INSERT INTO admin_user "
               "VALUES (%s, %s)")
add_visitor = ("INSERT INTO visitor "
                   "VALUES (%s, %s, %s, %s, %s, %s)")
add_museum = ("INSERT INTO museum "
                  "VALUES(%s, %s)")
#---------------------------ADMIN DATA----------------------------------
data_admin = ('very_cool_guy@hotmail.com', 'imcool')
# Insert new admin
cursor.execute(add_admin, data_admin)

#--------------------------VISITOR DATA----------------------------------
# email, password, credit card num, expiry month, expiry year, security num
data_visitor = []
data_visitor.append(('themuseumguy@gmail.com', 'themuseumguy', '1111222233334444', 12, '1999', 666)) 
for v in range(len(data_visitor)):
    cursor.execute(add_visitor, data_visitor[v])
    print("visitor added...")
    v += 1

#--------------------------MUSEUM DATA-----------------------------------
# museum name, curator email (optional)
data_museum = []

#-------------------------CURATOR REQUEST DATA---------------------------
# email, museum name
data_curator_request = []


#-------------------------REVIEW DATA------------------------------------
# email, museum name, comment (optional), rating
data_review = []

#-------------------------TICKET DATA------------------------------------
# email, museum name, price, purchase_timestamp
data_ticket = []

#-------------------------EXHIBIT DATA-----------------------------------
# museum name, exhibit name, year, url
data_exhibit = []

# Make sure data is committed to the database
cnx.commit()
cursor.close()
cnx.close()
