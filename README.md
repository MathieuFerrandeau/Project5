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

<ul>sql.py:
	<li>In init we pass all the parameters of authenticity in parameter.</li>
	<li>First method, we use these parameters to create the database.</li>
	<li>Second method, we use all the parameters to connect to the database.</li>
	<li>Third method, we create the tables of the database thanks to the .sql file.</li>
</ul>