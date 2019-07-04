"""Class that retrieves the data from the API and insert them into the db"""
import mysql.connector
import requests
from config import FIELDS, DB_NAME

class CollectData:
    """Takes care of recovering data from OpenFoodFact and inserting them into the database"""

    def __init__(self):
        self.cnx = mysql.connector.connect(**FIELDS, database=DB_NAME)

    def insert_category(self):
        """Picks up categories and insert 10"""
        res = requests.get("https://fr.openfoodfacts.org/categories&json=1")
        data_json = res.json()
        data_tags = data_json.get('tags')
        data_cat = [d.get('name') for d in data_tags]
        i = 2
        while i < 12:
            cursor = self.cnx.cursor()
            add_category = ("INSERT INTO Category" "(name)" "VALUES('{}')".format(data_cat[i]))
            try:
                print("Creating Category: {}.".format(data_cat[i]))
                cursor.execute(add_category)
                self.cnx.commit()
                cursor.close()
                i = i+1
            except:
                print("An error occurred while creating categories")

    def get_food(self, nb_fd):
        """Recovers the number of products given in parameter"""
        for i in range(1, 11):
            nb_ini_cat = i
            nb_food = nb_fd
            cursor = self.cnx.cursor(buffered=True)
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

            for j in range(nb_food):
                prod_name_saved = [d.get('product_name_fr') for d in test2]
                name = str(prod_name_saved[j])
                store_saved = [d.get('stores') for d in test2]
                store = str(store_saved[j])
                link_saved = [d.get('url') for d in test2] #get ingredients list in french
                link = str(link_saved[j])
                nutri_grd_saved = [d.get('nutrition_grade_fr') for d in test2] #get nutrigrade
                nutri_grd = str(nutri_grd_saved[j])
                add_food = (
                    "INSERT INTO Product"
                    "(name, store, link, nutriscore, category)"
                    "VALUES (%s, %s, %s, %s, %s)")
                data = (name, store, link, nutri_grd, cat_nb_1)
                cursor.execute(add_food, data)
                self.cnx.commit()
            cursor.close()
        print("Products added.")
