import json
import models
from connect import db

with open('cats.json', 'r', encoding='utf-8') as c:
    cats_data = json.load(c)

for cat_data in cats_data:
    c = db.cat.insert_one(cat_data)
