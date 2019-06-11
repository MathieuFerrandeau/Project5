import mysql.connector
from mysql.connector import errorcode 

DB_NAME = 'test10'
config = {
	
	'user': 'xxx', 
	'password': 'xxx',
    'host':'localhost',
    #'database':'test10',
    'raise_on_warnings': True
}

TABLES = {}
TABLES['category'] = (
    "CREATE TABLE `category` ("
    "  `id` smallint(3) NOT NULL AUTO_INCREMENT,"
    "  `name` varchar(50) NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

TABLES['product'] = (
    "CREATE TABLE `product` ("
    "  `id` smallint(3) NOT NULL AUTO_INCREMENT,"
    "  `name` varchar(200) NOT NULL,"
    "  `store` varchar(100) NOT NULL,"
    "  `link` text NOT NULL,"
    "  `nutriscore` varchar(1) NOT NULL,"
    "  `category` smallint(3) NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "  CONSTRAINT `fk_product` FOREIGN KEY (`category`) REFERENCES `category`(`id`) ON DELETE CASCADE ON UPDATE CASCADE"
    ") ENGINE=InnoDB")

TABLES['substitute'] = (
    "CREATE TABLE `substitute` ("
    "  `id` smallint(3) NOT NULL AUTO_INCREMENT,"
    "  `id_product_to_substitute` smallint(3) NOT NULL,"
    "  `id_substitute_product` smallint(3) NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "  CONSTRAINT `fk_substitute_product` FOREIGN KEY (`id_substitute_product`) REFERENCES `product`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,"
    "  CONSTRAINT `fk_product_to_substitute` FOREIGN KEY (`id_product_to_substitute`) REFERENCES `product`(`id`) ON DELETE CASCADE ON UPDATE CASCADE"
    ") ENGINE=InnoDB")

try:
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor() 

except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
    print('good')

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

cursor.close()
cnx.close()