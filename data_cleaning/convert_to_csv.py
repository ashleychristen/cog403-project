import json
import csv

with open('organized_info.json', 'r') as f:
    data = json.load(f)

with open('organized_info.csv', 'w') as f:
    writer = csv.writer()
    writer.writerow(['code', 'language', ''])