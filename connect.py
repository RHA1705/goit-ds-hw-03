# from mongoengine import connect
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import configparser


config = configparser.ConfigParser()
config.read('config.ini')

mongo_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'pass')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')

# connect to cluster on AtlasDB with connection string

client = MongoClient(f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority&appName=Cluster0""",
                                            server_api=ServerApi('1'))

db = client['goit-ds-hw-03']
# print("Connection success")
