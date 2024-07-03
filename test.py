import requests

def get_guess(phrase: str, guess_length: int):
    phrase = list(phrase)
    for i in range(len(phrase)):
        if phrase[i] == " ":
            phrase[i] = "%20"
    print(phrase)
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

guess = get_guess("book a hotel room in hawaii", 3)
print(guess)
response = requests.get("http://suggestqueries.google.com/complete/search?client=chrome&q="+guess)
autocompletes = response.json()[1][:9]
print(autocompletes)