import csv
import re

empty = 0
valid = 0

with open('Repository_data.csv','rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        regex = re.compile("'(.+?)'")
        topic = regex.findall(row['Topic'])
        if not topic :
            empty += 1
        else:
            valid += 1
    print empty, valid