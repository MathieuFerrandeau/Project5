import mysql.connector
from mysql.connector import errorcode
import requests
from config import *
from sql import * 

try:
    cnx = mysql.connector.connect(**FIELDS)
    cursor = cnx.cursor() 

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    pass

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


def create_tables():
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

def insert_category():
    res = requests.get("https://fr.openfoodfacts.org/categories&json=1")
    data_json = res.json()
    data_tags = data_json.get('tags')
    data_cat = [d.get('name') for d in data_tags]
    i = 2
    while i < 12:
        cursor = cnx.cursor()
        add_category = ("INSERT INTO Category" "(name)" "VALUES('{}')".format(data_cat[i]))
        try: 
            print("Creating Category: {}.".format(data_cat[i]))
            cursor.execute(add_category)
            cnx.commit()
            cursor.close()
            i=i+1
        except:
            print(err.msg)

def get_food(nb_fd):
    for i in range(1,6):
        nb_ini_cat = i
        nb_food = nb_fd
        cursor = cnx.cursor(buffered=True)
        cat_nb_1 = str(nb_ini_cat)
        selec_cat = ("SELECT name FROM Category WHERE id = "+cat_nb_1)
        cursor.execute(selec_cat)
        cat_saved = str(cursor.fetchone()[0]) #indexation
        payload = {
        'action': 'process',
        'tagtype_0': 'categories', #which subject is selected (categories)
        'tag_contains_0': 'contains', #contains or not
        'tag_0': '{}'.format(cat_saved), #parameters to choose
        'sort_by': 'unique_scans_n',
        'page_size': '{}'.format(nb_food),
        'countries': 'France',
        'json': 1,
        'page': 1
        }
        r_food = requests.get('https://fr.openfoodfacts.org/cgi/search.pl', params=payload)
        food_json = r_food.json()
        test2 = food_json.get('products') 
        

        food_id = ("SELECT id FROM Category WHERE id = "+cat_nb_1)
        cursor.execute(food_id)
        food_id_saved = cursor.fetchone()[0]
    
        for x in range(nb_food) :

            prod_name_saved = [d.get('product_name_fr') for d in test2] #get product name in french
            name = str(prod_name_saved[x])
            store_saved = [d.get('stores') for d in test2]
            store = str(store_saved[x])
            link_saved = [d.get('url') for d in test2] #get ingredients list in french
            link = str(link_saved[x])
            nutri_grd_saved = [d.get('nutrition_grade_fr') for d in test2] #get nutrigrade
            nutri_grd = str(nutri_grd_saved[x])
            #bar_code_saved = [d.get('id') for d in test2] #get barcode
            #category = bar_code_saved[x]
            add_food =(
                "INSERT INTO Product"
                "(name, store, link, nutriscore, category)"
                "VALUES (%s, %s, %s, %s, %s)")
            data = (name, store, link, nutri_grd, cat_nb_1)
            cursor.execute(add_food, data)
            cnx.commit()
        cursor.close()

create_tables()
insert_category()
get_food(5)