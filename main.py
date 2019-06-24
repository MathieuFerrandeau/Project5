import mysql.connector
from mysql.connector import errorcode 
from config import * 
from sql import * 
from collect_data import *


def main():
	sql = Sql(FIELDS['user'],FIELDS['password'],FIELDS['host'])
	data = CollectData()

	sql.create_db(DB_NAME)
	sql.create_tables()
	data.insert_category()
	data.get_food(10)


main()