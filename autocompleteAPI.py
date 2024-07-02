from fastapi import FastAPI, Path
from typing import Optional
import requests
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"]
)

url = "http://suggestqueries.google.com/complete/search?client=chrome&q=hello"

def get_guess(phrase: str, guess_length: int):
    phrase = list(phrase)
    for i in range(len(phrase)):
        if phrase[i] == " ":
            phrase[i] = "%20"
    guess = ""
    i = 0
    while i < guess_length:
        if phrase[i] == "%20":
            guess_length += 1
        guess += phrase[i]
        i += 1
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
    return {"Phrase": "Hello"}

@app.get("/get-score")
def get_score(phrase: str, guess: str):  
    guess_length = phrase_length(guess)
    if guess not in phrase:
        return {"Error": "Invalid guess"}  
    for i in range(1, len(phrase)):
        guess = get_guess(phrase, i)
        response = requests.get("http://suggestqueries.google.com/complete/search?client=chrome&q="+guess)
        if (not response):
            return {"Error": "Could not access autocomplete API"}
        autocompletes = response.json()[1][:9]
        if (phrase in autocompletes):
            return {"Score": max(i - guess_length, guess_length - i)}
    return {"Score": phrase_length}
