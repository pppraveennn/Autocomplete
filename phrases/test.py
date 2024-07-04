import csv

good_phrases = [{"Phrase": "Hello world", "Optimal": "hello w"},
                {"Phrase": "How to tie a tie", "Optimal": "how to"}]

with open("phrases/output.csv", "w") as csvfile:
    fieldnames = ["Phrase", "Optimal"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for phrase in good_phrases:
        writer.writerow(phrase)