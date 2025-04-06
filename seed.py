import json
import connect
import models

with open('cats.json', 'r') as a:
    cats_data = json.load(a)

for cat_data in cats_data:
    cats = models.Cat(name=cat_data['name'], age=cat_data['age'], features=cat_data['features'])
    cats.save()
