from pymongo import MongoClient

connection_string = "mongodb://mongoadmin:mongoadmin@localhost:27017/"
client = MongoClient(connection_string)
db = client.stock
