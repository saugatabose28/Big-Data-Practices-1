#Write a program in Python, to read the Tweet Dataset from MongoDB. For each tweet, 
#output/display its ‘text’ field in Python console. 
 
from pymongo import MongoClient 
client: MongoClient = MongoClient('127.0.0.1',27017) 
db = client["myNewDB"] 
tweets = db["tweets"] 

for t in tweets.find(): 
    print(t["text"] + "\#n") 
   # 
##Write a program in Python, to read the Tweet Dataset from MongoDB. Find the tweets where the 
#user id is smaller than 224499494522, output/display ‘user name’ field of these tweets in Python 
#console. 
query = {"user.id":{"$lt":224499494522}} 
for docs in tweets.find(query):  
    print(docs["user"]["name"] + "\n")

##Write a MongoDB query to update a user’s (user name is ‘user 23’) screen_name as 
#‘Superman’. 
##and Write a MongoDB query to remove or delete a user’s information (the user’s screen_name 
#is ‘Superman’)     
tweets.update_one({"user.name":"user 23"},{"$set":{"user.screen_name":"Superman"}})
x = tweets.delete_one({"user.screen_name":"Superman"}) 
print(x.deleted_count, " documents deleted.")
    
## insert 2 records in new collection
db = client["mydatabase"] 
col = db["mycollections"] 

mylist = [ {"name": "Candy", "address": "Northway 75"}, {"name": "Amy", "address": "Apple st 652"}] 
x = col.insert_many(mylist) 

print(client.list_database_names()) 
print(db.list_collection_names())