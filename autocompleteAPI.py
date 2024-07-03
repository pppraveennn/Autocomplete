from fastapi import FastAPI, Path
from typing import Optional
import requests
from pydantic import BaseModel
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

reader = csv.DictReader(open('phrases.csv'))
phrases = []
for row in reader:
    phrases.append(row)

def get_guess(phrase: str, guess_length: int):
    guess = ""
    i = 0
    while i < guess_length:
        try:
            if phrase[i] == " ":
                guess_length += 1
            guess += phrase[i]
            i += 1
        except IndexError:
            break
    return guess

def phrase_length(phrase: str):
    phrase = list(phrase)
    length = 0
    for i in range(len(phrase)):
        if (phrase[i] != " "):
            length += 1
    return length

@app.get("/get-phrase")
def get_phrase():
    return random.choice(phrases)

@app.get("/get-score")
def get_score(phrase: str, guess: str):
    phrase = phrase.lower()
    guess = guess.lower()  
    guess_length = phrase_length(guess)
    if (guess_length == 0):
        return {"Error": "Type in a guess!"}  
    if phrase.find(guess) != 0:
        return {"Error": "Your guess must be a part of the phrase!"}  
    for i in range(1, len(phrase)):
        guess = get_guess(phrase, i)
        response = requests.get("http://suggestqueries.google.com/complete/search?client=chrome&q="+guess)
        if (not response):
            return {"Error": "Could not access autocomplete API, please try again"}
        autocompletes = response.json()[1][:9]
        if (phrase in autocompletes):
            return {"Score": max(i - guess_length, guess_length - i),
                    "Optimal": get_guess(phrase, i)}
    return {"Score": phrase_length(phrase) - guess_length,
            "Optimal": phrase}
