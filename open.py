import requests
import json 

res = requests.get("https://fr.openfoodfacts.org/categories&json=1")
data_json = res.json()
data_tags = data_json.get('tags')
data_cat = [d.get('name') for d in data_tags]

for category in data_cat[:10]:
	print(category)


