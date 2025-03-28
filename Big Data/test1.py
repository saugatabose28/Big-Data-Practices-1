import pymongo 
client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["mydatabase"]

col = db["mycollections"]

mylist = [ {"name": "Candy", "address": "Northway 75"},
{"name": "Amy", "address": "Apple st 652"}] 
x = col.insert_many(mylist)

print(client.list_database_names())
print(db.list_collection_names())