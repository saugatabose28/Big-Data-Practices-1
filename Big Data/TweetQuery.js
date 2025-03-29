// as we already heave a databse named "myNewDB" and collection named "tweets "run this query-> mongosh myNewDB TweetQuery.js

// Insert 2 new Tweets to the collection

db.tweets.insert( 
{ 
 
 "created_at": "Thu Apr 06 15:24:15 +0000 2020", 
 "id_str": "1850006245121695744", 
 "text": "Have a nice day", 
 "user": { 
  "id": NumberLong(2244456599494501), 
  "name": "user 01", 
  "screen_name": "Twitter User", 
  "location": "Internet", 
  "url": "user URL", 
  "description": "user description" 
 }, 
 "place": { 
 
 }, 
 "entities": { 
  "hashtags": [ 
 
  ], 
  "urls": [{ 
   "url": "twt url sample", 
   "unwound": { 
    "url": "url sample", 
    "title": "web page title" 
   } 
  }], 
  "user_mentions": [ 
 
  ] 
 } 
}) 
//Tweet 2 
db.tweets.insert( 
{ 
 
 "created_at": "Thu Apr 06 15:24:15 +0000 2020", 
 "id_str": "1850006245121695744", 
 "text": "Good Morning", 
 "user": { 
  "id": NumberLong(2244456599494501), 
  "name": "user 01", 
  "screen_name": "Twitter User", 
  "location": "Internet", 
  "url": "user URL", 
  "description": "user description" 
 }, 
 "place": { 
 
 }, 
 "entities": { 
  "hashtags": [ 
 
  ], 
  "urls": [{ 
   "url": "twt url sample", 
   "unwound": { 
    "url": "url sample", 
    "title": "web page title" 
   } 
  }], 
  "user_mentions": [ 
 
  ] 
 } 
}) 

// Write a MongoDB query that returns all the Tweets. 
 
db.Tweets.find() 
 
// Write a MongoDB query to find one of your Tweets with user’s name: "user 30". 

db.Tweets.findOne({"user.name":"user 30"})  

// Update two Tweets to have two tags called “My first tag” and “My second tag” respectively using update() and or using save().  

db.Tweets.update({"user.name":"user 30"}, {$set:{"tag":"My first tag"}})  

var tweet_user40 = db.Tweets.findOne({"user.name":"user 40"}) 
tweet_user40["tag"] = "My second tag" 
db.Tweets.save(tweet_user40) 

// Write a MongoDB query to retrieve all documents from the Tweets collection where user name 
//equals either "user 30" or "user 40". 
 
db.Tweets.find({"user.name":{ $in: [ "user 30", "user 40" ] } }) 

// Write a MongoDB query to retrieve all documents from the Tweets collection where user 
//screen_name is "Twitter User" and user location is "Internet". (Specify AND Conditions) 

db.Tweets.find({$and: [{"user.screen_name": "Twitter User"}, {"user.location":"Internet"}]}) 

// Write a MongoDB query to retrieve all documents from the Tweets collection where user 
//screen_name is "Twitter User" or user url is "user URL". (Specify OR Conditions) 
 
db.Tweets.find({ $or: [{"user.screen_name": "Twitter User"}, {"user.url":"user URL"}]}) 

// Write a MongoDB query to retrieve all documents from the Tweets collection where user id is not 
224499494502. 
 
//Solution 1: 
db.Tweets.find({"user.id":{$ne:224499494502}}) 
//Solution 2: 
//db.Tweets.find({"user.id":{$not:{$eq:224499494502}}})

// Write a MongoDB query to retrieve all documents from the Tweets collection where user names 
// do not equal "user 30" and "user 40". 

//Solution 1: 
db.Tweets.find({"user.name":{$not: { $in: [ "user 30", "user 40" ] }} }) 
//Solution 2: 
//db.Tweets.find({"user.name":{$nin: [ "user 30", "user 40" ] } }) 

//Write a MongoDB query that returns all Tweets in which the field “tag” has values. Note that not 
//all the Tweets have tags, obviously. 
 
db.Tweets.find({"tag": {$exists:true}}) 
// Write a MongoDB query to display the first 10 Tweets which has the screen name with value 
//"Twitter User" (i.e., "screen_name": "Twitter User"). 
 
db.Tweets.find({"user.screen_name":"Twitter User"}).limit(10) 

//Write a MongoDB query to find the Tweets where the Tweet id (i.e., id_str) is greater than 
//8000000000000000000 but less than 9000000000000000000. 
 
db.Tweets.find({"id_str":{"$gt":"8000000000000000000","$lt":"9000000000000000000"}}) 

//Write a MongoDB query to return the "Tweet Id", "name" and "location" fields for those 
//Tweetswhich contain "Thu" as first three letters for its "created_at" field. 
 
db.Tweets.find({"created_at":{"$regex":"Thu"}},{"user.id":1,"user.name":1,"user.location":1}) 

//Write a MongoDB query to find the Tweet Id ("id_str") for those Tweets which contain 
//thekeyword “Sydney” in their text. 
 
db.Tweets.find({"text":/Sydney/},{"id_str":1}) 

//Write a MongoDB query to count the number of the Tweets whose user id is greater 
//than224499494502 but less than 224499494522. 
 
db.Tweets.find({"user.id":{"$gt":224499494502,"$lt":224499494522}}).count() 

//Write a MongoDB query to sort all the Tweets in descending order according to the created 
//time("created_at"). Repeat the question and output in ascending order. 
 
db.Tweets.find().sort({"created_at":-1}) 
db.Tweets.find().sort({"created_at":1}) 

//Write a MongoDB query to find the three earliest tweets (according to created time). 

db.Tweets.find().sort({"created_at":1}).limit(3) 

//Write a MongoDB query to update a user’s (user name is ‘user 21’) screen_name as ‘Superman’. 
 
db.Tweets.update({"user.name":"user 21"},{$set:{"user.screen_name":"Superman"}}) 

//Write a MongoDB query to remove or delete a user’s information (the user’s screen_name is 
//‘Superman’) 
 
db.Tweets.remove({"user.screen_name":"Superman"}) 
//or
//db.Tweets.deleteOne({"user.screen_name":"Superman"}) 

//Write a MongoDB query to retrieve all documents from the Tweets collection where user id is 
//not 224499494502. 
 
db.Tweets.find({"user.id":{$ne:224499494502}}) 
//or 
//db.Tweets.find({"user.id":{$not:{$eq:224499494502}}}) 

//Write a MongoDB query to retrieve all documents from the Tweets collection where user names 
//do not equal "user 30" and "user 40". 

db.Tweets.find({"user.name":{$not: { $in: [ "user 30", "user 40" ] }} }) 
//or 
//db.Tweets.find({"user.name":{$nin: [ "user 30", "user 40" ] } }) 

