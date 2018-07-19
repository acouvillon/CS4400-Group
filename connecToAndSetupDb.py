from __future__ import print_function
import time
import datetime
import mysql.connector
from mysql.connector import errorcode

config = {
  'user': 'root',
  'password': 'rootuserpassword',
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

#Creating user types

TABLES = {}

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

TABLES['museum'] = (
    "CREATE TABLE `museum` ("
    "`museum_name` VARCHAR(100) NOT NULL,"
    "`curator_email` VARCHAR(100),"
    "`ticket_price` VARCHAR(140) NULL,"
    "PRIMARY KEY (`museum_name`),"
    "CONSTRAINT `FK_email` FOREIGN KEY (`curator_email`)"
    "REFERENCES `visitor` (`email`) ON DELETE CASCADE"
    ") ENGINE=InnoDB;")

TABLES['admin_user'] = (
    "CREATE TABLE `admin_user` ("
    "  `email` VARCHAR(100) NOT NULL,"
    "  `password` VARCHAR(100) NOT NULL,"
    "  PRIMARY KEY (`email`)"
    ") ENGINE=InnoDB")

TABLES['curator_request'] = (
    "CREATE TABLE `curator_request` ("
    "  `email` VARCHAR(100) NOT NULL,"
    "  `museum_name` VARCHAR(100) NOT NULL,"
    "  PRIMARY KEY (`museum_name`,`email`),"
    "  CONSTRAINT `FK_email_id` FOREIGN KEY (`email`) "
    "     REFERENCES `visitor` (`email`) ON DELETE CASCADE,"
    "  CONSTRAINT `FK_museum_name` FOREIGN KEY (`museum_name`) "
    "     REFERENCES `museum` (`museum_name`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

TABLES['review'] = (
    "  CREATE TABLE `review` ("
    "  `email` VARCHAR(100) NOT NULL,"
    "  `museum_name` VARCHAR(100) NOT NULL,"
    "  `comment` VARCHAR(140) NULL,"
    "  `rating` INT NOT NULL,"
    "  PRIMARY KEY (`email`,`museum_name`),"
    "  CONSTRAINT `FK_visitor_email` FOREIGN KEY (`email`) "
    "     REFERENCES `visitor` (`email`) ON DELETE CASCADE,"
    "  CONSTRAINT `FK_name_museum` FOREIGN KEY (`museum_name`) "
    "     REFERENCES `museum` (`museum_name`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

TABLES['ticket'] = (
    "CREATE TABLE `ticket` ("
    "  `email` VARCHAR(100) NOT NULL,"
    "  `museum_name` VARCHAR(100) NOT NULL,"
    "  `price` VARCHAR(140) NULL,"
    "  `purchase_timestamp` DATETIME,"
    "  PRIMARY KEY (`email`,`museum_name`),"
    "  CONSTRAINT `FK_email_visitor` FOREIGN KEY (`email`)"
    "     REFERENCES `visitor` (`email`),"
    "  CONSTRAINT `FK_mu_name` FOREIGN KEY (`museum_name`)"
    "     REFERENCES `museum` (`museum_name`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

TABLES['exhibit'] = (
    "CREATE TABLE `exhibit` ("
    "  `museum_name` VARCHAR(100) NOT NULL,"
    "  `exhibit_name` VARCHAR(100) NOT NULL,"
    "  `year` INT,"
    "  `url` VARCHAR(100),"
    "  PRIMARY KEY (`museum_name`,`exhibit_name`),"
    "  CONSTRAINT `FK_museumname` FOREIGN KEY (`museum_name`)"
    "     REFERENCES `museum` (`museum_name`) ON DELETE CASCADE"
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
                  "VALUES(%s, %s, %s)")
add_curator_request = ("INSERT INTO curator_request "
                           "VALUES (%s, %s)")
add_review = ("INSERT INTO review "
                  "VALUES(%s, %s, %s, %s)")
add_ticket = ("INSERT INTO ticket "
                  "VALUES (%s, %s, %s, %s)")
add_exhibit = ("INSERT INTO exhibit "
                   "VALUES (%s, %s, %s, %s)")
#---------------------------ADMIN DATA----------------------------------
data_admin = ('alex@gatech.edu', 'iamadmin')
#Insert new admin
cursor.execute(add_admin, data_admin)

#--------------------------VISITOR DATA----------------------------------
# email, password, credit card num, expiry month, expiry year, security num
data_visitor = []
data_visitor.append(('themuseumguy@gmail.com', 'themuseumguy', '1111222233334444', 12, '1999', 666))
data_visitor.append(('daniel@gatech.edu', 'bilingual', '1234567812345670', 1, '2020', 123))
data_visitor.append(('helen@gatech.edu', 'architecture4ever', '8765432187654320', 2, '2021', 456))
data_visitor.append(('zoe@gatech.edu', 'yogasister', '2468135924681350', 3, '2022', 789))
data_visitor.append(('bobross@iliketopaint.com', 'treesrgr8', '1234543212345432', 1, '1995', 606))
data_visitor.append(('spiderman@webdesign.org', 'spidey', '9119119119119115', 8, '1962', 888))
data_visitor.append(('bruce@thetrickster.gov', 'canada', '1234567891011123', 4, '1967', 112))
data_visitor.append(('charlie@aol.net', 'shrek', '6786786786786785', 6, '1999', 333))
data_visitor.append(('abby@deathstar.gov', 'ihatesand', '8888888888888888', 7, '1998', 555))
data_visitor.append(('kristin@grapes.com', 'grapeybois', '4444444444444444', 4, '1998', 222))
data_visitor.append(('neha@easy.com', 'easy', '1111111111111111', 3, '1999', 999))
data_visitor.append(('jake@grayshirt.net', 'gray', '9999999999999999', 12, '1998', 100))
data_visitor.append(('kieraknighley@pnp.org', 'darcy', '6666666666666666', 2, '2006', 777))
data_visitor.append(('gtcoc@leaked.com', 'spreadsheet', '8888888888888888', 7, '2018', 333))
data_visitor.append(('daisha@unquenchablethirst.com', 'thirsty', '2222222222222222', 5, '2055', 123))
data_visitor.append(('ashwini@vlog.org', 'vlog', '3333333333333333', 1, '2023', 111))
data_visitor.append(('angi@travel.gov', 'sandals', '5555555555555555', 10, '3040', 543))
data_visitor.append(('jackson@hotmail.com', 'hott1e', '8675309986753099', 1, '1998', 770))
data_visitor.append(('sam@inthetank.org', 'swim', '7777777777777777', 8, '2017', 234))
data_visitor.append(('georgepburdell@gatech.edu', 'stealthets', '8585858585858585', 8, '1927', 998))


for v in range(len(data_visitor)):
    cursor.execute(add_visitor, data_visitor[v])
    print("visitor added...")
    v += 1
cursor.execute(add_visitor, ('abc', 'abc', '123', 1, '2033', 222))

#--------------------------MUSEUM DATA-----------------------------------
# museum name, curator email (optional)
data_museum = []
data_museum.append(('MACBA', 'zoe@gatech.edu', '5'))
data_museum.append(('Picasso Museum', None, '10'))
data_museum.append(('CCCB', 'helen@gatech.edu', '4'))
data_museum.append(('Miro Museum', 'themuseumguy@gmail.com', '5'))
data_museum.append(('Muhba Museum', 'themuseumguy@gmail.com', '15'))
data_museum.append(('Catalunya Museum', None, '12'))
data_museum.append(('Can Framis Museum', None, '11'))
for v in range(len(data_museum)):
    cursor.execute(add_museum, data_museum[v])
    print("museum added...")
    v += 1

#-------------------------CURATOR REQUEST DATA---------------------------
# email, museum name
data_curator_request = []
data_curator_request.append(('zoe@gatech.edu', 'Picasso Museum'))
for v in range(len(data_curator_request)):
    cursor.execute(add_curator_request, data_curator_request[v])
    print("curator_request added...")
    v += 1

#-------------------------REVIEW DATA------------------------------------
# email, museum name, comment (optional), rating
data_review = []
data_review.append(('zoe@gatech.edu', 'MACBA', 'Didn\'t get it', 1))
data_review.append(('helen@gatech.edu', 'Picasso Museum', 'So many shapes!', 5))
data_review.append(('helen@gatech.edu', 'CCCB', 'Scary, but cool', 3))
for v in range(len(data_review)):
    cursor.execute(add_review, data_review[v])
    print("review added...")
    v += 1


#-------------------------TICKET DATA------------------------------------
# email, museum name, price, purchase_timestamp
data_ticket = []
data_ticket.append(('zoe@gatech.edu', 'MACBA', 5, '2018-05-20'))
data_ticket.append(('helen@gatech.edu', 'Picasso Museum', 20, '2018-06-11'))
data_ticket.append(('helen@gatech.edu', 'CCCB', 20, '2018-06-29'))
for v in range(len(data_ticket)):
    cursor.execute(add_ticket, data_ticket[v])
    print("ticket added...")
    v += 1

#-------------------------EXHIBIT DATA-----------------------------------
# museum name, exhibit name, year, url
data_exhibit = []
data_exhibit.append(('MACBA', 'Bird', '2018', 'www.macba.es/bird/'))
data_exhibit.append(('MACBA', 'Plane', '2018', 'www.macba.es/plane/'))
data_exhibit.append(('MACBA', 'Train', '2018', 'www.macba.es/train/'))
data_exhibit.append(('Picasso Museum', 'Geometric Shapes', '1900', 'www.picassomuseo.com/geo/'))
data_exhibit.append(('CCCB', 'Black Light 1', '1985', 'www.cccb.com/bl1'))
data_exhibit.append(('CCCB', 'Black Light 2', '1986', 'www.cccb.com/bl2'))
data_exhibit.append(('Miro Museum', 'Shipwrecked Species', '2017', 'https://www.fmirobcn.org/en/exhibitions/5731/shipwrecked-species'))
data_exhibit.append(('Miro Museum', 'Non-Slave Tenderness', '2018', 'https://www.fmirobcn.org/en/exhibitions/5733/non-slave-tenderness'))
data_exhibit.append(('Miro Museum', 'The Odyssey', '2018', 'https://www.fmirobcn.org/en/exhibitions/5734/the-odyssey'))
data_exhibit.append(('Picasso Museum', 'Picasso\'s Kitchen', '2018', 'http://www.bcn.cat/museupicasso/en/exhibitions/picasso-kitchen/exhibition.html'))
data_exhibit.append(('Picasso Museum', 'Picasso Discovers Paris', '2018', 'http://www.bcn.cat/museupicasso/en/exhibitions/picasso-discovers-paris.html'))
data_exhibit.append(('Picasso Museum', 'Picasso in Barcelona', '2017', 'http://www.bcn.cat/museupicasso/en/exhibitions/1917-picasso-barcelona/'))
data_exhibit.append(('Muhba Museum', '40 anys fent l\'Ateneu Popular 9 Barris', '1977', 'http://ajuntament.barcelona.cat/museuhistoria/en/'))
data_exhibit.append(('Muhba Museum', 'El port franc i la fàbrica de Barcelona.', '1977', 'http://ajuntament.barcelona.cat/museuhistoria/en/2'))
data_exhibit.append(('Catalunya Museum', 'Gala Salvador Dali. A Room of One\'s Own In Pubol', '2018', 'http://www.museunacional.cat/en/gala-dali'))
data_exhibit.append(('Catalunya Museum', 'Torres-Garcia at his Crossroads', '2011', 'http://www.museunacional.cat/en/torres-garcia-his-crossroads'))
data_exhibit.append(('Catalunya Museum', 'The Journey to Spain of Alexandre de Laborde', '2006', 'http://www.museunacional.cat/en/journey-spain-alexandre-de-laborde'))
data_exhibit.append(('Can Framis Museum', 'Relato cartográfico', '2018', 'http://www.fundaciovilacasas.com/en/exhibition/relato-cartografico'))
data_exhibit.append(('Can Framis Museum', 'Hiberticer', '2018', 'http://www.fundaciovilacasas.com/en/exhibition/hiberticer'))
data_exhibit.append(('Can Framis Museum', 'Non-Slave Tenderness', '2017', ''))
data_exhibit.append(('Miro Museum', 'Frank Horvat - Please don’t smile. Homenaje en el 90 aniversario', '2018', 'http://www.fundaciovilacasas.com/en/exhibition/please-dont-smile-homenaje-en-el-90-aniversario'))
for v in range(len(data_exhibit)):
    cursor.execute(add_exhibit, data_exhibit[v])
    print("exhibit added...")
    v += 1

# Make sure data is committed to the database
cnx.commit()
cursor.close()
cnx.close()
