import PySense
import csv

if not PySense.authenticate_by_file('C:\\PySenseConfig.yaml'):
    print("Auth error")
    exit(1)

with open("users.csv", encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        PySense.post_user(row[0], row[1], row[2], row[3], row[4], groups=row[5].split(','))

