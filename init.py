"""Class allowing the creation of the database with an argument"""
import argparse
from collect_data import CollectData
from sql import Sql
from config import FIELDS, DB_NAME

class Init:
    """Takes care of creating and filling the db"""
    def __init__(self):
        pass

    def init_db(self):
        """Uses class methods to create and fill the DB"""
        sql = Sql(**FIELDS)
        sql.create_db(DB_NAME)
        sql.create_tables()
        data = CollectData()
        data.insert_category()
        data.get_food(20)

    def arg(self):
        """ADD the --init argument"""
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--init", "-i", action="store_true", help="Initialise the DB with -i or --init"
        )
        args = parser.parse_args()

        if args.init:
            self.init_db()
            return True
