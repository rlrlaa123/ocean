import csv
import re

empty = 0
valid = 0

with open('Repository_data.csv','rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        regex = re.compile("'(.+?)'")
        topic = regex.findall(row['Topic'])
        with open ('Topic_data.csv','a') as csvfile:
            writer = csv.writer(csvfile)
            if not topic :
                empty += 1
            else:
                valid += 1
                writer.writerow([row['full_name']]+topic)
    print empty, valid