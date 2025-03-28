from pymongo import MongoClient 
import nltk 
from nltk.tokenize import word_tokenize 
from nltk.stem import PorterStemmer 
from nltk.corpus import stopwords 
import re 

def download_nltk() -> None: 
 """need to download these once before you can run any of their related methods  on a computer""" 
 nltk.download("stopwords") #used for stopwords 
 nltk.download("punkt") #used for tonkenising 
 nltk.download('averaged_perceptron_tagger') #used for Parts-of-Speech tagging 

def remove_stopwords(words: list) -> list: 
 """returns list of words without inconsequetial/unimportant/common words""" 
 result: list = [] 
 for w in words: 
    if w not in stopwords.words("english"): 
        result.append(w) 
 return result 

def stem_words(words: list) -> list: 
 """reduces words to their root word by removing derivational affixes""" 
 ps: PorterStemmer = PorterStemmer() 
 result: list = []
 for w in words:
    result.append(ps.stem(w)) 
 return result 

def find_keywords_in_text(text: str) -> list: 
 text = re.sub(r"[^\w]"," ", text) #removes non-alphabetical symbols (like punctuation and numbers) 
 words: list = word_tokenize(text) #convert into list of words 
 words = remove_stopwords(words) #remove stopwords 
 words = stem_words(words) #make the words undergo a form of linguistic normalisation 
 keywords: list = nltk.pos_tag(words) #run Parts-of-Speech tagging to identify grammatical groupings of keywords 
 return keywords 

#accesses database and its collection 'Tweets' 
client: MongoClient = MongoClient('127.0.0.1',27017) 
db = client["myNewDB"] 
tweets = db["tweets"]
nltk.download() #only necessary on first time the script is run, left in to demonstrate
#loops through each tweet, calls various functions to help in extracting keywords, 
#then updates the database with the keywords in CSV format 
for t in tweets.find():
    keywords = find_keywords_in_text(t["text"])
    for k in keywords:
        print(k)
    print("\n")