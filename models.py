from mongoengine import Document
from mongoengine.fields import StringField, ListField, IntField, DictField


class Cat(Document):
    name = StringField()
    age = IntField()
    features = ListField()
