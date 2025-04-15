import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client.assignment_1
collection = db.song

def extract(output_file):

    with open(output_file, "w") as f:
        for song in collection.find():
            artist = song["Artist"]
            year = song["Year"]
            sales = song["Sales"]
            f.write(f'\"{artist}\", {year}, {sales}\n')

extract('task1_1_output.txt')