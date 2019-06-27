<h1><strong>Project 5: Use public data from OpenFoodFacts</strong></h1>

This project uses openfoodfacts data to allow a user to choose from a product list a substitute with a nutriscore superior or equivalent to the chosen product.   
As well as to save this substitute so as to retrieve the information that interest the user like the name, stores where to buy it and an url link with all the features of the product.

<h2>How to use it:</h2>

<ol>
	<li>Change FIELDS in config.py file with your own mysql credentials.</li>
	<li>Enter the following command in you console : pip install -r requirements.txt</li>
	<li>Enter the following command : python3 main.py -i (or --init) .</li>
	<li>And finally run the main.py file.</li>
</ol>

Once the connection is established the user has two possibilities: 
<li>Select from a list of 10 categories a product to have substitutes with a nutriscore equivalent or higher, 
to choose one and have the possibility to save it or not in its list of substitutes.</li>
<li>The possibility to consult its list of surrogates registered beforehand (empty if first connection).</li>

<h2>Operation:</h2>

<ul><strong>sql.py:</strong><br>	
	<li>In init we pass all the parameters of authenticity in parameter.</li>
	<li>First method we use these parameters to create the database.</li>
	<li>Second method we use all the parameters to connect to the database.</li>
	<li>Third method we create the tables of the database thanks to the .sql file.</li>
</ul>

<ul><strong>collect_data.py:</strong><br>
	<li>The first method retrieves API categories and insert 10 in the Category table.</li>
	<li>The second method retrieves 20 products for each category from the Category table and inserts them into the Product table.</li>
</ul>

<ul><strong>init.py</strong><br>
	<li>The method allows you to initialize the database with the methods of classes Sql and Colledata (from its creation to repmlissage).</li>
</ul>

<ul><strong>program.py:</strong><br>
	<li>The first method displays the 10 categories.</li>
	<li>The second method displays 20 products according to the chosen category</li>
	<li>The third method is to display a substitute that has a nutrient equivalent or greater than the product previously selected with the possibility to save it in the database or not.</li>
	<li>The fourth method allows the user once all completed steps to return to the main menu or exit the application.</li>
	<li>Finally the last method allows the user to consult his list of registered surrogates (empty if first use).</li>
</ul>

<ul><strong>main.py:</strong><br>
	<li>The main file can be called two ways, the first using an argument (-i or --init) will create and fill the database thanks to the class Init.
And the second, by executing it without argument, it will launch the application that will allow the interaction between the user and the program.</li>
</ul>