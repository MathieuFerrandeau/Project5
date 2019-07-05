"""Manages interaction with user and parse data"""
import mysql.connector
from config import FIELDS, DB_NAME


class Program:
    """This Class manages the interaction between the user and the console """
    def __init__(self):
        self.cnx = mysql.connector.connect(**FIELDS, database=DB_NAME)
        self.cat_id = None
        self.nutriscore_product_choose = None
        self.id_product_choose = None
        self.id_product_substitute = None
        self.response = ['Y', 'N']

    def show_category(self):
        """Show the category"""
        cursor = self.cnx.cursor()
        dict_category = {}
        category = ("SELECT id, name FROM Category;")
        cursor.execute(category)
        rows = cursor.fetchall()
        print("\n\nlist of categories: \n")
        for i, row in rows:
            print('{} : {}'.format(i, row))
            dict_category[i] = row

        while True:
            try:
                self.cat_id = int(input("\n\nChoose id cat : \n"))
                cat_choose = dict_category[self.cat_id]
                break
            except ValueError:
                print("It has to be a number")
            except KeyError:
                print("You have to choose a good number for cat")
        print("You choose {} category\n\n".format(cat_choose))

    def show_product(self):
        """Show the products of the chosen category"""
        print("Here list of products in this category: \n")

        cursor = self.cnx.cursor()
        get_product = ("SELECT id, name FROM Product WHERE category={}".format(self.cat_id))
        cursor.execute(get_product)
        result = cursor.fetchall()
        coef = (self.cat_id-1)*20
        for i in range(len(result)):
            map_id = result[i][0] - coef
            print("{}. {}".format(map_id, result[i][1]))

        while True:
            try:
                self.id_product_choose = int(input("\nChoose id product: \n"))
                self.id_product_choose = self.id_product_choose + coef              
                get_nutriscore = ("SELECT nutriscore \
                	FROM Product WHERE id={} \
                	AND category={}".format(self.id_product_choose, self.cat_id))
                cursor.execute(get_nutriscore)
                self.nutriscore_product_choose = cursor.fetchall()[0][0]
                break
            except ValueError:
                print("It has to be a number")
            except IndexError:
                print("You have to choose a good number for cat")

        cursor.close()
        print("\nThe product you choose have this nutriscore : {} \n\n".format(
            self.nutriscore_product_choose
        ))

    def show_substitute(self):
        """Show the substitutes"""
        cursor = self.cnx.cursor()
        query = ("SELECT id, name, nutriscore, store, link \
            FROM Product WHERE nutriscore <= '{}' \
            AND category={} AND id !={}".format(
                self.nutriscore_product_choose,
                self.cat_id,
                self.id_product_choose
                )
                )
        cursor.execute(query)
        result = cursor.fetchall()

        coef = (self.cat_id-1)*20
        print("Here the list of product with a better or equivalent nutriscore:\n")
        for i in range(len(result)):
            map_id = result[i][0] - coef
            if result[i][0] is None:
                print('There is no substitute')
            else:
                print(
                    "{}. {} with nutriscore: {}. \n"
                    " Can buy at {} more informations on this link : \n{}\n"
                    .format(
                        map_id, result[i][1],
                        result[i][2],
                        result[i][3],
                        result[i][4]
                        )
                    )

        while True:
            try:
                self.id_product_substitute = int(input("\n Choose id product: \n"))
                self.id_product_substitute = self.id_product_substitute + coef
                break
            except ValueError:
                print("It has to be a number")
            except IndexError:
                print("You have to choose a good number for product")

        save = ()
        while save not in ['Y', 'N']:
            save = input('\nDo you want to save this substitute?\n"Y" or "N"\n').upper()

        if save == "Y":
            query = ("INSERT INTO Substitute \
                    (id_product_to_substitute, id_substitute_product) VALUES ({}, {})".format(
                        self.id_product_choose,
                        self.id_product_substitute)
                    )
            cursor.execute(query)
            self.cnx.commit()
        cursor.close()

    def continu(self):
        """Return to the beginning"""
        answer = ()
        while answer not in self.response:
            answer = str(input('\nDo you want to continue ?\n"Y" or "N"\n').upper())

        if answer == "Y":
            print("\nWell, now choose a category of product you want to replace: ")
            return True

        if answer == "N":
            print("\nGoodbye thanks.\n")
            exit(1)

        return False

    def consult_substitutes(self):
        """Display registered susbtitutes"""
        while True:
            try:
                response = ()
                while response not in [1, 2]:
                    response = int(
                        input(
                            "\n1 - Select a category to replace.\n"
                            "2 - Show your substitutes ?\n"
                        ).upper()
                    )
                    if response not in [1, 2]:
                        print("\nYou have to choose between 1 or 2.")
                break
            except ValueError:
                print("\nIt has to be a number")

        if response == 2:
            query = ("SELECT name, nutriscore, store, link \
                    FROM Product \
                    INNER JOIN Substitute \
                    ON Substitute.id_substitute_product = Product.id")

            cursor = self.cnx.cursor()
            cursor.execute(query)
            results = cursor.fetchall()

            i = 1
            print('\n\nHere is the list of your substitutions: \n')
            for result in results:
                print(
                    "{}. {} with nutriscore : {}.\n"
                    "can buy at {} more information on this link : \n{}\n"
                    .format(
                        i, result[0], result[1], result[2], result[3]
                    )
                )
                i += 1
            self.continu()
