from fastapi import FastAPI, Path
from fastapi.middleware.cors import CORSMiddleware
import random
import csv

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"]
)

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