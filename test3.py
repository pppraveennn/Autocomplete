import csv

reader = csv.DictReader(open('example.csv'))
phrases = []
for row in reader:
    phrases.append(row)
print(phrases)