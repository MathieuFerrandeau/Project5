"""Class to create and connect to the database"""

import mysql.connector
from config import DB_NAME

class Sql:
    """Create and use tje database"""

    def __init__(self, user, password, host):
        self.user = str(user)
        self.password = str(password)
        self.host = str(host)

    def create_db(self, database):
        """Create the database"""
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
        """Etablsih the connection to the database"""
        try:
            cnx = mysql.connector.connect(
                user=self.user,
                password=self.password,
                host=self.host
                )
            return cnx

        except mysql.connector.errors.ProgrammingError:
            return False

    def create_tables(self):
        """Create tables in database"""
        cnx = self.connect_db()
        cursor = cnx.cursor()
        use_db = ("USE {}".format(DB_NAME))
        cursor.execute(use_db)

        try:
            with open('createdb.sql', 'r') as file:
                query = file.read()
            cursor.execute(query)
            cursor.close()

        except:
            pass
    