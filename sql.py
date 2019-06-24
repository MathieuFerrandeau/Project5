import mysql.connector
from mysql.connector import errorcode 
from config import * 

class Sql:
    """   """

    def __init__(self, user, password, host):
        self.user = str(user)
        self.password = str(password)
        self.host = str(host)
        

    def create_db(self, database):
        cnx = self.connect_db()
        cursor = cnx.cursor()
        self.database = str(database)
        try:
            cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
            print("Database {} created successfully.".format(DB_NAME))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)
       

    def connect_db(self):
        """ se connecte a la db"""
        try:
            cnx = mysql.connector.connect(
                user = self.user,
                password = self.password,
                host = self.host
                )
            return cnx

        except mysql.connector.errors.ProgrammingError:
            return False

    def create_tables(self):
        """ """
        cnx = self.connect_db()
        cursor = cnx.cursor()
        use_db = ("USE {}".format(DB_NAME))
        cursor.execute(use_db)

      
        TABLES = {}
        TABLES['Category'] = (
            "CREATE TABLE `Category` ("
            "  `id` smallint(3) NOT NULL AUTO_INCREMENT," 
            "  `name` varchar(50) NOT NULL,"
            "  PRIMARY KEY (`id`)"
            ") ENGINE=InnoDB")

        TABLES['Product'] = (
            "CREATE TABLE `Product` ("
            "  `id` smallint(3) NOT NULL AUTO_INCREMENT,"
            "  `name` varchar(200) NOT NULL,"
            "  `store` varchar(100) NOT NULL,"
            "  `link` text NOT NULL,"
            "  `nutriscore` varchar(100) NOT NULL,"
            "  `category` smallint(3) NOT NULL,"
            "  PRIMARY KEY (`id`),"
            "  CONSTRAINT `fk_product` FOREIGN KEY (`category`) REFERENCES `Category`(`id`) ON DELETE CASCADE ON UPDATE CASCADE"
            ") ENGINE=InnoDB")

        TABLES['Substitute'] = (
            "CREATE TABLE `Substitute` ("
            "  `id` smallint(3) NOT NULL AUTO_INCREMENT,"
            "  `id_product_to_substitute` smallint(3) NOT NULL,"
            "  `id_substitute_product` smallint(3) NOT NULL,"
            "  PRIMARY KEY (`id`),"
            "  CONSTRAINT `fk_substitute_product` FOREIGN KEY (`id_substitute_product`) REFERENCES `Product`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,"
            "  CONSTRAINT `fk_product_to_substitute` FOREIGN KEY (`id_product_to_substitute`) REFERENCES `Product`(`id`) ON DELETE CASCADE ON UPDATE CASCADE"
            ") ENGINE=InnoDB")


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
