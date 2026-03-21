import json
import csv

with open('cleaned_data/modified_info_standardized.json', 'r') as f:
    data = json.load(f)

both1 = ('1A', '3A', '4A', '6A', '7A', '8A', '9A', '11A', '13A', '14A', '16A', '20A', '21A', '21B', '22A', '23A', '24A', '25B', '26A', '27A', '28A', '29A')
both2 = ('2A', '9A', '11A', '13A', '16A', '17A', '19A', '20A', '22A', '23A', '25B', '26A', '27A', '29A')
both3 = ('2A', '13A', '23A', '25B')
both = [both1, both2, both3]

south = 0
north = 0
east = 0
west = 0

chosen_languages = []
for i in range(3):
    for language in data:

        same = 0

        feats = data[language].keys()
        for f in both[i]:
            if f in feats:
                same += 1
        
        if same == len(both[i]):

            chosen_languages.append(language)

chosen_languages = set(chosen_languages)
outfile = "coords.csv"
with open(outfile, 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['language', 'latitude', 'longitude'])
    for lang in chosen_languages:

        lat = data[lang]['latitude']
        long = data[lang]['longitude']

        if long > 0:
            east += 1
        else:
            west += 1
        
        if lat > 0:
            north += 1
        else:
            south += 1


        writer.writerow([lang, lat, long])

print(f"south: {south} ({south / (north + south)} %), north: {north} ({north / (north + south)} %)")

print(f"east: {east} ({east / (east + west)} %), west: {west} ({west / (east + west)} %)")