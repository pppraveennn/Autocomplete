from fastapi import FastAPI, Path
from fastapi.middleware.cors import CORSMiddleware
import pymongo
from pydantic import BaseModel
import random
import csv
from datetime import date
import os
from dotenv import load_dotenv


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"]
)

load_dotenv()
dbpass = os.getenv("autocompletedbpass")
client = pymongo.MongoClient("mongodb+srv://praveencubes:"+dbpass+"@autocomplete.fbrspbu.mongodb.net/?retryWrites=true&w=majority&appName=Autocomplete")
db = client["high_scores"]
col = db["scores"]

@app.get("/")
async def root():
    return {"message": "Check /docs for documentation"}

reader = csv.DictReader(open('phrases/phrases.csv'))
phrases = []
for row in reader:
    phrases.append(row)

@app.get("/get-phrase")
def get_phrase():
    return random.choice(phrases)

@app.get("/get-phrase-list")
def get_phrase_list():
    phrase_list = []
    while len(phrase_list) < 10:
        phrase = random.choice(phrases)
        if phrase not in phrase_list:
            phrase_list.append(phrase)
    phrase_dict = {}
    for i in range(1, len(phrase_list) + 1):
        phrase_dict[str(i)] = phrase_list[i-1]
    return phrase_dict

@app.get("/get-leaderboard")
def get_leaderboard():
    doc = col.find().sort({"Score": 1, "Year": 1, "Month": 1, "Day": 1}).limit(10)
    response = {}
    for count, row in enumerate(doc, start=1):
        row.pop("_id", None)
        response[str(count)] = row
    return response

@app.get("/get-rank")
def get_rank(score: int):
    doc = col.find().sort("Score")
    doclist = list(doc)
    for i in range(len(doclist)-1, -1, -1):
        if doclist[i]["Score"] == score:
            return {"Rank": i+1}

class Item(BaseModel):
    score: int

@app.post("/post-score")
def post_score(score: Item):
    today = date.today()
    year = today.strftime("%Y")[-2:]
    month = today.strftime("%m")
    day = today.strftime("%d")
    submission = {"Score": score.score, 
                  "Year": year,
                  "Month": month,
                  "Day": day}
    col.insert_one(submission)
    submission.pop("_id", None)
    return submission

@app.post("/test-post")
def post_test():
    return {"Message": "Success"}

