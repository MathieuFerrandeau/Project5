import requests
import json 

res = requests.get("https://fr.openfoodfacts.org/categories&json=1")
result = res.json()


print(result)