import csv

reader = csv.DictReader(open('phrases.csv'))
phrases = []
for row in reader:
    phrases.append(row)
print(phrases)

